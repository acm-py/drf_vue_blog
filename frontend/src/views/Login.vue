<template>
  <BlogHeader/>
  <div id="grid">
    <div id="sign">
      <h3>登录账号</h3>
      <form>
        <div class="form-elem">
          <span>账号:</span>
          <input v-model="signName" type="text" placeholder="请输入用户名">
        </div>
        <div class="form-elem">
          <span>密码：</span>
          <input v-model="signPwd" type="password" placeholder="输入密码">
        </div>
        <div class="form-elem">
          <button v-on:click.prevent="sign">登录</button>
        </div>
      </form>
    </div>
  </div>
  <BlogFooter/>
</template>

<script>
import BlogHeader from "@/components/BlogHeader";
import BlogFooter from "@/components/BlogFooter";
import axios from "axios";
export default {
  name: "Login",
  components: {BlogFooter, BlogHeader},
  data: function () {
    return {
      signName: '',
      signPwd: '',
    }
  },
  methods: {
    sign() {
      const that = this;
      axios
          .post('/api/token/', {
            username: that.signName,
            password: that.signPwd,
          })
          .then(function (response) {
            const storage = localStorage;
            // Date.parse(...) 返回1970年1月1日UTC以来的毫秒数
            // Token 被设置为1天，因此这里加上86400000毫秒
            const expiredTime = Date.parse(response.headers.date) + 86400000
            // 设置localStorage
            storage.setItem('access.myblog', response.data.access);
            storage.setItem('refresh.myblog', response.data.refresh);
            storage.setItem('expiredTime.myblog', expiredTime);
            storage.setItem('username.myblog', that.signName);
            axios
                .get('/api/user/' + that.signName + '/')
                .then(function (response) {
                  storage.setItem('isSuperuser.myblog', response.data.is_superuser);

                  // 路由跳转
                  // 登录成功返回首页
                  that.$router.push({name: 'Home'});
                });
          })
    }
  },
}
</script>

<style scoped>
#grid {
        display: grid;
        grid-template-columns: 1fr;
    }
    #sign {
        text-align: center;
    }
    .form-elem {
        padding: 10px;
    }
    input {
        height: 25px;
        padding-left: 10px;
    }
    button {
        height: 35px;
        cursor: pointer;
        border: none;
        outline: none;
        background: gray;
        color: whitesmoke;
        border-radius: 5px;
        width: 60px;
    }

</style>