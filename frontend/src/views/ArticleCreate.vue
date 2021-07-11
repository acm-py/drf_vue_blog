<template>
  <BlogHeader/>
  <div id="article-create">
    <h3>发表文章</h3>
    <form id="image_form">
      <div class="form-elem">
        <span>图片：</span>
        <input
               v-on:change="onFileChange"
               type="file"
               id="file"
               >
      </div>
    </form>
    <form>
      <div class="form-elem">
        <span>标题：</span>
        <input v-model="title" type="text" placeholder="输入标题">
      </div>

      <div class="form-elem">
        <span>分类：</span>
        <span
              v-for="category in categories"
              :key="category.id"
              >
          <!--样式也可以通过 :style 绑定-->
          <button
                  class="category-btn"
                  :style="categoryStyle(category)"
                  @click.prevent="chooseCategory(category)"
                  >
            {{category.title}}
          </button>
        </span>
      </div>

      <div class="form-elem">
        <span>标签：</span>
        <input v-model="tags" type="text" placeholder="输入标签，用逗号分隔">
      </div>

      <div class="form-elem">
        <span>正文：</span>
        <textarea v-model="body" placeholder="输入正文" rows="20" cols="80"></textarea>
      </div>

      <div class="form-elem">
        <button v-on:click.prevent="submit">提交</button>
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
export default {
  name: "ArticleCreate",
  components: {BlogFooter, BlogHeader},
  data: function (){
    return {
      // 文章标题
      title: '',
      body: '',
      categories: [],
      selectedCategory: null,
      tags: '',
      avatarID: null,
    }
  },
  mounted() {
    axios
      .get('/api/category')
      .then(response => this.categories = response.data)
  },
  methods: {
    onFileChange(e) {
        // 将文件二进制数据添加到提交数据中
        const file = e.target.files[0];
        let formData = new FormData();
        formData.append("content", file);

        // 略去鉴权和错误处理的部分
        axios
          .post('/api/avatar/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            'Authorization': 'Bearer ' + localStorage.getItem('access.myblog')
          }
        })
          .then( response => this.avatarID = response.data.id)
      },
    categoryStyle(category){
      if(this.selectedCategory !== null && category.id === this.selectedCategory.id){
        return {
          backgroundColor: 'black',
        }
      }
      return {
        backgroundColor: 'lightgray',
        color:'black',
      }
    },
    // 选取分类的方法
    chooseCategory(category) {
        // 如果点击已选取的分类，则将 selectedCategory 置空
        if (this.selectedCategory !== null && this.selectedCategory.id === category.id) {
          this.selectedCategory = null
        }
        // 如果没选中当前分类，则选中它
        else {
          this.selectedCategory = category;
        }
      },
    submit() {
        const that = this;
        // 前面封装的验证函数又用上了
        authorization()
          .then(function (response) {
            if (response[0]) {
              // 需要传给后端的数据字典
              let data = {
                title: that.title,
                body: that.body,
              };
              data.avatar_id = that.avatarID;
              // 添加分类
              if (that.selectedCategory) {
                data.category_id = that.selectedCategory.id
              }
              // 标签预处理
              data.tags = that.tags
                // 用逗号分隔标签
                .split(/[,，]/)
                // 剔除标签首尾空格
                .map(x => x.trim())
                // 剔除长度为零的无效标签
                .filter(x => x.charAt(0) !== '');

              // 将发表文章请求发送至接口
              // 成功后前往详情页面
              const token = localStorage.getItem('access.myblog');
              axios
                .post('/api/article/',
                  data,
                  {
                        headers: {Authorization: 'Bearer ' + token}
                    })
                .then(function (response) {
                    that.$router.push({name: 'ArticleDetail', params: {id: response.data.id}});

              })
            }
            else {
              alert('令牌过期，请重新登录。')
            }
          }
        )
  }
  }
}
</script>

<style scoped>
.category-btn {
    margin-right: 10px;
  }
  #article-create {
    text-align: center;
    font-size: large;
  }
  form {
    text-align: left;
    padding-left: 100px;
    padding-right: 10px;
  }
  .form-elem {
    padding: 10px;
  }
  input {
    height: 25px;
    padding-left: 10px;
    width: 50%;
  }
  button {
    height: 35px;
    cursor: pointer;
    border: none;
    outline: none;
    background: steelblue;
    color: whitesmoke;
    border-radius: 5px;
    width: 60px;
  }
</style>