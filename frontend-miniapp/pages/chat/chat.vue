<template>
    <view class="container">
        <view class="chat-header">
            <text class="scenario-title">{{ scenarioTitle }}</text>
            <text class="status">对练中</text>
        </view>

        <view class="chat-area">
            <text class="placeholder">对话区域（待实现）</text>
        </view>

        <view class="control-area">
            <button class="record-btn" @tap="startRecord">按住说话</button>
            <button class="end-btn" @tap="endPractice">结束对练</button>
        </view>
    </view>
</template>

<script>
export default {
    data() {
        return {
            scenarioId: null,
            scenarioTitle: '销售对练'
        }
    },
    onLoad(options) {
        this.scenarioId = options.scenarioId
        console.log('场景ID:', this.scenarioId)
    },
    methods: {
        startRecord() {
            uni.showToast({
                title: '录音功能待实现',
                icon: 'none'
            })
        },
        endPractice() {
            uni.showModal({
                title: '提示',
                content: '确定要结束对练吗？',
                success: (res) => {
                    if (res.confirm) {
                        uni.navigateTo({
                            url: '/pages/report/report'
                        })
                    }
                }
            })
        }
    }
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
    color: #52c41a;
}

.chat-area {
    flex: 1;
    padding: 30rpx;
    display: flex;
    align-items: center;
    justify-content: center;
}

.placeholder {
    font-size: 28rpx;
    color: #999;
}

.control-area {
    padding: 30rpx;
    background: white;
    border-top: 1rpx solid #eee;
}

.record-btn {
    background: #007aff;
    color: white;
    border: none;
    border-radius: 8rpx;
    padding: 30rpx;
    font-size: 32rpx;
    margin-bottom: 20rpx;
}

.end-btn {
    background: #ff3b30;
    color: white;
    border: none;
    border-radius: 8rpx;
    padding: 25rpx;
    font-size: 28rpx;
}
</style>
