<template>
  <div class="common-layout"  style="height: 100%; width: 100%">
    <el-container style="height: 100%; width: 100%">
      <el-header class="custom-header z-50" style="border-bottom: 1px solid #000000;"><HeadView/></el-header>
      <el-main class="custom-main" style="padding: 0">
        <router-view ></router-view>
      </el-main>
    </el-container>
  </div>
</template>

<script >

import {defineComponent} from "vue";
import HeadView from "./views/header/HeadView.vue";

export default defineComponent({
  components: {HeadView}
})
</script>

<style lang="less">
@import './style/common';
.custom-header{
}
.custom-main{
  height: 100%;
}
</style>
