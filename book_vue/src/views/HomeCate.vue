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
                            <th role="columnheader" scope="col" aria-colindex="1" class="" style="width:160px;font-family: verdana,arial,sans-serif; font-size:13px; color:	#686868; border-width: 2px; border-color: #dedede;border-style: none none solid none;"><div>小说</div></th>
                            <th role="columnheader" scope="col" aria-colindex="2" class="" style="width:250px;font-family: verdana,arial,sans-serif; font-size:13px; color:	#686868; border-width: 2px; border-color: #dedede;border-style: none none solid none;"><div>最新章节</div></th>
                            <th role="columnheader" scope="col" aria-colindex="3" class="" style="width:110px;font-family: verdana,arial,sans-serif; font-size:13px; color:	#686868; border-width: 2px; border-color: #dedede;border-style: none none solid none;"><div>作者</div></th>
                            <th role="columnheader" scope="col" aria-colindex="4" class="" style="width:140px;font-family: verdana,arial,sans-serif; font-size:13px; color:	#686868; border-width: 2px; border-color: #dedede;border-style: none none solid none;"><div>更新时间</div></th>
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
                    <div class="center">
                        <ul class="pagination">
                            <li :class="pageNo<=1?'disabled':''" @click="prePage()">
                                <a aria-label="Previous" href="#">
                                    <span aria-hidden="true">上一页</span>
                                </a>
                            </li>
                            <li>
                                <a>
                                  第{{pageNo}}页
                                </a>
                            </li>

                            <li :class="pageNo>=pageTotal?'disabled':''" @click="nextPage()">
                                <a aria-label="Next" href="#">
                                  <span aria-hidden="true">下一页</span>
                                </a>
                            </li>
                        </ul>
                    </div>

<!--                    <div class="pager" id="pager">-->
<!--                    <span class="form-inline">-->
<!--                        <label>-->
<!--                        <select class="form-control" v-model="pageSize" v-on:change="showPage(pageNo,$event,true)" number>-->
<!--                            <option value="10">10</option>-->
<!--                            <option value="20">20</option>-->
<!--                            <option value="30">30</option>-->
<!--                            <option value="40">40</option>-->
<!--                        </select>-->
<!--                        </label>-->
<!--                    </span>-->
<!--                    <span v-for="item in pageTotal+1">-->
<!--                        <span v-if="item===1" class="btn btn-default" v-on:click="showPage(1,$event)" :class="{'disabled':fDisabled}">-->
<!--                            首页-->
<!--                        </span>-->
<!--                        <span v-if="item===1" class="btn btn-default" v-on:click="showPage(pageNo-1,$event)" :class="{'disabled':fDisabled}">-->
<!--                            上一页-->
<!--                        </span>-->
<!--                        <span v-if="item===1" class="btn btn-default" v-on:click="showPage(item,$event)">-->
<!--                            {{item}}-->
<!--                        </span>-->
<!--                        <span v-if="item===1&&item<showPagesStart-1" class="btn btn-default disabled">-->
<!--                            ...-->
<!--                        </span>-->
<!--                        <span v-if="item>1&&item<=pageTotal-1&&item>=showPagesStart&&item<=showPageEnd&&item<=pageTotal" class="btn btn-default" v-on:click="showPage(item,$event)">-->
<!--                            {{item}}-->
<!--                        </span>-->
<!--                        <span v-if="item===pageTotal&&item>showPageEnd+1" class="btn btn-default disabled">-->
<!--                            ...-->
<!--                        </span>-->
<!--                        <span v-if="item===pageTotal" class="btn btn-default" v-on:click="showPage(item,$event)"  >-->
<!--                            {{item}}-->
<!--                        </span>-->
<!--                        <span v-if="item===pageTotal" class="btn btn-default" v-on:click="showPage(pageNo+1,$event)" :class="{'disabled':lDisabled}">-->
<!--                            下一页-->
<!--                        </span>-->
<!--                        <span v-if="item===pageTotal" class="btn btn-default" v-on:click="showPage(pageTotal,$event)" :class="{'disabled':lDisabled}">-->
<!--                            尾页-->
<!--                        </span>-->
<!--                    </span>-->
<!--                    <span>{{pageNo}}/{{pageTotal}}</span>-->
<!--                </div>-->

            </b-col>

            <b-col cols="12" md="4">
                        <b-nav tabs style="margin-left:50px; width:350px">
                        <b-nav-item active><a style="font-size:16px; color:#E00000">人气小说</a></b-nav-item>
                        </b-nav>

                    <table role="table" aria-busy="false" aria-colcount="3" class="table b-table" style="table-layout:fixed; margin-left:50px"><!----><!---->
                        <thead role="rowgroup" class=""><!---->
                        <tr role="row" class="">
                            <th role="columnheader" scope="col" aria-colindex="1" class="" style="width:160px;font-family: verdana,arial,sans-serif; font-size:13px; color:	#686868; border-width: 2px; border-color: #dedede;border-style: none none solid none;"><div>小说</div></th>
                            <th role="columnheader" scope="col" aria-colindex="2" class="" style="width:160px;font-family: verdana,arial,sans-serif; font-size:13px; color:	#686868; border-width: 2px; border-color: #dedede;border-style: none none solid none;"><div>作者</div></th>
                            </tr>
                        </thead>
                        <tbody role="rowgroup"><!---->
                            <tr role="row" v-for="item in items.mostItems" :key="item.book_id">
                            <td aria-colindex="1" role="cell" class="" style="white-space:nowrap;overflow:hidden;text-overflow: ellipsis;font-family: verdana,arial,sans-serif; font-size:10px; border-width: 1.5px;background-color: #ffffff;"><a :href="'/book/'+ item.book_id" style="font-size: 12px;color:#F08080">{{ item.book_title }}</a></td>
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

