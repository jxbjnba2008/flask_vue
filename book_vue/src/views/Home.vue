<template>
  <div class="home">
    <Header />

      <b-container class="mt-4">
<!--          <div>-->
<!--              <b-nav tabs>-->
<!--                <b-nav-item active><a style="font-size:16px; color:#E00000">站长推荐</a></b-nav-item>-->
<!--              </b-nav>-->
<!--          </div>-->
          <b-card no-body>
            <b-tabs v-model="tabIndex" small card active-nav-item-class="font-weight-bold text-uppercase text-danger">
              <b-tab title="站长推荐">
                <div class="">
<!--                  <ul>-->
                    <div v-for="item in bookItems" style="width:178px;float:left">
                      <b-img thumbnail fluid class="img-rounded" style="'width':+screenWidth; height:14vw;border-style: groove;" :src="item.img" alt="Image 1"></b-img>
                       <td style="width:100%;height:11px;font-size:14px;border:0">
                       </td>
                      <a :href="'/book/'+ item.book_id" style="font-size: 12px; color:#FF6666; text-align:left">{{item.book_title}}</a>
                      <p style="font-size: 12px; color:#686868; text-align:left">作者：{{item.author}}</p>
                    </div>
<!--                  </ul>-->
	              </div>
              </b-tab>
            </b-tabs>
          </b-card>

          <p></p>

          <b-card no-body>
            <b-tabs v-model="tabIndex" small card active-nav-item-class="font-weight-bold text-uppercase text-danger">
              <b-tab title="热门小说">

                <table role="table" aria-busy="false" aria-colcount="3" class="table b-table" style="table-layout:fixed;"><!----><!---->
      <!--                <b-nav tabs>-->
      <!--                  <caption style="text-align:left; caption-side: top"><h3 style="font-size:16px; color:#E00000">热门小说</h3></caption>-->
      <!--              <thead role="rowgroup" class="">&lt;!&ndash;&ndash;&gt;-->
      <!--                  <b-nav-item active><a style="font-size:16px; color:#E00000">热门小说</a></b-nav-item>-->
      <!--                </b-nav>-->


                      <tr role="row" class="">
                          <th role="columnheader" scope="col" aria-colindex="1" class="" style="width:160px;font-family: verdana,arial,sans-serif; font-size:13px; color:	#686868; border-width: 2px; border-color: #dedede;border-style: outset none outset outset;text-align:center"><div>小说封面</div></th>
                          <th role="columnheader" scope="col" aria-colindex="2" class="" style="width:250px;font-family: verdana,arial,sans-serif; font-size:13px; color:	#686868; border-width: 2px; border-color: #dedede;border-style: outset none outset none;text-align:center"><div>小说</div></th>
                          <th role="columnheader" scope="col" aria-colindex="3" class="" style="width:110px;font-family: verdana,arial,sans-serif; font-size:13px; color:	#686868; border-width: 2px; border-color: #dedede;border-style: outset none outset none;text-align:center"><div>作者</div></th>
                          <th role="columnheader" scope="col" aria-colindex="4" class="" style="width:140px;font-family: verdana,arial,sans-serif; font-size:13px; color:	#686868; border-width: 2px; border-color: #dedede;border-style: outset outset outset none;text-align:center"><div>更新时间</div></th>
                      </tr>
      <!--              </thead>-->
                      <tbody role="rowgroup"><!---->
                          <tr role="row" v-for="item in bookItems" :key="item.book_id">
                          <td style="text-align:center;border-style: outset none outset outset;border-width: 2px;"><b-img thumbnail fluid class="img-rounded" style="width:25%;border-style: outset;" :src="item.img" alt="Image 1"></b-img></td>
                          <td aria-colindex="2" role="cell" class="" style="border-style: none none outset none;white-space:nowrap;overflow:hidden;text-overflow: ellipsis;font-family: verdana,arial,sans-serif; background-color: #ffffff; border-width: 2px;text-align:center; vertical-align: middle"><a :href="'/book/'+ item.book_id" style="font-size: 16px; color:#FF6666">{{ item.book_title }}</a></td>
                          <td aria-colindex="3" role="cell" class="" style="border-style: none none outset none;white-space:nowrap;overflow:hidden;text-overflow: ellipsis;font-family: verdana,arial,sans-serif; background-color: #ffffff; border-width: 2px;text-align:center; vertical-align: middle"><a style="font-size: 15px; color:#888888">{{ item.author }}</a></td>
                          <td aria-colindex="4" role="cell" class="" style="border-style: none outset outset none;white-space:nowrap;overflow:hidden;text-overflow: ellipsis;font-family: verdana,arial,sans-serif; background-color: #ffffff; border-width: 2px;text-align:center; vertical-align: middle"><a style="font-size: 14px; color:#686868">{{ dateFormat(item.update_time) }}</a></td></tr>

                      </tbody><!---->
                </table>

              </b-tab>
            </b-tabs>
          </b-card>
  <!--        <b-row class="mb-4">-->
  <!--            <b-col clos="12" md="4" v-for="item in items.indexItems" :key="item.book_id"><a :href="'/book/'+item.book_id" style="font-size:12px; color:#F08080">{{ item.book_title }}</a></b-col>-->
  <!--        </b-row>-->

      </b-container>

    <Footer />

  </div>
</template>

<style lang="scss" scoped>

</style>

<script>
// @ is an alias to /src
import Header from "../components/Header.vue";
import Footer from "../components/Footer.vue";

import { GetBooks } from "../apis/read.js";

import dateFormat from "@/utils/date";


export default {
  name: 'Home',
  components: {
    Header,
    Footer
  },
    data() {
      return {
          dateFormat,
          screenWidth: document.body.clientWidth,
          now_url: this.$route.path,
          bookItems: {},
          // indexItems: {},

      }
  },

   created () {
    console.log('page', this.currentPage)
      GetBooks().then(resp =>{
          console.log("In bookItems resp.data = ", resp.data);
          this.bookItems = resp.data.data;
      });

  },
    watch: {
        screenWidth(val){
            // 为了避免频繁触发resize函数导致页面卡顿，使用定时器
            if(!this.timer){
                // 一旦监听到的screenWidth值改变，就将其重新赋给data里的screenWidth
                this.screenWidth = val
                this.timer = true
                let that = this
                setTimeout(function(){
                    // 打印screenWidth变化的值
                    console.log(that.screenWidth)
                    that.timer = false
                },400)
            }
        }
      },
      mounted () {
        const that = this
        window.onresize = () => {
        return (() => {
            window.screenWidth = document.body.clientWidth
            that.screenWidth = window.screenWidth
          })()

          }

      },

}
</script>
