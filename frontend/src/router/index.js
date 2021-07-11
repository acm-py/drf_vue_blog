import {createWebHashHistory, createRouter} from "vue-router";
import Home from "@/views/Home";
import ArticleDetail from "@/views/ArticleDetail";
import Login from "@/views/Login";
import UserCenter from "@/views/UserCenter";
import ArticleCreate from "@/views/ArticleCreate";
import ArticleEdit from "@/views/ArticleEdit";

const routes = [
    {
        path: "/",
        name: "Home",
        component: Home,
        meta:{
            title: "阿炳的小站"
        }
    },
    {
        path: "/article/:id",
        name: "ArticleDetail",
        component: ArticleDetail,
        meta:{
            title: "文章详情"
        }
    },
    {
        path: "/login",
        name: "Login",
        component: Login,
        meta:{
            title: "登录页面"
        }
    },
    {
        path: "/user/:username",
        name: "UserCenter",
        component: UserCenter,
        meta:{
            title: "用户中心"
        }
    },
    {
        path: "/article/create",
        name: "ArticleCreate",
        component: ArticleCreate,
        meta:{
            title: "文章发布"
        }
    },
    {
        path: "/article/edit/:id",
        name: "ArticleEdit",
        component: ArticleEdit,
        meta:{
            title: "文章编辑"
        }
    },
];

const router = createRouter({
    history: createWebHashHistory(),
    routes
});
export default router;