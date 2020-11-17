<template>
<div id="BookDetail">
    <Header />
<!--    <Ads />-->
    <b-container v-if="items.detailsItems.length == 1">
        <b-row class="mt-3">
            <b-col>
            当前路径: <a href="/">首页</a>--<a :href="'/book/'+ items.detailsItems[0].book_id">{{ items.detailsItems[0].book_title }}</a>--{{items.detailsItems[0].chart_title}}
            </b-col>
        </b-row>
        <b-row class="mt-3 mb-3">
            <b-col id="book-detail-title" >
            {{ items.detailsItems[0].chart_title }}
            </b-col>
        </b-row>

        <b-row class="mb-3">

            <b-col class="normal-center " cols="4" md="4"  v-if="items.detailsItems[0].before_sort_id == ''">
                <a>上一页</a>
            </b-col>
            <b-col class="normal-center" cols="4" md="4"  v-else>
                <a :href="'/book/'+ items.detailsItems[0].book_id +'/'+ items.detailsItems[0].before_sort_id">上一页</a>
            </b-col>


            <b-col class="normal-center" cols="4" md="4">
                <a :href="'/book/'+ items.detailsItems[0].book_id">返回目录</a>
            </b-col>

            <b-col class="normal-center" cols="4" md="4" v-if="items.detailsItems[0].next_sort_id == ''">
                <a>下一页</a>
            </b-col>
            <b-col class="normal-center" cols="4" md="4" v-else>
                <a :href="'/book/'+ items.detailsItems[0].book_id +'/'+ items.detailsItems[0].next_sort_id">下一页</a>
            </b-col>

        </b-row>

<!--        <b-row class="mt-3 mb-3">-->
<!--          <b-col id="chart_content" >-->
<!--            {{items.detailsItems[0].chart_content}}}-->
<!--          </b-col>-->
<!--        </b-row>-->

        <b-row>
            <b-col >
            <p id="content-text" v-html="items.detailsItems[0].chart_content"></p>
            </b-col>
        </b-row>

        <b-row class="mb-3">

            <b-col class="normal-center" cols="4" md="4"  v-if="items.detailsItems[0].before_sort_id == ''">
                <a>上一页</a>
            </b-col>
            <b-col class="normal-center" cols="4" md="4"  v-else>
                <a :href="'/book/'+ items.detailsItems[0].book_id +'/'+ items.detailsItems[0].before_sort_id">上一页</a>
            </b-col>


            <b-col class="normal-center" cols="4" md="4">
                <a :href="'/book/'+ items.detailsItems[0].book_id">返回目录</a>
            </b-col>

            <b-col class="normal-center" cols="4" md="4" v-if="items.detailsItems[0].next_sort_id == ''">
                <a>下一页</a>
            </b-col>
            <b-col class="normal-center" cols="4" md="4" v-else>
                <a :href="'/book/'+ items.detailsItems[0].book_id +'/'+ items.detailsItems[0].next_sort_id">下一页</a>
            </b-col>

        </b-row>
    </b-container>

    <b-container v-else>
        您要查询的图书章节不存在哦
    </b-container>
<!--    <AdsFooter />-->
    <Footer />
    </div>
    
</template>

<style lang="scss" scoped>
#book-detail-title{
    text-align: center;
    font-size: 28px;
}
#content-text{
    line-height: 40px;
    font-size: 18px;
}
</style>

<script>
import Header from "../components/Header.vue";
import Footer from "../components/Footer.vue";
// import AdsFooter from "../components/AdsFooter.vue";
// import Ads from "../components/Ads.vue";
// import { ref, reactive, onMounted } from "@vue/composition-api";
import { GetInfoPost } from "../apis/read.js";
import dateFormat from "@/utils/date";
import { replacebr } from "../utils/replaceBr.js"


export default {
    name:"BookDetail",
    components:{
        Header,
        Footer,
        // AdsFooter,
        // Ads
    },
    data() {
        return {
            dateFormat,
            replacebr,
            now_url: this.$route.path,
            detailPramas: {
                url: this.$route.path,
                key: ''
            },
            items: {
                detailsItems:[],
            },
        }
    },

   created () {
      GetInfoPost(this.detailPramas).then(resp =>{
          // console.log("In bookindex resp.data = ", resp.data);
          this.items.detailsItems = resp.data.data;
      });
  },
}
</script>