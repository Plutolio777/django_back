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
          <h1 class="text-2xl font-bold bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent">数据源管理</h1>
          <p class="mt-2 text-gray-600">管理和维护各类数据源，支持远程文件和接口获取等多种数据源类型</p>
        </div>
      </div>
      <div class="mt-4 flex gap-4">
        <div class="flex items-center gap-2">
          <div class="w-2 h-2 rounded-full bg-green-500"></div>
          <span class="text-gray-600">在线数据源：36</span>
        </div>
        <div class="flex items-center gap-2">
          <div class="w-2 h-2 rounded-full bg-blue-500"></div>
          <span class="text-gray-600">远程文件：22</span>
        </div>
        <div class="flex items-center gap-2">
          <div class="w-2 h-2 rounded-full bg-purple-500"></div>
          <span class="text-gray-600">接口数据源：14</span>
        </div>
      </div>
    </div>
    <!-- 功能栏区域 -->
    <div class="mb-6 bg-white p-4 rounded-xl shadow-sm flex flex-wrap items-center justify-between gap-4">
      <div class="flex items-center gap-4">
        <button @click="showCreateModal = true" class="!rounded-button flex items-center gap-2 bg-gradient-to-r from-blue-600 to-blue-700 px-5 py-2.5 text-white hover:from-blue-700 hover:to-blue-800 transition-all duration-200 shadow-sm">
          <i class="fas fa-plus text-white/90"></i>
          <span class="whitespace-nowrap font-medium">添加数据源</span>
        </button>
        <div class="flex gap-4">
          <div class="relative">
            <button @click="toggleTypeFilter" class="!rounded-button flex items-center gap-2 bg-gray-50 border-gray-200 border px-4 py-2.5 text-gray-700 hover:bg-gray-100 transition-all duration-200">
              <i class="fas fa-filter text-gray-500"></i>
              <span class="whitespace-nowrap">数据源类型</span>
              <i class="fas fa-chevron-down text-gray-400 text-xs ml-1"></i>
            </button>
            <div v-if="showTypeFilter" class="absolute left-0 top-full z-10 mt-2 w-56 rounded-xl border border-gray-200 bg-white p-3 shadow-lg">
              <div v-for="type in dataTypes" :key="type" class="flex items-center gap-3 p-2 hover:bg-gray-50 rounded-lg transition-colors cursor-pointer">
                <input type="checkbox" :value="type" v-model="selectedTypes" class="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500">
                <span class="text-gray-700">{{ type }}</span>
              </div>
            </div>
          </div>
          <div class="relative">
            <button @click="showStatusFilter = !showStatusFilter" class="!rounded-button flex items-center gap-2 bg-gray-50 border-gray-200 border px-4 py-2.5 text-gray-700 hover:bg-gray-100 transition-all duration-200">
              <i class="fas fa-filter text-gray-500"></i>
              <span class="whitespace-nowrap">执行状态</span>
              <i class="fas fa-chevron-down text-gray-400 text-xs ml-1"></i>
            </button>
            <div v-if="showStatusFilter" class="absolute left-0 top-full z-10 mt-2 w-56 rounded-xl border border-gray-200 bg-white p-3 shadow-lg">
              <div v-for="status in ['unexecuted', 'executing', 'failed']" :key="status" class="flex items-center gap-3 p-2 hover:bg-gray-50 rounded-lg transition-colors cursor-pointer">
                <input type="checkbox" :value="status" v-model="selectedStatus" class="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500">
                <span class="text-gray-700">{{ status === 'unexecuted' ? '未执行' : status === 'executing' ? '执行中' : '执行失败' }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="relative flex-1 max-w-md">
        <i class="fas fa-search absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
        <input
            v-model="searchQuery"
            type="text"
            placeholder="搜索数据源名称"
            class="!rounded-button w-full bg-gray-50 border border-gray-200 pl-11 pr-4 py-2.5 text-gray-700 placeholder-gray-400 focus:bg-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all duration-200"
        >
      </div>
    </div>
    <!-- 数据集列表 -->
    <div class="mb-6 overflow-x-auto rounded-lg bg-white shadow">
      <table class="min-w-full table-auto">
        <thead class="bg-gray-50">
        <tr>
          <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">数据源名称</th>
          <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">数据源类型</th>
          <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">描述</th>
          <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">状态</th>
          <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">生成时间</th>
          <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">上次执行时间</th>
          <th class="px-6 py-3 text-center text-sm font-semibold text-gray-900">操作</th>
        </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
        <template v-if="currentPageData.length">
          <tr v-for="item in currentPageData" :key="item.id" class="hover:bg-gray-50">
            <td class="px-6 py-4">
              <a href="#" class="text-blue-600 hover:underline">{{ item.name }}</a>
            </td>
            <td class="px-6 py-4">
              <div class="max-w-[5em] overflow-hidden text-ellipsis whitespace-nowrap hover:overflow-visible hover:whitespace-normal hover:absolute hover:z-10 hover:bg-white hover:shadow-lg hover:p-2 hover:rounded-lg hover:border hover:min-w-[300px] hover:max-w-[400px]">{{ item.description }}</div>
            </td>
            <td class="px-6 py-4">
              <span class="rounded-full bg-blue-100 px-3 py-1 text-sm text-blue-800">{{ item.type }}</span>
            </td>
            <td class="px-6 py-4">
<span class="rounded-full px-3 py-1 text-sm" :class="{
'bg-gray-100 text-gray-800': item.status === 'unexecuted',
'bg-blue-100 text-blue-800': item.status === 'executing',
'bg-red-100 text-red-800': item.status === 'failed'
}">
{{
    item.status === 'unexecuted' ? '未执行' :
        item.status === 'executing' ? '执行中' : '执行失败'
  }}
