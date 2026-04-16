/**
 * Pipecat WebSocket 客户端
 *
 * 封装与 Pipecat 后端的 WebSocket 通信，
 * 处理 protobuf 帧的编解码。
 */

import { encodeAudioFrame, decodeFrame } from './protobuf-client.js'

export class PipecatWebSocket {
  constructor(url) {
    this.url = url
    this.ws = null

    // 回调
    this.onUserTranscript = null // (text: string, isFinal: boolean) => void
    this.onBotText = null // (text: string) => void
    this.onBotAudio = null // (pcmInt16Array: Int16Array, sampleRate: number) => void
    this.onConnected = null // () => void
    this.onDisconnected = null // () => void
    this.onError = null // (err: Error) => void
  }

  connect() {
    // #ifdef H5
    this.ws = new WebSocket(this.url)
    this.ws.binaryType = 'arraybuffer' // 关键：必须设为 arraybuffer 才能接收二进制帧

    this.ws.onopen = () => {
      if (this.onConnected) this.onConnected()
    }

    this.ws.onmessage = (event) => {
      this._handleMessage(event.data)
    }

    this.ws.onclose = () => {
      if (this.onDisconnected) this.onDisconnected()
    }

    this.ws.onerror = (err) => {
      if (this.onError) this.onError(err)
    }
    // #endif

    // #ifdef MP-DINGTALK
    // 钉钉小程序 WebSocket（MVP 阶段暂用 H5 模式调试）
    // this.ws = uni.connectSocket({ url: this.url })
    // this.ws.onOpen(() => { if (this.onConnected) this.onConnected() })
    // this.ws.onMessage((res) => this._handleMessage(res.data) })
    // this.ws.onClose(() => { if (this.onDisconnected) this.onDisconnected() })
    // #endif
  }

  /**
   * 发送音频帧给 Pipecat
   * @param {Int16Array} pcmInt16Array - PCM 16-bit 音频数据
   */
  sendAudio(pcmInt16Array) {
    if (!this.ws || this.ws.readyState !== 1) return // WebSocket.OPEN = 1

    const buffer = encodeAudioFrame(pcmInt16Array.buffer, 16000, 1)

    // #ifdef H5
    this.ws.send(buffer)
    // #endif

    // #ifdef MP-DINGTALK
    // 钉钉小程序可能需要 base64 编码二进制数据
    // this.ws.send({ data: arrayBufferToBase64(buffer) })
    // #endif
  }

  /**
   * 处理接收到的消息
   */
  _handleMessage(data) {
    let buffer
    if (data instanceof ArrayBuffer) {
      buffer = data
    } else if (typeof data === 'string') {
      // 可能是 base64 编码的二进制（小程序环境）
      buffer = this._base64ToArrayBuffer(data)
    } else {
      return
    }

    const frame = decodeFrame(buffer)
    if (!frame) return

    switch (frame.type) {
      case 'transcription':
        if (this.onUserTranscript) {
          this.onUserTranscript(frame.text || '', frame.isFinal !== false)
        }
        break
      case 'text':
        if (this.onBotText) this.onBotText(frame.text || '')
        break
      case 'audio':
        if (this.onBotAudio) {
          this.onBotAudio(frame.audio, frame.sample_rate || 24000)
        }
        break
      case 'message':
        // 系统消息，可忽略或显示
        break
    }
  }

  close() {
    if (this.ws) {
      // #ifdef H5
      this.ws.close()
      // #endif
      // #ifdef MP-DINGTALK
      // uni.closeSocket()
      // #endif
      this.ws = null
    }
  }

  _base64ToArrayBuffer(base64) {
    const binary = atob(base64)
    const bytes = new Uint8Array(binary.length)
    for (let i = 0; i < binary.length; i++) {
      bytes[i] = binary.charCodeAt(i)
    }
    return bytes.buffer
  }
}
