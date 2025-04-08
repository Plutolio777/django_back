<!-- 代码已包含 CSS：使用 TailwindCSS , 安装 TailwindCSS 后方可看到布局样式效果 -->
<template>
  <div class="min-h-screen bg-gray-50 p-4 max-w-[1980px] mx-auto">
    <!-- 标题区域 -->
    <div class="mb-6 bg-gradient-to-r from-white to-blue-50 p-6 rounded-xl shadow-sm border border-gray-100">
      <div class="flex items-center gap-4">
        <div class="p-3 bg-blue-500 bg-opacity-10 rounded-xl">
          <i class="fas fa-database text-2xl text-blue-600"></i>
        </div>
        <div>
          <h1 class="text-2xl font-bold bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent">数据集管理</h1>
          <p class="mt-2 text-gray-600">管理和维护各类数据集，支持查看、编辑和删除操作</p>
        </div>
      </div>
      <div class="mt-4 flex gap-4">
        <div class="flex items-center gap-2">
          <div class="w-2 h-2 rounded-full bg-green-500"></div>
          <span class="text-gray-600">在线数据集：125</span>
        </div>
        <div class="flex items-center gap-2">
          <div class="w-2 h-2 rounded-full bg-blue-500"></div>
          <span class="text-gray-600">总存储量：1.2 TB</span>
        </div>
        <div class="flex items-center gap-2">
          <div class="w-2 h-2 rounded-full bg-purple-500"></div>
          <span class="text-gray-600">今日更新：8</span>
        </div>
      </div>
    </div>
    <!-- 功能栏区域 -->
    <div class="mb-6 bg-white p-4 rounded-xl shadow-sm flex flex-wrap items-center justify-between gap-4">
      <div class="flex items-center gap-4">
        <button @click="showCreateModal = true" class="!rounded-button flex items-center gap-2 bg-gradient-to-r from-blue-600 to-blue-700 px-5 py-2.5 text-white hover:from-blue-700 hover:to-blue-800 transition-all duration-200 shadow-sm">
          <i class="fas fa-plus text-white/90"></i>
          <span class="whitespace-nowrap font-medium">新建数据集</span>
        </button>
        <div class="relative">
          <button @click="toggleTypeFilter" class="!rounded-button flex items-center gap-2 bg-gray-50 border-gray-200 border px-4 py-2.5 text-gray-700 hover:bg-gray-100 transition-all duration-200">
            <i class="fas fa-filter text-gray-500"></i>
            <span class="whitespace-nowrap">数据集类型</span>
            <i class="fas fa-chevron-down text-gray-400 text-xs ml-1"></i>
          </button>
          <div v-if="showTypeFilter" class="absolute left-0 top-full z-10 mt-2 w-56 rounded-xl border border-gray-200 bg-white p-3 shadow-lg">
            <div v-for="type in dataTypes" :key="type" class="flex items-center gap-3 p-2 hover:bg-gray-50 rounded-lg transition-colors cursor-pointer">
              <input type="checkbox" :value="type" v-model="selectedTypes" class="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500">
              <span class="text-gray-700">{{ type }}</span>
            </div>
          </div>
        </div>
      </div>
      <div class="relative flex-1 max-w-md">
        <i class="fas fa-search absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
        <input
            v-model="searchQuery"
            type="text"
            placeholder="搜索数据集名称"
            class="!rounded-button w-full bg-gray-50 border border-gray-200 pl-11 pr-4 py-2.5 text-gray-700 placeholder-gray-400 focus:bg-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all duration-200"
        >
      </div>
    </div>
    <!-- 数据集列表 -->
    <div class="mb-6 overflow-x-auto rounded-lg bg-white shadow">
      <table class="min-w-full table-auto">
        <thead class="bg-gray-50">
        <tr>
          <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">数据集名称</th>
          <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">描述</th>
          <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">类型</th>
          <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">生成时间</th>
          <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">更新时间</th>
          <th class="px-6 py-3 text-center text-sm font-semibold text-gray-900">操作</th>
        </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
        <template v-if="dataSetList.length">
          <tr v-for="item in dataSetList" :key="item.id" class="hover:bg-gray-50">
            <td class="px-6 py-4">
              <a :href="item.data_set_path" :download="item.origin_path" class="text-blue-600 hover:underline">{{ item.name }}</a>
            </td>
            <td class="px-6 py-4">
              <div class="max-w-[5em] overflow-hidden text-ellipsis whitespace-nowrap hover:overflow-visible hover:whitespace-normal hover:absolute hover:z-10 hover:bg-white hover:shadow-lg hover:p-2 hover:rounded-lg hover:border hover:min-w-[300px] hover:max-w-[400px]">{{ item.description }}</div>
            </td>
            <td class="px-6 py-4">
              <span class="rounded-full bg-blue-100 px-3 py-1 text-sm text-blue-800">{{ item.type }}</span>
            </td>
            <td class="px-6 py-4 text-sm text-gray-500">{{ item.create_time}}</td>
            <td class="px-6 py-4 text-sm text-gray-500">{{ item.update_time }}</td>
            <td class="px-6 py-4">
              <div class="flex justify-center gap-3">
                <button @click="editDataset(item)" class="!rounded-button text-gray-600 hover:text-blue-600" title="编辑">
                  <i class="fas fa-edit"></i>
                </button>
                <button class="!rounded-button text-gray-600 hover:text-green-600" title="查看" @click="viewDataset(item)">
                  <i class="fas fa-eye"></i>
                </button>
                <button @click="deleteDataset(item.id)" class="!rounded-button text-gray-600 hover:text-red-600" title="删除">
                  <i class="fas fa-trash"></i>
                </button>
              </div>
            </td>
          </tr>
        </template>
        <template v-else>
          <tr>
            <td colspan="6" class="px-6 py-8 text-center">
              <div class="flex flex-col items-center justify-center text-gray-500">
                <i class="fas fa-inbox text-4xl mb-2"></i>
                <span class="text-sm">暂无数据</span>
              </div>
            </td>
          </tr>
        </template>
        </tbody>
      </table>
    </div>
    <!-- 分页 -->
    <div class="flex items-center justify-between bg-white px-4 py-3 sm:px-6">
      <div class="flex items-center gap-2">
        <span class="text-sm text-gray-700">每页显示</span>
        <div class="relative">
          <button @click="showPageSizeOptions = !showPageSizeOptions" class="!rounded-button flex items-center gap-2 border border-gray-200 px-3 py-1.5 text-sm hover:bg-gray-50">
            <span>{{ pageSize }}</span>
            <i class="fas fa-chevron-down text-gray-400 text-xs"></i>
          </button>
          <div v-if="showPageSizeOptions" class="absolute left-0 top-full z-10 mt-1 w-20 rounded-lg border border-gray-200 bg-white py-1 shadow-lg">
            <button v-for="size in [5, 10, 20, 50]" :key="size" @click="() => { pageSize = size; handlePageSizeChange(); showPageSizeOptions = false; }" class="w-full px-4 py-2 text-left text-sm hover:bg-blue-50" :class="{'text-blue-600 bg-blue-50': pageSize === size, 'text-gray-700': pageSize !== size}">
              {{ size }}
            </button>
          </div>
        </div>
        <span class="text-sm text-gray-700">条</span>
      </div>
      <div class="flex items-center gap-2">
        <button
            @click="currentPage--"
            :disabled="currentPage === 1"
            class="!rounded-button whitespace-nowrap border px-3 py-1 text-sm disabled:opacity-50"
        >
          上一页
        </button>
        <span class="text-sm text-gray-700">第 {{ currentPage }} 页，共 {{ totalPages }} 页</span>
        <button
            @click="currentPage++"
            :disabled="currentPage === totalPages"
            class="!rounded-button whitespace-nowrap border px-3 py-1 text-sm disabled:opacity-50"
        >
          下一页
        </button>
      </div>
    </div>
    <!-- 创建数据集弹窗 -->
    <div v-if="showCreateModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div class="w-11/12 max-w-xl rounded-lg bg-white p-5">
        <div class="mb-6 flex items-center justify-between">
          <h3 class="text-lg font-semibold">创建新数据集</h3>
          <button @click="showCreateModal = false;resetNewDataSetForm()" class="!rounded-button text-gray-500 hover:text-gray-700">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <form @submit.prevent="handleCreateDataset" class="space-y-6">
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-700">数据集名称</label>
            <input
                v-model="newDataset.name"
                type="text"
                class="!rounded-button w-full border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:ring-blue-500"
                placeholder="请输入数据集名称"
            >
          </div>
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-700">数据集类型</label>
            <div class="relative">
              <button
                  type="button"
                  @click="showTypeSelect = !showTypeSelect"
                  class="!rounded-button flex w-full items-center justify-between border border-gray-300 bg-white px-3 py-2 text-sm hover:bg-gray-50"
              >
                <span class="text-gray-700">{{ newDataset.type || '请选择数据集类型' }}</span>
                <i class="fas fa-chevron-down text-gray-400"></i>
              </button>
              <div v-if="showTypeSelect" class="absolute left-0 right-0 top-full z-50 mt-1 max-h-48 overflow-y-auto rounded-lg border bg-white py-1 shadow-lg">
                <button
                    v-for="type in dataTypes"
                    :key="type"
                    type="button"
                    @click="() => { newDataset.type = type; showTypeSelect = false; }"
                    class="w-full px-4 py-2 text-left text-sm hover:bg-blue-50"
                    :class="{'text-blue-600 bg-blue-50': newDataset.type === type, 'text-gray-700': newDataset.type !== type}"
                >
                  {{ type }}
                </button>
              </div>
            </div>
          </div>
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-700">描述</label>
            <textarea
                v-model="newDataset.description"
                rows="3"
                class="!rounded-button w-full border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:ring-blue-500"
                placeholder="请输入数据集描述"
            ></textarea>
          </div>
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-700">上传数据文件</label>
            <div class="relative">
              <input
                  ref="fileInput"
                  type="file"
                  @change="handleFileChange"
                  class="hidden"
                  accept=".csv,.xlsx,.xls"
              >
              <div
                  @click="$refs.fileInput.click()"
                  class="!rounded-button flex cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed border-gray-300 p-6 hover:border-blue-500"
              >
                <i class="fas fa-cloud-upload-alt mb-2 text-3xl text-gray-400"></i>
                <p class="mb-1 text-sm text-gray-600">点击或拖拽文件到此处上传</p>
                <p class="text-xs text-gray-500">支持 .csv、.xlsx、.json 格式文件</p>
              </div>
              <div v-if="selectedFile" class="mt-2 flex items-center gap-2 text-sm text-gray-600">
                <i class="fas fa-file"></i>
                <span>{{ selectedFile.name }}</span>
                <button @click="selectedFile = null" type="button" class="!rounded-button text-red-500 hover:text-red-600">
                  <i class="fas fa-times"></i>
                </button>
              </div>
            </div>
          </div>
          <div class="flex justify-end gap-3">
            <button
                type="button"
                @click="showCreateModal = false;resetNewDataSetForm()"
                class="!rounded-button border border-gray-300 px-4 py-2 text-sm hover:bg-gray-50"
            >
              取消
            </button>
            <button
                type="submit"
                class="!rounded-button bg-blue-600 px-4 py-2 text-sm text-white hover:bg-blue-700"
            >
              创建
            </button>
          </div>
        </form>
      </div>
    </div>
    <!-- 编辑数据集弹窗 -->
    <div v-if="showEditModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div class="w-11/12 max-w-xl rounded-lg bg-white p-5">
        <div class="mb-6 flex items-center justify-between">
          <h3 class="text-lg font-semibold">编辑数据集</h3>
          <button @click="showEditModal = false" class="!rounded-button text-gray-500 hover:text-gray-700">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <form @submit.prevent="handleEditDataset" class="space-y-6">
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-700">数据集名称</label>
            <input
                v-model="editingDataset!.name"
                type="text"
                required
                class="!rounded-button w-full border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:ring-blue-500"
                placeholder="请输入数据集名称"
            >
          </div>
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-700">数据集类型</label>
            <input
                :value="editingDataset?.type"
                type="text"
                disabled
                class="!rounded-button w-full border border-gray-200 bg-gray-50 px-3 py-2 text-sm text-gray-500"
            >
          </div>
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-700">描述</label>
            <textarea
                v-model="editingDataset!.description"
                rows="3"
                class="!rounded-button w-full border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:ring-blue-500"
                placeholder="请输入数据集描述"
            ></textarea>
          </div>
          <div class="text-sm text-gray-500">
            <div>创建时间：{{ editingDataset?.create_time }}</div>
            <div>更新时间：{{ editingDataset?.update_time }}</div>
          </div>
          <div class="flex justify-end gap-3">
            <button
                type="button"
                @click="showEditModal = false"
                class="!rounded-button border border-gray-300 px-4 py-2 text-sm hover:bg-gray-50"
            >
              取消
            </button>
            <button
                type="submit"
                class="!rounded-button bg-blue-600 px-4 py-2 text-sm text-white hover:bg-blue-700"
            >
              保存
            </button>
          </div>
        </form>
      </div>
    </div>
    <!-- 数据集查看弹窗 -->
    <div v-if="showViewModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div class="w-11/12 max-w-5xl rounded-lg bg-white p-5">
        <div class="mb-4 flex items-center justify-between">
          <h3 class="text-lg font-semibold">{{ dataSetDetail?.name }} - 数据详情</h3>
          <button @click="showViewModal = false; detailCurrentPage=0" class="!rounded-button text-gray-500 hover:text-gray-700">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="mb-4 overflow-x-auto">
          <table class="min-w-full table-auto">
            <thead class="bg-gray-50">
            <tr>
              <th v-for="header in dataSetDetail.headers" :key="header" class="px-6 py-3 text-left text-sm font-semibold text-gray-900">
                {{ header }}
              </th>
            </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
            <template v-if="dataSetDetail.headers.length">
              <tr v-for="(row, index) in dataSetDetail.data" :key="index" class="hover:bg-gray-50">
                <td v-for="header in dataSetDetail.headers" :key="header" class="px-6 py-4 text-sm">
                  {{ row[header] }}
                </td>
              </tr>
            </template>
            <template v-else>
              <tr>
                <td :colspan="dataSetDetail.headers.length" class="px-6 py-8 text-center">
                  <div class="flex flex-col items-center justify-center text-gray-500">
                    <i class="fas fa-inbox text-4xl mb-2"></i>
                    <span class="text-sm">暂无数据</span>
                  </div>
                </td>
              </tr>
            </template>
            </tbody>
          </table>
        </div>
        <!-- 详情数据分页 -->
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="text-sm text-gray-700">每页显示</span>
            <div class="relative">
              <button @click="showDetailPageSizeOptions = !showDetailPageSizeOptions" class="!rounded-button flex items-center gap-2 border border-gray-200 px-3 py-1.5 text-sm hover:bg-gray-50">
                <span>{{ detailPageSize }}</span>
                <i class="fas fa-chevron-down text-gray-400 text-xs"></i>
              </button>
              <div v-if="showDetailPageSizeOptions" class="absolute left-0 top-full z-10 mt-1 w-20 rounded-lg border border-gray-200 bg-white py-1 shadow-lg">
                <button v-for="size in [5, 10]" :key="size" @click="() => { detailPageSize = size; showDetailPageSizeOptions = false; }" class="w-full px-4 py-2 text-left text-sm hover:bg-blue-50" :class="{'text-blue-600 bg-blue-50': detailPageSize === size, 'text-gray-700': detailPageSize !== size}">
                  {{ size }}
                </button>
              </div>
            </div>
            <span class="text-sm text-gray-700">条</span>
          </div>
          <div class="flex items-center gap-2">
            <button
                @click="detailCurrentPage--"
                :disabled="detailCurrentPage === 1"
                class="!rounded-button whitespace-nowrap border px-3 py-1 text-sm disabled:opacity-50"
            >
              上一页
            </button>
            <span class="text-sm text-gray-700">第 {{ detailCurrentPage }} 页，共 {{ detailTotalPages }} 页</span>
            <button
                @click="detailCurrentPage++"
                :disabled="detailCurrentPage === detailTotalPages"
                class="!rounded-button whitespace-nowrap border px-3 py-1 text-sm disabled:opacity-50"
            >
              下一页
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import apiService from "@/api/apiService"
export default {
  mounted() {
    this.pageSize=10;
    this.currentPage=1;
    // this.selectedDataset = [];
    this.selectedTypes = [];
    this.searchQuery = "";
    this.fetchData()
  },
  data() {
    return {
      showEditModal: false,
      showCreateModal: false,
      showTypeFilter: false,
      showTypeSelect: false,
      selectedFile: null,
      newDataset: {
        name: '',
        type: '',
        description: '',

      },
      editingDataset: {
        id: "",
        name:"",
        type:"",
        description:"",
        create_time: "",
        update_time:"",
      },
      total: 0,

      searchQuery: '',
      currentPage: 1,
      pageSize: 10,
      showViewModal: false,
      selectedDataset: null,
      detailCurrentPage: 0,
      detailPageSize: 5,
      showPageSizeOptions: false,
      showDetailPageSizeOptions: false,
      dataTypes: ['csv', 'excel'],
      selectedTypes: [],
      dataSetList: [

      ],
      dataSetDetail: {
        id:null,
        name:"",
        headers: [],
        total_rows: 0,
        data:[]
      },
      datasetHeaders: []
    };
  },
  computed: {
    totalPages() {
      if (this.total === 0){
        return 1;
      }else {
        return Math.ceil(this.total / this.pageSize);
      }
    },
    detailTotalPages() {
      if (this.dataSetDetail.total_rows === 0){
        return 1;
      }else {
        return Math.ceil(this.dataSetDetail.total_rows / this.pageSize);
      }

    },
  },
  watch: {
    currentPage: "fetchData",
    pageSize: "fetchData",
    searchQuery: "fetchData",
    selectedTypes: "fetchData",
    detailCurrentPage(newValue, oldValue) {
      if (newValue !== 0) {
        this.fetchDetailData();
      }
    },
    detailPageSize: "fetchDetailData"
  },
  methods: {
    async fetchDetailData(){
      let params = {
        id: this.selectedDataset.id,
        offset: (this.detailCurrentPage - 1) * this.detailPageSize,
        limit: this.detailPageSize,
      }
      let res = await apiService.dataSetDetail({}, params)
      if (res.success){
        this.dataSetDetail = res.data.data
      }else{
        this.$message.error("数据查询失败");
      }
    },
    async editDataset(dataset: Object){
      this.editingDataset = { ...dataset };
      this.showEditModal = true;
    },
    async deleteDataset(dataSetId: Number){
      let res = await apiService.deleteDataSet({}, {}, {id: dataSetId})
      if (res.success) {
        this.$message({type:"success", message:"删除成功"})
        await this.fetchData();
      }else {
        this.$message({type:"error", message:"删除失败"})
      }
    },
    clearPageData(){

    },
    async fetchData(){
      let params = {
        limit: this.pageSize,
        offset: (this.currentPage - 1) * this.pageSize,
      }
      if (this.selectedTypes.length > 0) {
        params["type"]= this.selectedTypes.join(',');
      }

      if (this.searchQuery) {
        params["name"] = this.searchQuery;
      }

      let response = await apiService.fetchDataSet({}, params);
      if (response.success){
        this.total = response.data.data.count;
        this.dataSetList = response.data.data.results
        console.log(this.dataSetList);
      }else {
        this.$message({
          type: "error",
          message: "数据集加载失败"
        })
      }
    },
    handleFileChange(event) {
      console.log(event);
      const input = event.target;
      if (input.files && input.files[0]) {
        this.selectedFile = input.files[0];
        input.value = '';
      }
    },
    resetNewDataSetForm(){
      // Reset form
      this.newDataset = {
        name: '',
        type: '',
        description: ''
      };
      this.selectedFile = null;
      this.showCreateModal = false;
    },
    async handleCreateDataset() {
      if (!this.newDataset.name) {
        this.$message({
          type: "warning",
          message: "请输入数据集名称",
        })
        return;
      }
      if (!this.newDataset.type) {
        this.$message({
          type: "warning",
          message: "请选择数据集类型",
        })
        return;
      }
      if (!this.selectedFile) {
        this.$message({
          type: "warning",
          message: "请选择上传的文件",
        })
        return;
      }
      let data = {
        name: this.newDataset.name,
        type: this.newDataset.type,
        description: this.newDataset.description,
        data_set_path: this.selectedFile,
      }
      let response = await apiService.uploadDataSet(data)
      if (response.success){
        this.$message({
          type: "success",
          message: "上传成功"
        })
        await this.fetchData()
      }else {
        this.$message({
          type: "error",
          message: "上传失败"
        })
      }
      console.log(123123, response)
      this.resetNewDataSetForm()
      this.showCreateModal = false;
    },
    async handleEditDataset(){
      let data = {
        name: this.editingDataset.name,
        description: this.editingDataset.description,
      }
      let pathParams = {
        id: this.editingDataset.id,
      }
      let response = await apiService.editDataSet(data, {}, pathParams)
      if (response.success) {
        this.$message({type:"success", message:"编辑成功"})
        this.showEditModal = false;
        await this.fetchData();

      }else {
        this.$message({type:"error", message:"编辑失败"})
      }

    },
    handlePageSizeChange() {
      this.currentPage = 1;
    },
    toggleTypeFilter() {
      this.showTypeFilter = !this.showTypeFilter;
    },
    async viewDataset(dataset) {
      this.selectedDataset = dataset;
      this.showViewModal = true;
      this.detailCurrentPage = 1;
    }
  }
};
</script>

<style scoped>
.custom-table__row:hover {
  background-color: rgba(0, 0, 0, 0.02);
}
input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
</style>
