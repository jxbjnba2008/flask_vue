<template>
<div id="HomeCate">
    <Header />

    <b-container class="mt-4 mb-2" v-if="items.newestItems.length > 0">
        <b-row>
            <b-col cols="12" md="7">
                    <div>
                        <b-nav tabs>
                        <b-nav-item active><a style="font-size:16px; color:#E00000">最新更新的小说</a></b-nav-item>
                        </b-nav>
                    </div>
                    <table role="table" aria-busy="false" aria-colcount="3" class="table b-table" style="table-layout:fixed;"><!----><!---->
                        <thead role="rowgroup" class=""><!---->
                        <tr role="row" class="">
                            <th role="columnheader" scope="col" aria-colindex="1" class="" style="width:160px;font-family: verdana,arial,sans-serif; font-size:13px; color:	#686868; border-width: 2px; border-color: #dedede;background-color: ;border-style: none none solid none;"><div>小说</div></th>
                            <th role="columnheader" scope="col" aria-colindex="2" class="" style="width:250px;font-family: verdana,arial,sans-serif; font-size:13px; color:	#686868; border-width: 2px; border-color: #dedede;background-color: ;border-style: none none solid none;"><div>最新章节</div></th>
                            <th role="columnheader" scope="col" aria-colindex="3" class="" style="width:110px;font-family: verdana,arial,sans-serif; font-size:13px; color:	#686868; border-width: 2px; border-color: #dedede;background-color: ;border-style: none none solid none;"><div>作者</div></th>
                            <th role="columnheader" scope="col" aria-colindex="4" class="" style="width:140px;font-family: verdana,arial,sans-serif; font-size:13px; color:	#686868; border-width: 2px; border-color: #dedede;background-color: ;border-style: none none solid none;"><div>更新时间</div></th>
                        </tr>
                        </thead>
                        <tbody role="rowgroup"><!---->
                            <tr role="row" v-for="item in items.newestItems" :key="item.book_id">
                            <td aria-colindex="1" role="cell" class="" style="white-space:nowrap;overflow:hidden;text-overflow: ellipsis;font-family: verdana,arial,sans-serif; font-size:10px; border-width: 1.5px;background-color: #ffffff;"><a :href="'/book/'+ item.book_id" style="font-size:12px; color:#F08080">{{ item.book_title }}</a></td>
                            <td aria-colindex="2" role="cell" class="" style="white-space:nowrap;overflow:hidden;text-overflow: ellipsis;font-family: verdana,arial,sans-serif; font-size:10px; border-width: 1.5px;background-color: #ffffff;"><a :href="item.new_chart_url" style="font-size: 12px; color:#686868">{{ item.new_chart }}</a></td>
                            <td aria-colindex="3" role="cell" class="" style="white-space:nowrap;overflow:hidden;text-overflow: ellipsis;font-family: verdana,arial,sans-serif; font-size:10px; border-width: 1.5px;background-color: #ffffff;"><a style="font-size: 12px; color:#888888">{{ item.author }}</a></td>
                            <td aria-colindex="4" role="cell" class="" style="white-space:nowrap;overflow:hidden;text-overflow: ellipsis;font-family: verdana,arial,sans-serif; font-size:10px; border-width: 1.5px;background-color: #ffffff;"><a style="font-size: 12px; color:#686868">{{ dateFormat(item.update_time) }}</a></td></tr>

                        </tbody><!---->
                    </table>
            </b-col>

            <b-col cols="12" md="4">
                        <b-nav tabs style="margin-left:50px; width:350px">
                        <b-nav-item active><a style="font-size:16px; color:#E00000">人气小说</a></b-nav-item>
                        </b-nav>

                    <table role="table" aria-busy="false" aria-colcount="3" class="table b-table" style="table-layout:fixed; margin-left:50px"><!----><!---->
                        <thead role="rowgroup" class=""><!---->
                        <tr role="row" class="">
                            <th role="columnheader" scope="col" aria-colindex="1" class="" style="width:160px;font-family: verdana,arial,sans-serif; font-size:13px; color:	#686868; border-width: 2px; border-color: #dedede;background-color: ;border-style: none none solid none;"><div>小说</div></th>
                            <th role="columnheader" scope="col" aria-colindex="2" class="" style="width:160px;font-family: verdana,arial,sans-serif; font-size:13px; color:	#686868; border-width: 2px; border-color: #dedede;background-color: ;border-style: none none solid none;"><div>作者</div></th>
                            </tr>
                        </thead>
                        <tbody role="rowgroup"><!---->
                            <tr role="row" v-for="item in items.mostItems" :key="item.book_id">
                            <td aria-colindex="1" role="cell" class="" style="white-space:nowrap;overflow:hidden;text-overflow: ellipsis;font-family: verdana,arial,sans-serif; font-size:10px; border-width: 1.5px;background-color: #ffffff;"><a :href="'/book_'+ item.book_id" style="font-size: 12px;color:#F08080">{{ item.book_title }}</a></td>
                            <td aria-colindex="2" role="cell" class="" style="white-space:nowrap;overflow:hidden;text-overflow: ellipsis;font-family: verdana,arial,sans-serif; font-size:10px; border-width: 1.5px;background-color: #ffffff;"><a style="font-size: 12px;color:#888888">{{ item.author }}</a></td>
                            
                            </tr>
                            
                        </tbody><!---->
                    </table>
            </b-col>
        </b-row>
    </b-container>
    <!-- <b-container class="mt-4" v-else>
                哦哦，您要查看的图书不存在
    </b-container> -->

    <Footer />
</div>
</template>


<script>
import Header from "../components/Header.vue";
import Footer from "../components/Footer.vue";
//import AdsFooter from "../components/AdsFooter.vue";
//import Ads from "../components/Ads.vue";
//import { ref, reactive, onMounted } from "@vue/composition-api";
import { GetInfoPost } from "../apis/read.js";
import dateFormat from "../utils/date.js";

export default {
    name:"HomeCate",
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
            newstParams: {
                url: this.$route.path,
                key: 'newest'
            },
            mostParams:{
                url: this.$route.path,
                key: 'most'
            },
            items: {
                newestItems:[],
                mostItems:[]
            },
            //titlePramas: {
            //    url: '/title',
            //    key: this.$route.path.replace(/\//g,'')
            //},
        }
    },

    created () {
        //this.now_url = this.$route.path;
        console.log("now_url3 = ", this.now_url);

        GetInfoPost(this.newstParams).then(resp => {
            console.log("news : resp.data.data", resp.data.data);
            this.items.newestItems = resp.data.data
        });

        GetInfoPost(this.mostParams).then(resp => {
            console.log("most : resp.data.data", resp.data.data);
            this.items.mostItems = resp.data.data
        });
    },

    //mounted () {
    //    console.log("in hhhhhhhhhhcccccccccccccc= ", this.$route.path.replace(/\//g,''));

    //    GetInfoPost(this.titlePramas).then(resp => {
    //        console.log("In Home title = ", resp.data.data);
    //        document.title = resp.data.data[0];
    //        document.querySelector('meta[name="keywords"]').setAttribute("content", resp.data.data[1]);
    //        document.querySelector('meta[name="description"]').setAttribute("content", resp.data.data[2]);
    //    });
    //},
}

</script>

<style lang="scss" scoped>

</style>