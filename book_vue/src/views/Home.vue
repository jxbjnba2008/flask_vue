<template>
  <div class="home">
    <Header />

      <b-container class="mt-4">
          <div>
              <b-nav tabs>
              <b-nav-item active><a style="font-size:16px; color:#E00000">热门推荐</a></b-nav-item>
              </b-nav>
          </div>
          <table role="table" aria-busy="false" aria-colcount="3" class="table b-table" style="table-layout:fixed;"><!----><!---->
                <thead role="rowgroup" class=""><!---->
                <tr role="row" class="">
                    <th role="columnheader" scope="col" aria-colindex="1" class="" style="width:160px;font-family: verdana,arial,sans-serif; font-size:13px; color:	#686868; border-width: 2px; border-color: #dedede;border-style: none none solid none;"><div>小说封面</div></th>
                    <th role="columnheader" scope="col" aria-colindex="2" class="" style="width:250px;font-family: verdana,arial,sans-serif; font-size:13px; color:	#686868; border-width: 2px; border-color: #dedede;border-style: none none solid none;"><div>小说</div></th>
                    <th role="columnheader" scope="col" aria-colindex="3" class="" style="width:110px;font-family: verdana,arial,sans-serif; font-size:13px; color:	#686868; border-width: 2px; border-color: #dedede;border-style: none none solid none;"><div>作者</div></th>
                    <th role="columnheader" scope="col" aria-colindex="4" class="" style="width:140px;font-family: verdana,arial,sans-serif; font-size:13px; color:	#686868; border-width: 2px; border-color: #dedede;border-style: none none solid none;"><div>更新时间</div></th>
                </tr>
                </thead>
                <tbody role="rowgroup"><!---->
                    <tr role="row" v-for="item in indexItems" :key="item.book_id">
                    <td><b-img thumbnail fluid class="img-rounded" style="width:25%;" :src="item.img" alt="Image 1"></b-img></td>
                    <td aria-colindex="2" role="cell" class="" style="white-space:nowrap;overflow:hidden;text-overflow: ellipsis;font-family: verdana,arial,sans-serif; font-size:10px; border-width: 1.5px;background-color: #ffffff;"><a :href="'/book/'+ item.book_id" style="font-size: 14px; color:#686868">{{ item.book_title }}</a></td>
                    <td aria-colindex="3" role="cell" class="" style="white-space:nowrap;overflow:hidden;text-overflow: ellipsis;font-family: verdana,arial,sans-serif; font-size:10px; border-width: 1.5px;background-color: #ffffff;"><a style="font-size: 14px; color:#888888">{{ item.author }}</a></td>
                    <td aria-colindex="4" role="cell" class="" style="white-space:nowrap;overflow:hidden;text-overflow: ellipsis;font-family: verdana,arial,sans-serif; font-size:10px; border-width: 1.5px;background-color: #ffffff;"><a style="font-size: 14px; color:#686868">{{ dateFormat(item.update_time) }}</a></td></tr>

                </tbody><!---->
          </table>
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
          now_url: this.$route.path,
          indexItems: {},
      }
  },

   created () {
      GetBooks().then(resp =>{
          console.log("In indexItems resp.data = ", resp.data);
          this.indexItems = resp.data.data;
      });

  }
}
</script>
