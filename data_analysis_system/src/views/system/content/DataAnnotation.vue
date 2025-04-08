<template>
  <el-row>
    <div class="tss-data-source-title">
      标注数据
    </div>
  </el-row>
  <el-row>
<!--    <el-col style="text-align: left; margin-top: 6px" :span="10">-->
<!--      <el-button type="primary" style="width:60px; font-size: 9px; height: 23px; border-radius: 2px">+创建数据集</el-button>-->
<!--    </el-col>-->
    <el-col style="text-align: right;" :span="24">
      <el-select
          v-model="requestParams"
          placeholder="Select"
          size="small"
          style="width: 185px; height: 23px; padding: 0; margin-right: 6px; border-radius: 2px; font-size: 10px"
      >
        <el-option
            v-for="item in data_source_options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
            style="width: 185px; height: 23px; line-height: 23px"
        />
      </el-select>
      <el-select
          v-model="requestParams"
          placeholder="Select"
          size="small"
          style="width: 185px; height: 23px; padding: 0; margin-right: 6px; border-radius: 2px; font-size: 10px"
      >
        <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
            style="width: 185px; height: 23px; line-height: 23px"
        />
      </el-select>
      <el-input
          v-model="requestParams.data_set"
          style="width: 185px; height: 23px; padding: 0; margin-right: 6px; border-radius: 2px; font-size: 10px"
          size="large"
          placeholder="输入标签组名称"
          :suffix-icon="Search"

      />
      <el-button :icon="RefreshRight"  style="height: 23px; width: 23px; padding: 0"/>
    </el-col>
  </el-row>
  <el-row style="margin-top: 10px">
    <el-table  height="200" max-height="200" :data="tableData" :cell-style="{fontSize:'10px', lineHeight:'10px'}" :header-row-style="{lineHeight: '10px'}" :header-cell-style="{lineHeight:'10px',height: '10px',fontSize: '10px', backgroundColor: '#f5f7fa', color: '#333', fontWeight: 'bold' ,}">
      <el-table-column prop="name" label="数据集/数据源名称" width="150" sortable></el-table-column>
      <el-table-column prop="comment" label="描述" width="300" show-overflow-tooltip></el-table-column>
      <el-table-column prop="type" label="类型" width="150" sortable></el-table-column>
      <el-table-column prop="create_time" label="创建时间" width="150" sortable></el-table-column>
      <el-table-column prop="update_time" label="更新时间" width="150" sortable></el-table-column>
      <el-table-column prop="file" label="标注文件" width="150" sortable></el-table-column>
      <el-table-column label="操作" fixed="right" min-width="150">
        <template #default="scope">
          <el-button size="small" link style="font-size: 10px;" type="primary">
            下载
          </el-button>
          <el-button size="small" link style="font-size: 10px;" type="primary">
            查看
          </el-button>
          <el-button
              size="small"
              type="danger"
              link
              style="font-size: 10px;"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
      <template v-slot:empty >
        <div style="line-height: normal" >
          <svg style="height: 40px; width: 40px; line-height: normal" t="1732961684200" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="6025" width="200" height="200"><path d="M0 808.96a512 153.6 0 1 0 1024 0 512 153.6 0 1 0-1024 0Z" fill="#E8E8E8" fill-opacity=".5" p-id="6026"></path><path d="M284.0064 317.44h455.9872a20.48 20.48 0 0 1 17.12128 9.25696l130.41664 199.04512A20.48 20.48 0 0 1 890.88 536.96512V819.2a20.48 20.48 0 0 1-20.48 20.48H153.6a20.48 20.48 0 0 1-20.48-20.48V536.96512a20.48 20.48 0 0 1 3.34848-11.22304l130.41664-199.04512A20.48 20.48 0 0 1 284.0064 317.44z" fill="#F9F9F9" p-id="6027"></path><path d="M284.0064 312.32h455.9872a25.6 25.6 0 0 1 21.4016 11.5712l130.41664 199.04512a25.6 25.6 0 0 1 4.18816 14.0288V819.2a25.6 25.6 0 0 1-25.6 25.6H153.6a25.6 25.6 0 0 1-25.6-25.6V536.96512a25.6 25.6 0 0 1 4.18816-14.0288L262.59456 323.8912a25.6 25.6 0 0 1 21.41184-11.5712z m0 10.24a15.36 15.36 0 0 0-12.84096 6.94272L140.7488 528.54784a15.36 15.36 0 0 0-2.5088 8.41728V819.2a15.36 15.36 0 0 0 15.36 15.36h716.8a15.36 15.36 0 0 0 15.36-15.36V536.96512a15.36 15.36 0 0 0-2.5088-8.41728L752.83456 329.50272a15.36 15.36 0 0 0-12.84096-6.94272h-455.9872z" fill="#D3D3D3" p-id="6028"></path><path d="M276.48 81.92h471.04a20.48 20.48 0 0 1 20.48 20.48v552.96a20.48 20.48 0 0 1-20.48 20.48H276.48a20.48 20.48 0 0 1-20.48-20.48V102.4a20.48 20.48 0 0 1 20.48-20.48z" fill="#FFFFFF" fill-opacity=".726" p-id="6029"></path><path d="M296.96 76.8v10.24h-20.48v-10.24h20.48z m40.96 0v10.24h-20.48v-10.24h20.48z m40.96 0v10.24h-20.48v-10.24h20.48z m40.96 0v10.24h-20.48v-10.24h20.48z m40.96 0v10.24h-20.48v-10.24h20.48z m40.96 0v10.24h-20.48v-10.24h20.48z m40.96 0v10.24h-20.48v-10.24h20.48z m40.96 0v10.24h-20.48v-10.24h20.48z m40.96 0v10.24h-20.48v-10.24h20.48z m40.96 0v10.24h-20.48v-10.24h20.48z m40.96 0v10.24h-20.48v-10.24h20.48z m51.2 0v10.24h-30.72v-10.24h30.72z m15.36 35.21536h-10.24V102.4c0-2.74432-0.7168-5.36576-2.048-7.68l8.8576-5.12c2.23232 3.85024 3.4304 8.2432 3.4304 12.8v9.61536z m0 40.96h-10.24v-20.48h10.24v20.48z m0 40.96h-10.24v-20.48h10.24v20.48z m0 40.96h-10.24v-20.48h10.24v20.48z m0 40.96h-10.24v-20.48h10.24v20.48z m0 40.96h-10.24v-20.48h10.24v20.48z m0 40.96h-10.24v-20.48h10.24v20.48z m0 40.96h-10.24v-20.48h10.24v20.48z m0 40.96h-10.24v-20.48h10.24v20.48z m0 40.96h-10.24v-20.48h10.24v20.48z m0 40.96h-10.24v-20.48h10.24v20.48z m0 40.96h-10.24v-20.48h10.24v20.48z m0 40.96h-10.24v-20.48h10.24v20.48z m0 40.96h-10.24v-20.48h10.24v20.48z m-24.32 36.43392l-0.512-10.22976a15.36 15.36 0 0 0 12.9024-8.33536l9.1136 4.67968a25.6 25.6 0 0 1-21.504 13.88544z m-40.98048 0.03072v-10.24h20.48v10.24h-20.48z m-40.96 0v-10.24h20.48v10.24h-20.48z m-40.96 0v-10.24h20.48v10.24h-20.48z m-40.96 0v-10.24h20.48v10.24h-20.48z m-40.96 0v-10.24h20.48v10.24h-20.48z m-40.96 0v-10.24h20.48v10.24h-20.48z m-40.96 0v-10.24h20.48v10.24h-20.48z m-40.96 0v-10.24h20.48v10.24h-20.48z m-40.96 0v-10.24h20.48v10.24h-20.48z m-40.96 0v-10.24h20.48v10.24h-20.48z m-40.96 0v-10.24h20.48v10.24h-20.48z m-42.9568-11.264l8.47872-5.7344c2.84672 4.1984 7.5776 6.7584 12.73856 6.7584h1.25952v10.24H276.48c-8.6016 0-16.4864-4.28032-21.21728-11.264z m-4.38272-43.17184h10.24v20.48h-10.24v-20.48z m0-40.96h10.24v20.48h-10.24v-20.48z m0-40.96h10.24v20.48h-10.24v-20.48z m0-40.96h10.24v20.48h-10.24v-20.48z m0-40.96h10.24v20.48h-10.24v-20.48z m0-40.96h10.24v20.48h-10.24v-20.48z m0-40.96h10.24v20.48h-10.24v-20.48z m0-40.96h10.24v20.48h-10.24v-20.48z m0-40.96h10.24v20.48h-10.24v-20.48z m0-40.96h10.24v20.48h-10.24v-20.48z m0-40.96h10.24v20.48h-10.24v-20.48z m0-40.96h10.24v20.48h-10.24v-20.48z m0-40.96h10.24v20.48h-10.24v-20.48z m2.11968-42.82368l9.39008 4.096c-0.82944 1.90464-1.26976 3.98336-1.26976 6.12352v12.12416h-10.24V102.4c0-3.55328 0.72704-7.02464 2.11968-10.21952z m23.2448-15.38048l0.09216 10.24c-0.63488 0-1.26976 0.0512-1.88416 0.13312l-1.34144-10.14784c1.024-0.14336 2.07872-0.21504 3.13344-0.22528z" fill="#D0D0D0" p-id="6030"></path><path d="M143.36 532.48h226.37568a20.48 20.48 0 0 1 20.48 20.48v25.82528a20.48 20.48 0 0 0 20.48 20.48h202.60864a20.48 20.48 0 0 0 20.48-20.48V552.96a20.48 20.48 0 0 1 20.48-20.48H880.64a10.24 10.24 0 0 1 10.24 10.24v286.72a10.24 10.24 0 0 1-10.24 10.24H143.36a10.24 10.24 0 0 1-10.24-10.24V542.72a10.24 10.24 0 0 1 10.24-10.24z" fill="#FFFFFF" p-id="6031"></path><path d="M143.36 527.36h226.37568a25.6 25.6 0 0 1 25.6 25.6v25.82528a15.36 15.36 0 0 0 15.36 15.36h202.60864a15.36 15.36 0 0 0 15.36-15.36V552.96a25.6 25.6 0 0 1 25.6-25.6H880.64a15.36 15.36 0 0 1 15.36 15.36v286.72a15.36 15.36 0 0 1-15.36 15.36H143.36a15.36 15.36 0 0 1-15.36-15.36V542.72a15.36 15.36 0 0 1 15.36-15.36z m0 10.24a5.12 5.12 0 0 0-5.12 5.12v286.72a5.12 5.12 0 0 0 5.12 5.12h737.28a5.12 5.12 0 0 0 5.12-5.12V542.72a5.12 5.12 0 0 0-5.12-5.12H654.26432a15.36 15.36 0 0 0-15.36 15.36v25.82528a25.6 25.6 0 0 1-25.6 25.6H410.69568a25.6 25.6 0 0 1-25.6-25.6V552.96a15.36 15.36 0 0 0-15.36-15.36H143.36z" fill="#D3D3D3" p-id="6032"></path></svg>
        </div>
        <div style="line-height: normal; font-size: 12px">暂无标签组</div>
        <div style="line-height: normal; font-size: 8px">您可以添加 <el-button link style="padding: 0; border: none; font-size: 8px" type="primary">添加标签组</el-button></div>
      </template>
    </el-table>
  </el-row>
</template>

<script>
import {RefreshRight} from "@element-plus/icons-vue";

export default {
  name: "DataAnnotation",
  computed: {
    RefreshRight() {
      return RefreshRight
    }
  },
  data() {
    return {
      options: [{
        label: "全部",
        value: "全部"
      }],
      data_source_options: [{
        label: "我的数据集",
        value: "我的数据集"
      }],
      requestParams: {
        data_set: "",
      },
      tableData: [
        {
          "name": "测试数据集",
          "comment": "这是测试数据集",
          "type" : "时频标注",
          "create_time": "2024-12-01 23:11:00",
          "update_time": "2024-12-01 23:11:00",
          "file":"生成标注文件.xlsx"
        }
      ]
    }
  },
}
</script>

<style scoped>

</style>