<style>
    ul.pagination {
        display: inline-block;
        padding: 0;
        margin: 0;
    }

    ul.pagination li {display: inline;}

    ul.pagination li a {
        color: black;
        float: left;
        padding: 8px 16px;
        text-decoration: none;
        border-radius: 5px;
        transition: background-color .3s;
        border: 1px solid #FA8072;
        margin: 0 4px;
    }

    ul.pagination li a.active {
        background-color: #FA8072;
        color: white;
        border-radius: 5px;
    }

    ul.pagination li a:hover:not(.active) {background-color: #ddd;}
    div.center {text-align: center;}
</style>

<script>
import Header from "../components/Header.vue";
import Footer from "../components/Footer.vue";
//import AdsFooter from "../components/AdsFooter.vue";
//import Ads from "../components/Ads.vue";
//import { ref, reactive, onMounted } from "@vue/composition-api";
import { GetInfoPost } from "../apis/read.js";
import { GetPagePost } from "../apis/read.js";
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
            fDisabled:false,
            lDisabled:false,
            pageNo: 1, //当前页码
            pageTotal: 5, //总页数
            rows: 200, //总条数
            pageSize: 20, //每页条数
            //显示分页按钮数
            showPages: 11,
            //开始显示的分页按钮
            showPagesStart: 1,
            //结束显示的分页按钮
            showPageEnd: 100,

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

        // GetInfoPost(this.newstParams).then(resp => {
        //     console.log("news : resp.data.data", resp.data.data);
        //     this.items.newestItems = resp.data.data
        // });
        this.getData()
        GetInfoPost(this.mostParams).then(resp => {
            console.log("most : resp.data.data", resp.data.data);
            this.items.mostItems = resp.data.data
        });
    },
    // mounted(){
    //     this.showPage(this.pageNo, null, true);
    // },
    methods:{
        showPage(pageIndex, $event, forceRefresh){

            if (pageIndex > 0) {
                if (pageIndex > this.pageTotal) {
                    pageIndex = this.pageTotal;
                }
                //判断数据是否需要更新
                var currentPageCount = Math.ceil(this.rows / this.pageSize);
                if (currentPageCount !== this.pageTotal) {
                    pageIndex = 1;
                    this.pageTotal = currentPageCount;
                }
                else if (this.pageNo === pageIndex && currentPageCount === this.pageTotal && typeof (forceRefresh) == "undefined") {
                    console.log("not refresh");
                    return;
                }

                //处理分页点中样式
                var buttons = $("#pager").find("span");
                for (var j = 0; j < buttons.length; j++) {
                    if (buttons.eq(j).html() !== pageIndex) {
                        buttons.eq(j).removeClass("active");
                    }
                    else {
                        buttons.eq(j).addClass("active");
                    }
                }

                //测试数据 随机生成的
                // var newPageInfo = [];
                // var time=new Date();
                for (var i = 0; i < this.pageSize; i++) {
                    this.items.newestItems[this.items.newestItems.length] = {
                        timestamp: time,
                        count: (i + (pageIndex - 1) * 20)
                    };
                }
                this.pageNo = pageIndex;
                // this.arrayData = newestItems;
                //如果当前页首页或者尾页，则上一页首页就不能点击，下一页尾页就不能点击
                 if(this.pageNo===1){
                        this.fDisabled=true;
                    }else if(this.pageNo===this.pageTotal){
                        this.lDisabled=true;
                    }else{
                         this.fDisabled=false;
                         this.lDisabled=false;
                    }

                //计算分页按钮数据
                if (this.pageTotal > this.showPages) {
                    if (pageIndex <= (this.showPages - 1) / 2) {
                        this.showPagesStart = 1;
                        this.showPageEnd = this.showPages - 1;
                        console.log("showPage1")
                    }
                    else if (pageIndex >= this.pageTotal - (this.showPages - 3) / 2) {
                        this.showPagesStart = this.pageTotal - this.showPages + 2;
                        this.showPageEnd = this.pageTotal;
                        console.log("showPage2")
                    }
                    else {
                        console.log("showPage3")
                        this.showPagesStart = pageIndex - (this.showPages - 3) / 2;
                        this.showPageEnd = pageIndex + (this.showPages - 3) / 2;
                    }
                }
                console.log("showPagesStart:" + this.showPagesStart + ",showPageEnd:" + this.showPageEnd + ",pageIndex:" + pageIndex);
            }
        },


        getData:function (i){
            this.pageNo = i || this.pageNo;

            GetPagePost(this.now_url, this.pageNo, this.pageSize).then(resp => {
                console.log("Page : resp.data.data", resp.data.data);
                this.items.newestItems = resp.data.data
        });
      },
        //当前页
        curPage:function (i){
            this.getData(i)
        },
        //上一页
        prePage:function (){
          if(this.pageNo>1){
              this.getData(--this.pageNo);
          }
        },
        //下一页
        nextPage:function (){
          if(this.pageNo<this.pageTotal){
              this.getData(++this.pageNo);
          }
        },

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