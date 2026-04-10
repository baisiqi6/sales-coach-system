/**
 * API 请求封装
 */

// 后端 API 基础地址
// 开发环境使用局域网 IP，小程序无法访问 localhost
// 生产环境需要替换为正式服务器地址
const BASE_URL = 'http://192.168.108.55:8000/api/v1'

/**
 * 通用请求方法
 */
function request(options) {
    return new Promise((resolve, reject) => {
        uni.request({
            url: BASE_URL + options.url,
            method: options.method || 'GET',
            data: options.data || {},
            header: {
                'Content-Type': 'application/json',
                ...options.header
            },
            success: (res) => {
                if (res.statusCode >= 200 && res.statusCode < 300) {
                    resolve(res.data)
                } else {
                    reject(new Error(`请求失败: ${res.statusCode}`))
                }
            },
            fail: (err) => {
                reject(err)
            }
        })
    })
}

/**
 * 健康检查接口
 */
export function healthCheck() {
    return request({
        url: '/health',
        method: 'GET'
    })
}

/**
 * Ping 接口
 */
export function ping() {
    return request({
        url: '/ping',
        method: 'GET'
    })
}

// 导出基础配置
export { BASE_URL }
