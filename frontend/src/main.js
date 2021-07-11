import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

router.beforeEach((to,from,next) =>{
  if(to.meta.title){
    document.title = to.meta.title
  }
  next();
})
// 重写一下append方法，确保undefinde 在path路径中被排除掉
URLSearchParams.prototype.appendIfExists = function (key, value){
    if (value !== null && value !== undefined){
        this.append(key, value)
    }
}

createApp(App).use(router).mount('#app')

