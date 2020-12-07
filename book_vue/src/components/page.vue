<template id="page">
  <div class="text-right" style="width:95%;" v-if="pages===0||pages===1?false:true">
    <ul class="pagination" style="margin:0px 0px 50px 0px;">
      <li v-on:click.stop.prevent="pageChange(pageNo==1?1:pageNo-1)" v-bind:class="{disabled:pageNo===1}"><a href="javascript:void(0);">上一页</a></li>
      <!-- 默认显示第一页 -->
      <li @click.stop.prevent="pageChange(1)" v-bind:class="{active:pageNo===1}" v-if="{false:pageNo===1}"><a>1</a></li>
      <!-- 省略的页数 -->
      <li @click.stop.prevent="pageChange(pageNo - display)" v-if="showJumpPrev"><a style="font-weight:900;">&laquo;</a></li>
      <!-- 显示的页数 -->
      <li v-for="page in pagingCounts" @click.stop.prevent="pageChange(page)" v-bind:class="{active:pageNo===page}"><a>{{page}}</a></li>
      <!-- 省略的页数 -->
      <li @click.stop.prevent="pageChange(pageNo + display)" v-if="showJumpNext"><a style="font-weight:900;">&raquo;</a></li>
      <!-- 默认显示最后一页 -->
      <li @click.stop.prevent="pageChange(pages)" v-bind:class="{active:pageNo===pages}" v-if="pages===0||pages===1?false:true"><a>{{pages}}</a></li>
      <li v-on:click.stop.prevent="pageChange(pageNo==pages?pages:pageNo+1)" v-bind:class="{disabled:pageNo===pages}"><a href="javascript:void(0);">下一页</a></li>
      <li class="disabled"><a href="javascript:void(0);">{{total}}条记录</a></li>
    </ul>
  </div>
</template>

<script>
  export default {
    data: function () {
      return {
        // 当前页
        pageNo: 1,
        // 总页数
        pages: 0
      }
    },
    // 绑定页面传参
    props: {
      display: {// 显示页数
        type: Number,
        default: 5,
        required: false
      },
      total: {// 总记录数
        type: Number,
        default: 1
      },
      pageSize: {// 每页显示条数
        type: Number,
        default: 10,
        required: false
      }
    },
    created: function () {// 生命周期函数，创建时计算总页数
      let that = this
      this.pages = Math.ceil(that.total / that.pageSize)
    },
    computed: {
      numOffset() {
        return Math.floor((this.display + 2) / 2) - 1;
      },
      showJumpPrev() {
        if (this.total > this.display + 2) {
          if (this.pageNo > this.display) {
            return true
          }
        }
        return false
      },
      showJumpNext() {
        if (this.pages > this.display + 2) {
          if (this.pageNo <= this.pages - this.display) {
            return true
          }
        }
        return false
      },
      // 当前要显示的数字按钮集合
      pagingCounts() {
        let that = this,
          startNum,
          result = [],
          showJumpPrev = that.showJumpPrev,
          showJumpNext = that.showJumpNext;
        if (showJumpPrev && !showJumpNext) {
          startNum = that.pages - that.display;
          for (let i = startNum; i < that.pages; i++) {
            result.push(i);
          }
        } else if (!showJumpPrev && showJumpNext) {
          for (let i = 2; i < that.display + 2; i++) {
            result.push(i);
          }
        } else if (showJumpPrev && showJumpNext) {
          for (let i = that.pageNo - that.numOffset; i <= that.pageNo + that.numOffset; i++) {
            result.push(i);
          }
        } else {
          for (let i = 2; i < that.pages; i++) {
            result.push(i);
          }
        }
        return result
      }
    },
    methods: {
      pageChange: function (page) {
        if (this.pageNo === page) {
          return;
        }
        this.pageNo = page;
        this.$emit('navpage', this.pageNo);
      }
    },
    watch: {
      total:{
        handler: function(){
          let that = this
          this.pages = Math.ceil(that.total / that.pageSize)
        }
      }
    }
  }
</script>

<style scoped>

</style>