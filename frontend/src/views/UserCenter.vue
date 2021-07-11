<template>
  <BlogHeader ref="header"/>
  <div id="user-center">
    <h3>更新资料信息</h3>
    <form>
      <div class="form-elem">
        <span>用户名：</span>
        <input v-model="username" type="text" placeholder="输入用户名">
      </div>
      <div class="form-elem">
        <span>新密码：</span>
        <input v-model="password" type="text" placeholder="输入密码">
      </div>
      <div class="form-elem">
        <button v-on:click.prevent="changeInfo">更新</button>
      </div>
    </form>
  </div>
  <BlogFooter/>
</template>

<script>
import BlogHeader from "@/components/BlogHeader";
import BlogFooter from "@/components/BlogFooter";
import axios from "axios";
import authorization from "@/utils/authorization";

const storage = localStorage;

export default {
  name: "UserCenter",
  components: {BlogFooter, BlogHeader},
  data: function (){
    return {
      username: '',
      password: '',
      token: '',
    }
  },
  mounted() {
    this.username = storage.getItem('username.myblog');
  },
  methods: {
    changeInfo(){
      const that = this;
      // 验证登录状态
      authorization()
        .then(function (response){
          // 检查登录装填
          // 若登录已过期则不执行过后序操作
          if (!response[0]){
            alert('登录已经过期');
            return
          }
          console.log('change info start');
          // 密码不小于6位
          if(that.password.length > 0 && that.password.len < 6 ){
            alert('密码太短');
            return
          }
          // 旧的 username 用于向接口发送请求
          const oldName = storage.getItem('username.myblog');
          // 获取已填写的表单
          let data = {};
          if (that.username !== ''){
            data.username = that.username;
          }
          if (that.password !== ''){
            data.password = that.passowrd;
          }
          // 获取令牌
          that.token = storage.getItem('access.myblog');
          // 发送更新请求数据到接口
          axios
            .patch(
                '/api/user/' + oldName + '/',
                data,
                {
                  headers: {Authorization: 'Bearer ' + that.token}
                }
            )
            .then(function (response){
              const name = response.data.username;
              storage.setItem('username.myblog', name);
              that.$router.push({name: 'UserCenter', params: {username: name}});
              that.$refs.headers.refresh();
            })
        });
    }
  },
}
</script>

<style scoped>
  #user-center {
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
    width: 200px;
    }
</style>