/**
 * 简单的状态管理（生产环境可替换为 Pinia）
 */

class Store {
    constructor() {
        this.state = {
            user: null,
            currentSession: null,
            scenarios: []
        }
    }

    // 设置用户信息
    setUser(user) {
        this.state.user = user
    }

    // 获取用户信息
    getUser() {
        return this.state.user
    }

    // 设置当前会话
    setCurrentSession(session) {
        this.state.currentSession = session
    }

    // 获取当前会话
    getCurrentSession() {
        return this.state.currentSession
    }

    // 设置场景列表
    setScenarios(scenarios) {
        this.state.scenarios = scenarios
    }

    // 获取场景列表
    getScenarios() {
        return this.state.scenarios
    }
}

// 创建全局 store 实例
const store = new Store()

export default store
