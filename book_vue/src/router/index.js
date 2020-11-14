import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import BookSearch from "../views/BookSearch.vue"
import HomeCate from "../views/HomeCate.vue"
import BookIndex from "../views/BookIndex.vue";

Vue.use(VueRouter)

const routes = [
  {
    // 网站首页
    path: '/',
    name: 'Home',
    component: Home
  },
    // 搜索结果页面
  {
    path: "/search",
    name: "BookSearch",
    component: BookSearch
  },

    // 网站分类页面
  {
    path: "/:book_cate",
    name: "HomeCate",
    component: HomeCate
  },
    // 图书首页
  {
    path: "/book/:book_id",
    name: "BookIndex",
    component: BookIndex,
  },

]

const router = new VueRouter({
  mode: "history",
  routes
})

export default router
