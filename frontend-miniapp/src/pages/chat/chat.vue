<template>
    <view class="container">
        <view class="chat-header">
            <text class="scenario-title">{{ scenarioTitle }}</text>
            <text class="status" :class="{ active: isConnected }">
                {{ isConnected ? '对练中' : '连接中...' }}
            </text>
        </view>

        <scroll-view
            class="chat-area"
            scroll-y
            :scroll-into-view="scrollTarget"
            :scroll-with-animation="true"
        >
            <view
                v-for="(msg, idx) in messages"
                :key="idx"
                :id="'msg-' + idx"
                :class="['message', msg.role === 'SALE' ? 'user-msg' : 'bot-msg']"
            >
                <text class="msg-text">{{ msg.content }}</text>
            </view>
            <view id="msg-bottom" style="height: 20rpx;"></view>
        </scroll-view>

        <view class="control-area">
            <view class="record-btn-wrapper">
                <button
                    class="record-btn"
                    :class="{ recording: isRecording }"
                    @touchstart.prevent="onRecordStart"
                    @touchend.prevent="onRecordEnd"
                    @mousedown.prevent="onRecordStart"
                    @mouseup.prevent="onRecordEnd"
                >
                    {{ isRecording ? '松开结束' : '按住说话' }}
                </button>
            </view>
            <button class="end-btn" @tap="endPractice">结束对练</button>
        </view>
    </view>
</template>

<script>
import { PipecatWebSocket } from '@/src/utils/websocket.js'
import { AudioManager } from '@/src/utils/audio.js'
import { createSession, endSession } from '@/src/api/index.js'

const WS_BASE = 'ws://192.168.108.55:8000/api/v1'

export default {
    data() {
        return {
            scenarioId: null,
            scenarioTitle: '销售对练',
            sessionUuid: null,
            messages: [],       // { role: 'SALE'|'AI', content: string, finished?: boolean }
            isRecording: false,
            isConnected: false,
            scrollTarget: '',
            ws: null,
            audio: null,
        }
    },

    async onLoad(options) {
        this.scenarioId = options.scenarioId
        this.audio = new AudioManager()

        try {
            // 1. 创建会话
            const session = await createSession(1, this.scenarioId) // MVP: hardcoded user_id=1
            this.sessionUuid = session.uuid
            // 2. 连接 WebSocket
            this.connectWebSocket()
        } catch (err) {
            uni.showToast({ title: '创建会话失败', icon: 'none' })
            console.error('创建会话失败:', err)
        }
    },

    onUnload() {
        this.disconnect()
    },

    methods: {
        connectWebSocket() {
            const url = `${WS_BASE}/sessions/${this.sessionUuid}/ws`
            this.ws = new PipecatWebSocket(url)

            this.ws.onConnected = () => {
                this.isConnected = true
            }

            this.ws.onUserTranscript = (text, isFinal) => {
                if (!text) return
                if (isFinal) {
                    // 最终转录结果，添加为新的用户消息
                    this.messages.push({ role: 'SALE', content: text })
                } else {
                    // 中间转录结果，更新最后一条用户消息或追加
                    const lastMsg = this.messages[this.messages.length - 1]
                    if (lastMsg && lastMsg.role === 'SALE' && !lastMsg.finished) {
                        lastMsg.content = text
                    } else {
                        this.messages.push({ role: 'SALE', content: text, finished: false })
                    }
                }
                this.scrollToBottom()
            }

            this.ws.onBotText = (text) => {
                if (!text) return
                // 流式追加到 AI 消息
                const lastMsg = this.messages[this.messages.length - 1]
                if (lastMsg && lastMsg.role === 'AI' && !lastMsg.finished) {
                    lastMsg.content += text
                } else {
                    this.messages.push({ role: 'AI', content: text, finished: false })
                }
                this.scrollToBottom()
            }

            this.ws.onBotAudio = (pcmData, sampleRate) => {
                if (this.audio) {
                    this.audio.playAudioH5(pcmData, sampleRate)
                }
            }

            this.ws.onDisconnected = () => {
                this.isConnected = false
                // 标记最后一条 AI 消息为完成
                const lastMsg = this.messages[this.messages.length - 1]
                if (lastMsg && lastMsg.role === 'AI') {
                    lastMsg.finished = true
                }
            }

            this.ws.onError = (err) => {
                console.error('WebSocket 错误:', err)
                uni.showToast({ title: '连接异常', icon: 'none' })
            }

            // 录音回调 → 发送音频帧
            this.audio.onAudioChunk = (pcmInt16Array) => {
                if (this.ws && this.isConnected) {
                    this.ws.sendAudio(pcmInt16Array)
                }
            }

            this.ws.connect()
        },

        onRecordStart() {
            if (!this.isConnected) return
            this.isRecording = true
            this.audio.startRecordingH5()
        },

        onRecordEnd() {
            this.isRecording = false
            this.audio.stopRecordingH5()
        },

        scrollToBottom() {
            this.$nextTick(() => {
                this.scrollTarget = 'msg-bottom'
            })
        },

        async endPractice() {
            const confirmed = await new Promise((resolve) => {
                uni.showModal({
                    title: '提示',
                    content: '确定要结束对练吗？',
                    success: (res) => resolve(res.confirm),
                })
            })
            if (!confirmed) return

            this.disconnect()

            if (this.sessionUuid) {
                try {
                    await endSession(this.sessionUuid)
                } catch {}
            }

            uni.navigateTo({ url: '/pages/report/report' })
        },

        disconnect() {
            if (this.audio) {
                this.audio.stopRecordingH5()
                this.audio.stopAllPlayback()
            }
            if (this.ws) this.ws.close()
            this.isConnected = false
        },
    },
}
</script>

<style scoped>
.container {
    height: 100vh;
    display: flex;
    flex-direction: column;
}

.chat-header {
    padding: 30rpx;
    background: white;
    border-bottom: 1rpx solid #eee;
    text-align: center;
}

.scenario-title {
    font-size: 32rpx;
    font-weight: bold;
    display: block;
    margin-bottom: 10rpx;
}

.status {
    font-size: 24rpx;
    color: #999;
}

.status.active {
    color: #52c41a;
}

.chat-area {
    flex: 1;
    padding: 30rpx;
    overflow-y: auto;
}

.message {
    margin-bottom: 24rpx;
    max-width: 75%;
    padding: 20rpx 28rpx;
    border-radius: 16rpx;
    word-break: break-all;
}

.user-msg {
    background: #007aff;
    color: white;
    margin-left: auto;
    border-bottom-right-radius: 4rpx;
}

.bot-msg {
    background: #f0f0f0;
    color: #333;
    margin-right: auto;
    border-bottom-left-radius: 4rpx;
}

.msg-text {
    font-size: 28rpx;
    line-height: 1.6;
}

.control-area {
    padding: 30rpx;
    background: white;
    border-top: 1rpx solid #eee;
}

.record-btn-wrapper {
    margin-bottom: 20rpx;
}

.record-btn {
    background: #007aff;
    color: white;
    border: none;
    border-radius: 8rpx;
    padding: 30rpx;
    font-size: 32rpx;
    width: 100%;
}

.record-btn.recording {
    background: #ff9500;
}

.end-btn {
    background: #ff3b30;
    color: white;
    border: none;
    border-radius: 8rpx;
    padding: 25rpx;
    font-size: 28rpx;
    width: 100%;
}
</style>
