/**
 * 音频录制与播放管理器
 *
 * H5 模式：Web Audio API
 * 小程序模式：uni.getRecorderManager（MVP 阶段暂不实现）
 */

export class AudioManager {
  constructor() {
    this.isRecording = false
    this.onAudioChunk = null // callback: (pcmInt16Array: Int16Array) => void

    this._audioContext = null
    this._mediaStream = null
    this._scriptProcessor = null
    this._sources = [] // 活跃的播放源，用于打断时停止
  }

  // ---- H5 录音 ----

  async startRecordingH5() {
    this._audioContext = new (window.AudioContext || window.webkitAudioContext)({
      sampleRate: 16000,
    })

    this._mediaStream = await navigator.mediaDevices.getUserMedia({
      audio: {
        sampleRate: 16000,
        channelCount: 1,
        echoCancellation: true,
        noiseSuppression: true,
      },
    })

    const source = this._audioContext.createMediaStreamSource(this._mediaStream)
    // ScriptProcessorNode 虽然已 deprecated，但 AudioWorklet 在部分浏览器兼容性不佳
    this._scriptProcessor = this._audioContext.createScriptProcessor(4096, 1, 1)

    this._scriptProcessor.onaudioprocess = (event) => {
      if (!this.isRecording) return
      const float32 = event.inputBuffer.getChannelData(0)
      const int16 = this._float32ToInt16(float32)
      if (this.onAudioChunk) this.onAudioChunk(int16)
    }

    source.connect(this._scriptProcessor)
    this._scriptProcessor.connect(this._audioContext.destination)
    this.isRecording = true
  }

  stopRecordingH5() {
    this.isRecording = false
    if (this._scriptProcessor) {
      this._scriptProcessor.disconnect()
      this._scriptProcessor = null
    }
    if (this._mediaStream) {
      this._mediaStream.getTracks().forEach((t) => t.stop())
      this._mediaStream = null
    }
    if (this._audioContext) {
      this._audioContext.close()
      this._audioContext = null
    }
  }

  // ---- H5 播放 ----

  playAudioH5(pcmInt16Array, sampleRate = 24000) {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)({
      sampleRate,
    })
    const buffer = audioContext.createBuffer(1, pcmInt16Array.length, sampleRate)
    const channelData = buffer.getChannelData(0)
    for (let i = 0; i < pcmInt16Array.length; i++) {
      channelData[i] = pcmInt16Array[i] / 32768.0
    }
    const source = audioContext.createBufferSource()
    source.buffer = buffer
    source.connect(audioContext.destination)
    source.start()
    this._sources.push({ source, context: audioContext })
    source.onended = () => {
      audioContext.close()
      this._sources = this._sources.filter((s) => s.source !== source)
    }
  }

  /** 停止所有正在播放的音频（用于打断） */
  stopAllPlayback() {
    for (const { source, context } of this._sources) {
      try {
        source.stop()
        context.close()
      } catch {}
    }
    this._sources = []
  }

  // ---- 工具方法 ----

  _float32ToInt16(float32Array) {
    const int16 = new Int16Array(float32Array.length)
    for (let i = 0; i < float32Array.length; i++) {
      const s = Math.max(-1, Math.min(1, float32Array[i]))
      int16[i] = s < 0 ? s * 0x8000 : s * 0x7fff
    }
    return int16
  }
}
