<script>
export default {
    onLaunch: function() {
        console.log('App Launch')
        // #ifdef MP-DINGTALK
        console.log('钉钉小程序环境')
        // #endif
    },
    onShow: function() {
        console.log('App Show')
    },
    onHide: function() {
        console.log('App Hide')
    }
}
</script>

<style>
/*每个页面公共css */
page {
    background-color: #f5f5f5;
}

.container {
    padding: 20rpx;
}
</style>
