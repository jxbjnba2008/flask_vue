<template>
    <div id="BookIndex">
        <Header />
            <b-container class="mt-4" v-if="items.allCapItems.length > 1">
                <b-row class="mb-3" align-h="center">
                    <b-col clos="12" md="3"> <!-- 放图片 -->
                        <b-img thumbnail fluid class="img-rounded" style="width:100%; margin-left:0" :src="items.indexItems[0].img" alt="Image 1"></b-img>

                    </b-col>

                    <b-col  clos="12" md="8" > <!-- 放图书信息 -->

                        <b-jumbotron header-level="0" class="pt-3">
                            <template v-slot:header class="mt-1 mb-3" style="font-size:8px; color:#f08080">{{ items.indexItems[0].book_title }}</template>

                            <div class="mb-3">作者：{{ items.indexItems[0].author }}</div>
                            <div class="mb-3">最新章节：{{ items.indexItems[0].new_chart }}</div>
                            <div class="mb-3">最新更新时间：{{ dateFormat(items.indexItems[0].update_time) }}</div>
                            <div class="mb-3">小说简介：</div>
<!--                            <hr class="my-4">-->
                            <p v-text="items.indexItems[0].abstract">
                            </p>

                            <b-button pill variant="primary" class="left"  style="float:left; margin-left:5px" :href="'/book/'+items.indexItems[0].book_id+'/'+ items.allCapItems[0].chart_id">开始阅读</b-button>
                            <b-button pill variant="success" class="right" style="float:right; margin-right:5px"  href="#">加入收藏夹</b-button>

                        </b-jumbotron>

                    </b-col>
                </b-row>

                <b-row class="mb-2">
                    <b-col class="normal-center"><h4>最近更新的20章图书</h4></b-col> 
                </b-row>
                <b-row class="mb-4">
                    <b-col clos="12" md="4" v-for="item in items.newest20CapItems" :key="item.chart_id"><a :href="'/book/'+item.book_id+'/'+item.chart_id " style="font-size:12px; color:#F08080">{{ item.chart_title }}</a></b-col>
                </b-row>


                <b-row class="mb-2 ">
                    <b-col class="normal-center"><h4>所有章节的内容</h4></b-col>
                </b-row>
                <b-row class="mb-2">
                    <b-col clos="12" md="4" v-for="item in items.allCapItems" :key="item.chart_id"><a :href="'/book/'+item.book_id+'/'+item.chart_id " style="font-size:12px; color:#F08080">{{ item.chart_title }}</a></b-col>
                    
                </b-row>

               
            </b-container>
            <!-- <b-container class="mt-4" v-else>
                        哦哦，您要查看的图书不存在
            </b-container> -->

       <Footer />
    </div>
</template>

<style lang="scss" scoped>

</style>

<script>
import Header from "../components/Header.vue";
import Footer from "../components/Footer.vue";
//import AdsFooter from "../components/AdsFooter.vue";
//import Ads from "../components/Ads.vue";
import { GetInfoPost } from "../apis/read.js";
//import { reactive, ref, onMounted, onBeforeMount } from "@vue/composition-api";
import dateFormat from "../utils/date.js";
// import yuedu from "../components/shujia.vue";
// import 的时候什么时候没有{}： export default 出现在最后一行的时候，就没有{}
// 什么时候有{}: export 很多个fanctions的时候，就有{}

export default {
    name:'BookIndex',
    components:{
        Header,
        Footer,
        //AdsFooter,
        //Ads
    },
    data() {
        return {
            dateFormat,
            now_url: this.$route.path,
            indexParams: {
                url: this.$route.path,
                key: 'index'
            },
            cap20Params:{
                url: this.$route.path,
                key: 'cap20'
            },
            capAllParams:{
                url: this.$route.path,
                key: 'all'
            },
            items: {
                indexItems:[],
                allCapItems:[],
                newest20CapItems:[],
            },
            //titlePramas: {
            //    url: '/title',
            //    key: this.$route.path.replace(/\//g,'')
            //},
        }
    },

     created () {
        GetInfoPost(this.indexParams).then(resp =>{
            // console.log("In indexItems resp.data = ", resp.data);
            this.items.indexItems = resp.data.data;
        });

        GetInfoPost(this.capAllParams).then(resp =>{
            // console.log("In allCapItems resp.data = ", resp.data.data);
            this.items.allCapItems = resp.data.data

        });

        GetInfoPost(this.cap20Params).then(resp =>{
            // console.log("In newest20CapItems resp.data = ", resp.data.data);
            this.items.newest20CapItems = resp.data.data
        });
    }
}

</script>