</span>
            </td>
            <td class="px-6 py-4 text-sm text-gray-500">{{ item.createTime }}</td>
            <td class="px-6 py-4 text-sm text-gray-500">{{ item.lastExecuteTime }}</td>
            <td class="px-6 py-4">
              <div class="flex justify-center gap-3">
                <button class="!rounded-button text-gray-600" :class="{
'hover:text-green-600': item.status !== 'executing',
'hover:text-yellow-600': item.status === 'executing'
}" :title="item.status === 'executing' ? '暂停' : '执行'" @click="executeDataSource(item)">
                  <i class="fas" :class="{'fa-play': item.status !== 'executing', 'fa-pause': item.status === 'executing'}"></i>
                </button>
                <button class="!rounded-button text-gray-600 hover:text-red-600" title="删除">
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
            <button v-for="size in [10, 20, 50]" :key="size" @click="() => { pageSize = size; handlePageSizeChange(); showPageSizeOptions = false; }" class="w-full px-4 py-2 text-left text-sm hover:bg-blue-50" :class="{'text-blue-600 bg-blue-50': pageSize === size, 'text-gray-700': pageSize !== size}">
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
          <button @click="showCreateModal = false" class="!rounded-button text-gray-500 hover:text-gray-700">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <form @submit.prevent="handleCreateDataset" class="space-y-6">
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-700">数据集名称</label>
            <input
                v-model="newDataset.name"
                type="text"
                required
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
          <div v-if="newDataset.type === '远程文件'" class="space-y-4">
            <div>
              <label class="mb-2 block text-sm font-medium text-gray-700">远程资源地址</label>
              <input
                  v-model="newDataset.resourceUrl"
                  type="text"
                  class="!rounded-button w-full border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:ring-blue-500"
                  placeholder="请输入远程资源地址，例如：https://example.com/data.csv"
              >
            </div>
          </div>
          <div v-else-if="newDataset.type === '接口获取'" class="space-y-4">
            <div>
              <label class="mb-2 block text-sm font-medium text-gray-700">接口调用地址</label>
              <input
                  v-model="newDataset.apiUrl"
                  type="text"
                  class="!rounded-button w-full border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:ring-blue-500"
                  placeholder="请输入接口调用地址，例如：https://api.example.com/data"
              >
            </div>
            <div>
              <label class="mb-2 block text-sm font-medium text-gray-700">JSON 数据解析路径</label>
              <div class="space-y-2">
                <input
                    v-model="newDataset.jsonPath"
                    type="text"
                    class="!rounded-button w-full border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:ring-blue-500"
                    placeholder="请输入 JSON 解析路径，例如：data.list"
                >
                <div class="flex items-start gap-2">
                  <i class="fas fa-info-circle mt-1 text-blue-500"></i>
                  <p class="text-xs text-gray-500">
                    用点号分隔的路径表示，例如：data.items.list 表示解析 response.data.items.list 的数据。如果是根级别数组，直接留空即可。
                  </p>
                </div>
              </div>
            </div>
          </div>
          <div v-else>
            <div class="flex items-center justify-center rounded-lg border-2 border-dashed border-gray-300 p-6">
              <p class="text-sm text-gray-500">请先选择数据源类型</p>
            </div>
          </div>
          <div class="flex justify-end gap-3">
            <button
                type="button"
                @click="showCreateModal = false"
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
            <div>创建时间：{{ editingDataset?.createTime }}</div>
            <div>更新时间：{{ editingDataset?.updateTime }}</div>
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
          <h3 class="text-lg font-semibold">{{ selectedDataset?.name }} - 数据详情</h3>
          <button @click="showViewModal = false" class="!rounded-button text-gray-500 hover:text-gray-700">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="mb-4 overflow-x-auto">
          <table class="min-w-full table-auto">
            <thead class="bg-gray-50">
            <tr>
              <th v-for="header in datasetHeaders" :key="header" class="px-6 py-3 text-left text-sm font-semibold text-gray-900">
                {{ header }}
              </th>
            </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
            <template v-if="currentDetailPageData.length">
              <tr v-for="(row, index) in currentDetailPageData" :key="index" class="hover:bg-gray-50">
                <td v-for="header in datasetHeaders" :key="header" class="px-6 py-4 text-sm">
                  {{ row[header] }}
                </td>
              </tr>
            </template>
            <template v-else>
              <tr>
                <td :colspan="datasetHeaders.length" class="px-6 py-8 text-center">
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
                <button v-for="size in [5, 10, 20]" :key="size" @click="() => { detailPageSize = size; showDetailPageSizeOptions = false; }" class="w-full px-4 py-2 text-left text-sm hover:bg-blue-50" :class="{'text-blue-600 bg-blue-50': detailPageSize === size, 'text-gray-700': detailPageSize !== size}">
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
export default {
  data() {
    return {
      showCreateModal: false,
      showTypeFilter: false,
      showStatusFilter: false,
      showTypeSelect: false,
      selectedFile: null as File | null,
      fileInput: null as HTMLInputElement | null,
      newDataset: {
        name: '',
        type: '',
        description: '',
        resourceUrl: '',
        apiUrl: '',
        jsonPath: ''
      },
      showEditModal: false,
      editingDataset: null as Dataset | null,
      searchQuery: '',
      currentPage: 1,
      pageSize: 10,
      showViewModal: false,
      selectedDataset: null as any,
      detailCurrentPage: 1,
      detailPageSize: 5,
      showPageSizeOptions: false,
      showDetailPageSizeOptions: false,
      selectedTypes: [] as string[],
      selectedStatus: [] as string[],
      dataTypes: ['远程文件', '接口获取'],
      mockData: [
        {
          id: 1,
          name: 'AWS S3数据源',
          description: '存储在AWS S3上的历史订单数据文件，每日自动更新，用于订单分析和报表生成。',
          type: '远程文件',
          createTime: '2023-12-01 09:30:00',
          status: 'unexecuted',
          lastExecuteTime: '-'
        },
        {
          id: 2,
          name: '实时库存API',
          description: '连接仓储管理系统的实时库存数据接口，提供各仓库商品库存实时状态。',
          type: '接口获取',
          createTime: '2023-11-15 10:00:00',
          status: 'executing',
          lastExecuteTime: '2023-12-15 14:30:00'
        },
        {
          id: 3,
          name: 'FTP日志文件',
          description: '通过FTP服务器获取的系统运行日志文件，用于系统监控和性能分析。',
          type: '远程文件',
          createTime: '2023-10-20 14:15:00',
          status: 'failed',
          lastExecuteTime: '2023-12-15 10:15:00'
        },
        {
          id: 4,
          name: '支付系统API',
          description: '对接支付系统的交易数据接口，实时获取交易流水和支付状态信息。',
          type: '接口获取',
          createTime: '2023-09-30 16:20:00',
          status: 'unexecuted',
          lastExecuteTime: '-'
        },
        {
          id: 5,
          name: 'HDFS客户数据',
          description: '存储在Hadoop分布式文件系统中的客户信息文件，包含客户画像和行为数据。',
          type: '远程文件',
          createTime: '2023-09-01 11:45:00',
          status: 'executing',
          lastExecuteTime: '2023-12-15 15:45:00'
        }
      ],
      mockDetailData: [
        { id: 1, name: '张伟', age: 28, department: '销售部', performance: 95 },
        { id: 2, name: '李娜', age: 32, department: '市场部', performance: 88 },
        { id: 3, name: '王磊', age: 25, department: '技术部', performance: 92 },
        { id: 4, name: '刘芳', age: 30, department: '人事部', performance: 85 },
        { id: 5, name: '周鑫', age: 27, department: '销售部', performance: 90 },
        { id: 6, name: '赵琳', age: 29, department: '市场部', performance: 87 },
        { id: 7, name: '孙明', age: 31, department: '技术部', performance: 94 },
        { id: 8, name: '钱晓', age: 26, department: '人事部', performance: 89 }
      ],
      datasetHeaders: ['id', 'name', 'age', 'department', 'performance'],
    };
  },
  computed: {
    filteredData() {
      let result = [...this.mockData];
      if (this.selectedTypes.length > 0) {
        result = result.filter(item => this.selectedTypes.includes(item.type));
      }
      if (this.selectedStatus.length > 0) {
        result = result.filter(item => this.selectedStatus.includes(item.status));
      }
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        result = result.filter(item => item.name.toLowerCase().includes(query));
      }
      return result;
    },
    totalPages() {
      return Math.ceil(this.filteredData.length / this.pageSize);
    },
    currentPageData() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.filteredData.slice(start, end);
    },
    detailTotalPages() {
      return Math.ceil(this.mockDetailData.length / this.detailPageSize);
    },
    currentDetailPageData() {
      const start = (this.detailCurrentPage - 1) * this.detailPageSize;
      const end = start + this.detailPageSize;
      return this.mockDetailData.slice(start, end);
    }
  },
  methods: {
    handleFileChange(event: Event) {
      const input = event.target as HTMLInputElement;
      if (input.files && input.files[0]) {
        this.selectedFile = input.files[0];
      }
    },
    executeDataSource(dataSource: any) {
      const index = this.mockData.findIndex(item => item.id === dataSource.id);
      if (index !== -1) {
        if (this.mockData[index].status === 'executing') {
          this.mockData[index].status = 'unexecuted';
        } else {
          this.mockData[index].status = 'executing';
          this.mockData[index].lastExecuteTime = new Date().toLocaleString();
        }
      }
    },
    handleEditDataset() {
      if (!this.editingDataset) return;
      const index = this.mockData.findIndex(item => item.id === this.editingDataset?.id);
      if (index !== -1) {
        this.mockData[index] = {
          ...this.mockData[index],
          name: this.editingDataset.name,
          description: this.editingDataset.description,
          updateTime: new Date().toLocaleString()
        };
      }
      this.showEditModal = false;
      this.editingDataset = null;
    },
    handleCreateDataset() {
      if (this.newDataset.type === '远程文件' && !this.newDataset.resourceUrl) {
        alert('请输入远程资源地址');
        return;
      }
      if (this.newDataset.type === '接口获取' && !this.newDataset.apiUrl) {
        alert('请输入接口调用地址');
        return;
      }
      console.log('创建数据集：', {
        ...this.newDataset
      });
      this.newDataset = {
        name: '',
        type: '',
        description: '',
        resourceUrl: '',
        apiUrl: '',
        jsonPath: ''
      };
      this.showCreateModal = false;
    },
    handlePageSizeChange() {
      this.currentPage = 1;
    },
    toggleTypeFilter() {
      this.showTypeFilter = !this.showTypeFilter;
    },
    viewDataset(dataset: any) {
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
