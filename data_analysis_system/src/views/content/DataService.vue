<template>
  <el-row>
    <div style="width: 100%; margin-top: 15px; ">
      <el-steps

          style="max-width: 80%;margin-left: auto; margin-right: auto;background-color: white"
          :space="500"

          simple
      >
        <el-step title="数据管理" :icon="Edit" />
        <el-step title="数据标记" :icon="UploadFilled" />
        <el-step title="数据处理" :icon="Picture" />
        <el-step title="实时数据" :icon="Picture" />
      </el-steps>

<!--      <el-steps style="max-width: 600px" :active="1" finish-status="success" simple>-->
<!--        <el-step title="Step 1" />-->
<!--        <el-step title="Step 2" />-->
<!--        <el-step title="Step 3" />-->
<!--      </el-steps>-->
    </div>

  </el-row>
  <el-row style="margin-top: 30px">

    <div style="width: 65%; height: 300px; margin-left: auto; margin-right: auto;margin-bottom:0;padding: 1px; background-color: #f5f4f4">
      <el-row style="margin-top: 2px">
        <el-col :span="21" >
          <div style="text-align: left;padding-top: 2px; padding-left: 10px">
            数据管理
          </div>
        </el-col>
        <el-col :span="3" style="text-align: right; padding-right: 10px">
          <el-button link :type="'primary'">了解详情</el-button>
        </el-col>
      </el-row>
      <el-row style="margin-top: 10px; height: 100%">
        <el-col :span="8" style="display: flex; justify-content: center; align-items: center;">
          <div style="margin: 2px 2px; height: 251px; width:219px">
            <el-image src="/static/images/data-manage.png"></el-image>
          </div>
        </el-col>
        <el-col :span="16" style="display: flex; justify-content: center; align-items: center; width: 100%">
          <div style="height: 250px; width:100%;margin-right:10px; text-align: left">
            <div class="data-title">丰富的标注模版</div>
            <div class="data-content">支持图像分类、物体检测、图像分割、文本分类、短文本相似度、音频分类、视频分类等丰富易用的标注工具</div>
            <div class="data-title">智能标注</div>
            <div class="data-content">提供人机交互协作标注，最高降低90%的标注成本。目前智能标注已支持物体检测、图像分割等数据类型</div>
            <div class="data-title">百度众测及数据服务提供商标注支持</div>
            <div class="data-content">EasyData已全面对接百度众测及AI市场中的优质数据服务商，可通过EasyData平台面向百度众测提交详细的标注需求</div>


          </div>
        </el-col>
      </el-row >
    </div>
  </el-row>

</template>

<script>
import {Edit, Picture, Upload, UploadFilled} from "@element-plus/icons-vue";

export default {
  name: "DataService",
  computed: {
    UploadFilled() {
      return UploadFilled
    },
    Picture() {
      return Picture
    },
    Upload() {
      return Upload
    },
    Edit() {
      return Edit
    }
  }
}
</script>

<style scoped>
.el-card.card {
  --el-card-padding: 10px;
}
.data-title{
  font-size: 13px;
  font-weight: bold;
  padding-top: 10px;
}
.data-content{
  font-size: 11px;
  padding-top: 11px;
}
</style>