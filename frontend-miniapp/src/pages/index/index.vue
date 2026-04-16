<template>
    <view class="container">
        <view class="header">
            <text class="title">智能销售对练系统</text>
            <text class="subtitle">请选择对练场景</text>
        </view>

        <view class="scenario-list">
            <view
                class="scenario-item"
                v-for="(item, index) in scenarios"
                :key="index"
                @tap="selectScenario(item)"
            >
                <view class="scenario-icon">{{ item.icon }}</view>
                <view class="scenario-info">
                    <text class="scenario-name">{{ item.name }}</text>
                    <text class="scenario-desc">{{ item.description }}</text>
                </view>
            </view>
        </view>

        <view class="test-section">
            <button class="test-btn" @tap="testBackend">测试后端联通</button>
            <text class="test-result" v-if="testResult">{{ testResult }}</text>
        </view>
    </view>
</template>

<script>
import { getPersonas, healthCheck } from '@/src/api/index.js'

export default {
    data() {
        return {
            scenarios: [],
            testResult: ''
        }
    },
    onShow() {
        this.loadScenarios()
    },
    methods: {
        async loadScenarios() {
            try {
                const personas = await getPersonas()
                this.scenarios = personas.map(p => ({
                    id: p.id || p.uuid,
                    name: p.name,
                    description: p.scenario_desc,
                    icon: '🎯'
                }))
            } catch (err) {
                // 后端未就绪时使用默认场景
                this.scenarios = [
                    { id: 1, name: '价格异议处理', description: '练习应对客户对价格的抗拒', icon: '💰' },
                    { id: 2, name: '产品介绍', description: '向客户清晰介绍产品优势', icon: '📦' },
                    { id: 3, name: '成交促成', description: '在合适时机推进成交', icon: '🎯' }
                ]
            }
        },
        selectScenario(scenario) {
            uni.navigateTo({
                url: '/pages/chat/chat?scenarioId=' + scenario.id
            })
        },
        async testBackend() {
            this.testResult = '测试中...'
            try {
                await healthCheck()
                this.testResult = '后端联通成功！'
            } catch (error) {
                this.testResult = '后端联通失败: ' + error.message
            }
        }
    }
}
</script>

<style scoped>
.container {
    padding: 30rpx;
}

.header {
    text-align: center;
    margin-bottom: 60rpx;
}

.title {
    font-size: 48rpx;
    font-weight: bold;
    display: block;
    margin-bottom: 20rpx;
}

.subtitle {
    font-size: 28rpx;
    color: #999;
}

.scenario-list {
    margin-bottom: 60rpx;
}

.scenario-item {
    background: white;
    border-radius: 16rpx;
    padding: 30rpx;
    margin-bottom: 20rpx;
    display: flex;
    align-items: center;
    box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.08);
}

.scenario-icon {
    font-size: 80rpx;
    margin-right: 30rpx;
}

.scenario-info {
    flex: 1;
}

.scenario-name {
    font-size: 32rpx;
    font-weight: bold;
    display: block;
    margin-bottom: 10rpx;
}

.scenario-desc {
    font-size: 24rpx;
    color: #666;
}

.test-section {
    text-align: center;
}

.test-btn {
    background: #007aff;
    color: white;
    border: none;
    border-radius: 8rpx;
    padding: 20rpx 40rpx;
    font-size: 28rpx;
}

.test-result {
    display: block;
    margin-top: 20rpx;
    font-size: 24rpx;
    color: #666;
}
</style>
