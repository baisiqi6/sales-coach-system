/**
 * Pipecat Protobuf 帧编解码器
 *
 * 处理 Pipecat 的 ProtobufFrameSerializer 编码的帧。
 * 使用 protobufjs/minimal 解析帧。
 *
 * 帧类型：
 * - TextFrame: LLM 文本输出
 * - AudioRawFrame: 原始 PCM 音频
 * - TranscriptionFrame: ASR 转录结果
 * - UserImageRawFrame / ImageRawFrame: 图像（MVP 不用）
 */

// protobufjs/minimal 加载
let protobuf
try {
  protobuf = require('protobufjs/minimal')
} catch {
  // H5 环境可能通过 CDN 或 npm 引入
  protobuf = null
}

// Pipecat frames.proto 的 JSON 描述符（精简版，只含 MVP 需要的类型）
const ROOT_JSON = {
  nested: {
    pipecat: {
      nested: {
        Frame: {
          oneofs: { frame: { oneof: ['textFrame', 'audioRawFrame', 'transcriptionFrame', 'messageFrame'] } },
          fields: {
            textFrame: { type: 'TextFrame', id: 1 },
            audioRawFrame: { type: 'AudioRawFrame', id: 2 },
            transcriptionFrame: { type: 'TranscriptionFrame', id: 3 },
            messageFrame: { type: 'MessageFrame', id: 4 },
          },
        },
        TextFrame: {
          fields: {
            id: { type: 'uint64', id: 1 },
            name: { type: 'string', id: 2 },
            text: { type: 'string', id: 3 },
          },
        },
        AudioRawFrame: {
          fields: {
            id: { type: 'uint64', id: 1 },
            name: { type: 'string', id: 2 },
            audio: { type: 'bytes', id: 3 },
            sampleRate: { type: 'uint32', id: 4 },
            numChannels: { type: 'uint32', id: 5 },
          },
        },
        TranscriptionFrame: {
          fields: {
            id: { type: 'uint64', id: 1 },
            name: { type: 'string', id: 2 },
            text: { type: 'string', id: 3 },
            language: { type: 'string', id: 4 },
            timestamp: { type: 'uint64', id: 5 },
            isFinal: { type: 'bool', id: 6 },
          },
        },
        MessageFrame: {
          fields: {
            id: { type: 'uint64', id: 1 },
            name: { type: 'string', id: 2 },
            message: { type: 'string', id: 3 },
          },
        },
      },
    },
  },
}

let FrameType

/**
 * 初始化 protobuf 类型（懒加载）
 */
function _ensureInit() {
  if (FrameType) return
  if (!protobuf) {
    console.warn('protobufjs not available, using fallback codec')
    return
  }
  const root = protobuf.Root.fromJSON(ROOT_JSON)
  FrameType = root.lookupType('pipecat.Frame')
}

/**
 * 编码音频帧，发送给 Pipecat
 * @param {ArrayBuffer} pcmData - PCM 16-bit 音频数据
 * @param {number} sampleRate - 采样率（默认 16000）
 * @param {number} numChannels - 声道数（默认 1）
 * @returns {Uint8Array} protobuf 编码后的二进制数据
 */
export function encodeAudioFrame(pcmData, sampleRate = 16000, numChannels = 1) {
  _ensureInit()

  if (!FrameType) {
    // Fallback: 直接发送原始 PCM（Pipecat 需要序列化器才能解析）
    return new Uint8Array(pcmData)
  }

  const payload = {
    audioRawFrame: {
      name: 'InputAudioRawFrame',
      audio: new Uint8Array(pcmData),
      sampleRate,
      numChannels,
    },
  }

  const errMsg = FrameType.verify(payload)
  if (errMsg) throw new Error(`Protobuf encode error: ${errMsg}`)

  const msg = FrameType.create(payload)
  return FrameType.encode(msg).finish()
}

/**
 * 解码从 Pipecat 接收的帧
 * @param {ArrayBuffer} buffer - 二进制数据
 * @returns {{ type: string, text?: string, audio?: Int16Array, sample_rate?: number, language?: string, isFinal?: boolean } | null}
 */
export function decodeFrame(buffer) {
  _ensureInit()

  if (!FrameType) {
    // Fallback: 无法解码
    console.warn('No protobuf decoder available')
    return null
  }

  try {
    const msg = FrameType.decode(new Uint8Array(buffer))

    if (msg.textFrame) {
      return { type: 'text', text: msg.textFrame.text }
    }

    if (msg.audioRawFrame) {
      const audioBytes = msg.audioRawFrame.audio
      return {
        type: 'audio',
        audio: new Int16Array(audioBytes.buffer, audioBytes.byteOffset, audioBytes.byteLength / 2),
        sample_rate: msg.audioRawFrame.sampleRate,
      }
    }

    if (msg.transcriptionFrame) {
      return {
        type: 'transcription',
        text: msg.transcriptionFrame.text,
        language: msg.transcriptionFrame.language,
        isFinal: msg.transcriptionFrame.isFinal,
      }
    }

    if (msg.messageFrame) {
      return { type: 'message', text: msg.messageFrame.message }
    }

    return null
  } catch (e) {
    console.warn('Protobuf decode error:', e)
    return null
  }
}
