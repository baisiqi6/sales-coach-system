<template>
    <view class="container">
        <view class="report-header">
            <text class="title">对练报告</text>
        </view>

        <view class="score-section">
            <view class="score-circle">
                <text class="score-text">--</text>
            </view>
            <text class="score-label">总分</text>
        </view>

        <view class="detail-section">
            <text class="section-title">详细评分</text>
            <text class="placeholder">报告详情（待实现）</text>
        </view>

        <view class="action-section">
            <button class="btn-primary" @tap="goBack">返回首页</button>
        </view>
    </view>
</template>

<script>
export default {
    methods: {
        goBack() {
            uni.switchTab({
                url: '/pages/index/index'
            })
        }
    }
}
</script>

<style scoped>
.container {
    padding: 30rpx;
}

.report-header {
    text-align: center;
    margin-bottom: 60rpx;
}

.title {
    font-size: 48rpx;
    font-weight: bold;
}

.score-section {
    text-align: center;
    margin-bottom: 60rpx;
}

.score-circle {
    width: 200rpx;
    height: 200rpx;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 30rpx;
}

.score-text {
    font-size: 72rpx;
    font-weight: bold;
    color: white;
}

.score-label {
    font-size: 28rpx;
    color: #666;
}

.detail-section {
    background: white;
    border-radius: 16rpx;
    padding: 30rpx;
    margin-bottom: 40rpx;
}

.section-title {
    font-size: 32rpx;
    font-weight: bold;
    display: block;
    margin-bottom: 20rpx;
}

.placeholder {
    font-size: 28rpx;
    color: #999;
}

.action-section {
    text-align: center;
}

.btn-primary {
    background: #007aff;
    color: white;
    border: none;
    border-radius: 8rpx;
    padding: 25rpx 60rpx;
    font-size: 28rpx;
}
</style>
