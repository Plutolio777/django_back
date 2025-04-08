<!-- 代码已包含 CSS：使用 TailwindCSS , 安装 TailwindCSS 后方可看到布局样式效果 -->
<template>
  <div class="min-h-screen bg-gray-50 p-4 max-w-[1980px] mx-auto">
    <!-- 标题区域 -->
    <div class="mb-6 bg-gradient-to-r from-white to-blue-50 p-6 rounded-xl shadow-sm border border-gray-100">
      <div class="flex items-center gap-4">
        <div class="p-3 bg-blue-500 bg-opacity-10 rounded-xl">
          <i class="fas fa-clock text-2xl text-blue-600"></i>
        </div>
        <div>
          <h1 class="text-2xl font-bold bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent">
            时频标注</h1>
          <p class="mt-2 text-gray-600">对时序数据进行时频分析和标注，支持多种数据源和数据集的处理</p>
        </div>
      </div>
      <div class="mt-4 flex gap-4">
        <div class="flex items-center gap-2">
          <div class="w-2 h-2 rounded-full bg-green-500"></div>
          <span class="text-gray-600">已完成标注：42</span>
        </div>
        <div class="flex items-center gap-2">
          <div class="w-2 h-2 rounded-full bg-blue-500"></div>
          <span class="text-gray-600">进行中：15</span>
        </div>
        <div class="flex items-center gap-2">
          <div class="w-2 h-2 rounded-full bg-purple-500"></div>
          <span class="text-gray-600">未执行：23</span>
        </div>
      </div>
    </div>
    <!-- 功能栏区域 -->
    <div class="mb-6 bg-white p-4 rounded-xl shadow-sm flex flex-wrap items-center justify-between gap-4">
      <div class="flex items-center gap-4">
        <button @click="goToDatSet"
                class="!rounded-button flex items-center gap-2 bg-gradient-to-r from-blue-600 to-blue-700 px-5 py-2.5 text-white hover:from-blue-700 hover:to-blue-800 transition-all duration-200 shadow-sm">
          <i class="fas fa-plus text-white/90"></i>
          <span class="whitespace-nowrap font-medium">前往添加数据集</span>
        </button>
        <div class="flex gap-4">
          <div class="relative">
            <button @click="showDataTypeFilter = !showDataTypeFilter"
                    class="!rounded-button flex items-center gap-2 bg-gray-50 border-gray-200 border px-4 py-2.5 text-gray-700 hover:bg-gray-100 transition-all duration-200">
              <i class="fas fa-database text-gray-500"></i>
              <span class="whitespace-nowrap">数据类型</span>
              <i class="fas fa-chevron-down text-gray-400 text-xs ml-1"></i>
            </button>
            <div v-if="showDataTypeFilter"
                 class="absolute left-0 top-full z-10 mt-2 w-56 rounded-xl border border-gray-200 bg-white p-3 shadow-lg">
              <div v-for="type in dataTypes" :key="type"
                   class="flex items-center gap-3 p-2 hover:bg-gray-50 rounded-lg transition-colors cursor-pointer">
                <input type="checkbox" :value="type" v-model="selectedDataTypes"
                       class="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500">
                <span class="text-gray-700">{{ type }}</span>
              </div>
            </div>
          </div>
          <div class="relative">
            <button @click="showStatusFilter = !showStatusFilter"
                    class="!rounded-button flex items-center gap-2 bg-gray-50 border-gray-200 border px-4 py-2.5 text-gray-700 hover:bg-gray-100 transition-all duration-200">
              <i class="fas fa-clock text-gray-500"></i>
              <span class="whitespace-nowrap">执行状态</span>
              <i class="fas fa-chevron-down text-gray-400 text-xs ml-1"></i>
            </button>
            <div v-if="showStatusFilter"
                 class="absolute left-0 top-full z-10 mt-2 w-56 rounded-xl border border-gray-200 bg-white p-3 shadow-lg">
              <div v-for="status in ['executing', 'unexecuted', 'completed']" :key="status"
                   class="flex items-center gap-3 p-2 hover:bg-gray-50 rounded-lg transition-colors cursor-pointer">
                <input type="checkbox" :value="status" v-model="selectedStatus"
                       class="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500">
                <span class="text-gray-700">{{
                    status === 'unexecuted' ? '未执行' : status === 'executing' ? '执行中' : '已完成'
                  }}</span>
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
            placeholder="搜索数据名称"
            class="!rounded-button w-full bg-gray-50 border border-gray-200 pl-11 pr-4 py-2.5 text-gray-700 placeholder-gray-400 focus:bg-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all duration-200"
        >
      </div>
    </div>
    <!-- 数据集列表 -->
    <div class="mb-6 overflow-x-auto rounded-lg bg-white shadow">
      <table class="min-w-full table-auto relative">
        <thead class="bg-gray-50 sticky top-0">
        <tr>
          <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900 bg-gray-50 sticky left-0 z-20">数据源名称
          </th>
          <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">数据集类型</th>
          <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">数据类型</th>
          <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">描述</th>
          <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">状态</th>
          <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">生成时间</th>
          <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">上次执行时间</th>
          <th class="px-6 py-3 text-center text-sm font-semibold text-gray-900 bg-gray-50 sticky right-0 z-20">操作</th>
        </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
        <template v-if="total>0">
          <tr v-for="item in dataLabelList" :key="item.id" class="hover:bg-gray-50">
            <!--     数据集名称       -->
            <td class="px-6 py-4 bg-white sticky left-0 z-10">
              <a href="#" class="text-blue-600 hover:underline">{{ item.dataset.name }}</a>
            </td>
            <!--     数据集类型       -->
            <td class="px-6 py-4">
              <span class="rounded-full bg-blue-100 px-3 py-1 text-sm text-blue-800">{{ item.dataset.data_source_type }}</span>
            </td>
            <!--     数据集类型       -->
            <td class="px-6 py-4">
              <span class="rounded-full bg-blue-100 px-3 py-1 text-sm text-blue-800">{{ item.dataset.type }}</span>
            </td>
            <!--     数据集描述       -->
            <td class="px-6 py-4">
              <div
                  class="max-w-[5em] overflow-hidden text-ellipsis whitespace-nowrap hover:overflow-visible hover:whitespace-normal hover:absolute hover:z-10 hover:bg-white hover:shadow-lg hover:p-2 hover:rounded-lg hover:border hover:min-w-[300px] hover:max-w-[400px]">
                {{ item.dataset.description }}
              </div>
            </td>
            <!--     状态       -->
            <td class="px-6 py-4">
              <!--     执行中显示进度条       -->
              <div v-if="item.status === '执行中'" class="relative">
                <div class="flex items-center justify-between mb-1">
                  <span class="text-sm text-blue-600 font-medium">执行中</span>
                  <span class="text-sm text-blue-600 font-medium">{{ item.progress || 0 }}%</span>
                </div>
                <div class="w-full bg-gray-100 rounded-full h-2">
                  <div
                      class="bg-gradient-to-r from-blue-400 to-blue-600 h-2 rounded-full transition-all duration-300 relative overflow-hidden"
                      :style="{ width: (item.progress || 0) + '%' }"
                  >
                    <div class="absolute inset-0 bg-white/30 animate-[progressPulse_1s_ease-in-out_infinite]"></div>
                  </div>
                </div>
              </div>
              <!--     其他显示标签       -->
              <span v-else class="rounded-full px-3 py-1 text-sm" :class="{
                'bg-gray-100 text-gray-800': item.status === '未执行',
                'bg-red-100 text-red-800': item.status === '执行失败',
                'bg-green-100 text-green-800': item.status === '已执行'
                }">
                {{ item.status }}
              </span>
            </td>
            <!--     任务生成时间       -->
            <td class="px-6 py-4 text-sm text-gray-500">{{ item.label_create_time }}</td>
            <!--     上次执行时间       -->
            <td class="px-6 py-4 text-sm text-gray-500">{{ item.task_execute_time || "" }}</td>
            <!--     操作栏       -->
            <td class="px-6 py-4 bg-white sticky right-0 z-10">
              <div class="flex justify-center gap-3">
                <!--     执行按钮       -->
                <button class="!rounded-button text-gray-600" :class="{
                    'hover:text-green-600': item.status === '未执行',
                    'hover:text-yellow-600': item.status === '执行中'
                    }" :title="item.status === '执行中' ? '暂停' : '执行'" @click="toBeExecuteTask(item)">
                  <i class="fas"
                     :class="{'fa-play': item.status !== '执行中', 'fa-pause': item.status === '执行中'}"></i>
                </button>

                <!-- 查看按钮 -->
                <button class="!rounded-button"
                        :class="{
          'text-gray-300 cursor-not-allowed': item.status !== '已执行',
          'text-gray-600 hover:text-blue-600': item.status === '已执行'
        }"
                        :title="item.status !== '已执行' ? '请先执行任务' : '查看'"
                        :disabled="item.status !== '已执行'"
                        @click="item.status === '已执行' && viewDataset(item)">
                  <i class="fas fa-eye"></i>
                </button>

                <!-- 下载按钮 -->
                <button class="!rounded-button"
                        :class="{
          'text-gray-300 cursor-not-allowed': item.status !== '已执行',
          'text-gray-600 hover:text-green-600': item.status === '已执行'
        }"
                        :title="item.status !== '已执行' ? '请先执行任务' : '下载'"
                        :disabled="item.status !== '已执行'"
                        @click="item.status === '已执行' && downloadItem(item)">
                  <i class="fas fa-download"></i>
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
          <button @click="showPageSizeOptions = !showPageSizeOptions"
                  class="!rounded-button flex items-center gap-2 border border-gray-200 px-3 py-1.5 text-sm hover:bg-gray-50">
            <span>{{ pageSize }}</span>
            <i class="fas fa-chevron-down text-gray-400 text-xs"></i>
          </button>
          <div v-if="showPageSizeOptions"
               class="absolute left-0 top-full z-10 mt-1 w-20 rounded-lg border border-gray-200 bg-white py-1 shadow-lg">
            <button v-for="size in [10, 20, 50]" :key="size"
                    @click="() => { pageSize = size; handlePageSizeChange(); showPageSizeOptions = false; }"
                    class="w-full px-4 py-2 text-left text-sm hover:bg-blue-50"
                    :class="{'text-blue-600 bg-blue-50': pageSize === size, 'text-gray-700': pageSize !== size}">
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
    <!-- 数据集查看弹窗 -->
    <div v-if="showViewModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div class="w-11/12 max-w-6xl max-h-[90vh] rounded-xl bg-white p-8 overflow-y-auto">
        <div class="mb-6 flex items-center justify-between">
          <h3 class="text-2xl font-semibold text-gray-800">{{ selectedDataset?.dataset.name }}</h3>
          <button @click="showViewModal = false"
                  class="!rounded-button p-2 text-gray-400 hover:text-gray-600 transition-colors">
            <i class="fas fa-times text-xl"></i>
          </button>
        </div>
        <!-- 基本信息展示区域 -->
        <div
            class="mb-8 grid grid-cols-1 md:grid-cols-2 gap-8 p-6 bg-gradient-to-br from-blue-50/50 to-transparent rounded-xl border border-blue-100">
          <div class="space-y-6">
            <div>
              <h4 class="text-sm font-medium text-gray-500 mb-2">数据源类型</h4>
              <div class="flex items-center gap-2">
                <i class="fas fa-database text-blue-500"></i>
                <span class="text-gray-700">{{ selectedDataset?.dataset.type }}</span>
              </div>
            </div>
            <div>
              <h4 class="text-sm font-medium text-gray-500 mb-2">描述信息</h4>
              <p class="text-gray-700">{{ selectedDataset?.dataset.description }}</p>
            </div>
            <div>
              <h4 class="text-sm font-medium text-gray-500 mb-2">执行状态</h4>
              <span class="inline-flex items-center px-3 py-1 rounded-full text-sm"
                    :class="{
                      'bg-blue-100 text-blue-800': selectedDataset?.status === '执行中',
                      'bg-gray-100 text-gray-800': selectedDataset?.status === '已执行',
                      'bg-red-100 text-red-800': selectedDataset?.status === '执行失败',
                      'bg-green-100 text-green-800': selectedDataset.status === '已执行'
              }">
                <i class="fas"
                   :class="{
                  'fa-play': selectedDataset?.status === '未执行',
                  'fa-spinner fa-spin': selectedDataset?.status === '执行中',
                  'fa-exclamation-circle': selectedDataset?.status === '执行失败',
                  'fa-thumbs-up': selectedDataset?.status === '已执行'
                  }">
                </i>
                <span class="ml-2">{{
                    selectedDataset?.status
                  }}</span>
            </span>
            </div>
          </div>
          <div class="space-y-6">
            <div>
              <h4 class="text-sm font-medium text-gray-500 mb-2">创建时间</h4>
              <div class="flex items-center gap-2">
                <i class="fas fa-calendar text-blue-500"></i>
                <span class="text-gray-700">{{ selectedDataset?.label_create_time }}</span>
              </div>
            </div>
            <div>
              <h4 class="text-sm font-medium text-gray-500 mb-2">最后执行时间</h4>
              <div class="flex items-center gap-2">
                <i class="fas fa-clock text-blue-500"></i>
                <span class="text-gray-700">{{ selectedDataset?.task_execute_time }}</span>
              </div>
            </div>
            <div>
              <h4 class="text-sm font-medium text-gray-500 mb-2">数据量</h4>
              <div class="flex items-center gap-2">
                <i class="fas fa-chart-bar text-blue-500"></i>
                <span class="text-gray-700">{{ selectedDataset?.result_file_size }} 条记录</span>
              </div>
            </div>
          </div>
        </div>
        <!-- 图片墙区域 -->
        <div class="mb-8">
          <h4 class="text-lg font-medium text-gray-700 mb-4">数据可视化展示</h4>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div v-for="(image, index) in selectedDataset?.pictures_walet"
                 :key="index"
                 class="relative group rounded-xl overflow-hidden shadow-sm hover:shadow-md transition-shadow duration-300"
                 :class="{
                  'md:col-span-2 md:row-span-2': index === 0,
                  'col-span-1': index !== 0
                  }">
              <img :src="image.url"
                   :alt="image.title"
                   class="w-full h-full object-cover">
              <div
                  class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-end p-4">
                <span class="text-white text-sm font-medium">{{ image.title }}</span>
              </div>
            </div>
          </div>
        </div>
        <!--        <div class="mb-8">-->
        <!--          <h4 class="text-lg font-medium text-gray-700 mb-4">数据可视化展示</h4>-->
        <!--          <div class="relative pb-10 w-full">-->
        <!--            <swiper :modules="swiperModules" :slides-per-view="6"-->
        <!--            :space-between="20"-->
        <!--            :pagination="{ clickable: true, dynamicBullets: true, el: '.swiper-custom-pagination' }"-->
        <!--            :navigation="{ nextEl: '.swiper-button-next', prevEl: '.swiper-button-prev' }"-->
        <!--            :breakpoints="{-->
        <!--            320: { slidesPerView: 1, spaceBetween: 10 },-->
        <!--            640: { slidesPerView: 2, spaceBetween: 15 },-->
        <!--            768: { slidesPerView: 3, spaceBetween: 20 },-->
        <!--            1024: { slidesPerView: 4, spaceBetween: 20 }-->
        <!--            }"-->
        <!--            :autoplay="{ delay: 3000, disableOnInteraction: false }"-->
        <!--            class="w-full h-[300px]"-->
        <!--            >-->
        <!--            <swiper-slide-->
        <!--                v-for="(image, index) in selectedDataset?.pictures_walet"-->
        <!--                :key="index"-->
        <!--                class="flex-shrink-0 h-100 w-100"-->
        <!--            >-->
        <!--            <div class="relative h-100 w-100 group rounded-xl overflow-hidden shadow-sm hover:shadow-md transition-shadow duration-300">-->
        <!--              <img-->
        <!--                  :src="image.url"-->
        <!--                  :alt="image.title"-->
        <!--                  class="w-100 h-100 object-cover"-->
        <!--              >-->
        <!--              <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-end p-4">-->
        <!--                <span class="text-white text-sm font-medium">{{ image.title }}</span>-->
        <!--              </div>-->
        <!--            </div>-->
        <!--            </swiper-slide>-->
        <!--            </swiper>-->
        <!--            &lt;!&ndash; 导航按钮和分页器保持不变 &ndash;&gt;-->
        <!--          </div>-->
        <!--        </div>-->

        <div class="mb-4 overflow-x-auto">
          <table class="min-w-full table-auto">
            <thead class="bg-gray-50">
            <tr>
              <th v-for="header in datasetHeaders" :key="header"
                  class="px-6 py-3 text-left text-sm font-semibold text-gray-900">
                {{ header }}
              </th>
            </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
            <template v-if="currentDetailPageData.length">
              <tr v-for="(row, index) in currentDetailPageData" :key="index" class="hover:bg-gray-50">
                <td class="px-6 py-4 text-sm">
                  <a :href=row.FilePath target="_blank" class="text-blue-600 hover:underline">{{ row.FileName }}</a>
                </td>
                <td class="px-6 py-4 text-sm">
                  {{ row.Label }}
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
              <button @click="showDetailPageSizeOptions = !showDetailPageSizeOptions"
                      class="!rounded-button flex items-center gap-2 border border-gray-200 px-3 py-1.5 text-sm hover:bg-gray-50">
                <span>{{ detailPageSize }}</span>
                <i class="fas fa-chevron-down text-gray-400 text-xs"></i>
              </button>
              <div v-if="showDetailPageSizeOptions"
                   class="absolute left-0 top-full z-10 mt-1 w-20 rounded-lg border border-gray-200 bg-white py-1 shadow-lg">
                <button v-for="size in [5, 10, 20]" :key="size"
                        @click="() => { detailPageSize = size; showDetailPageSizeOptions = false; }"
                        class="w-full px-4 py-2 text-left text-sm hover:bg-blue-50"
                        :class="{'text-blue-600 bg-blue-50': detailPageSize === size, 'text-gray-700': detailPageSize !== size}">
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
    <!-- 执行任务选择弹窗 -->
    <div v-if="showExecuteModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">
      <div class="w-11/12 max-w-2xl rounded-xl bg-white shadow-xl flex flex-col max-h-[90vh]">
        <div class="p-6 border-b border-gray-100">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-50">
                <i class="fas fa-tasks text-xl text-blue-500"></i>
              </div>
              <div>
                <h3 class="text-xl font-semibold text-gray-900">选择执行任务</h3>
                <p class="mt-1 text-sm text-gray-500">请从下列任务中选择需要执行的内容</p>
              </div>
            </div>
            <button @click="showExecuteModal = false" class="!rounded-button p-2 text-gray-400 hover:text-gray-600 transition-colors">
              <i class="fas fa-times text-xl"></i>
            </button>
          </div>
        </div>
        <div class="flex-1 overflow-y-auto p-6 space-y-3">
          <div v-for="task in marTypeList" :key="task.id" class="group relative">
            <label class="flex cursor-pointer items-center gap-4 rounded-xl border border-gray-100 bg-white p-4 shadow-sm transition-all duration-200 hover:border-blue-100 hover:bg-blue-50/30">
              <input
                  type="checkbox"
                  :value="task.id"
                  v-model="selectedTaskIds"
                  class="h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              >
              <div class="flex-1">
                <div class="flex items-center gap-3">
                  <span class="text-sm font-medium text-gray-900">{{ task.type }}</span>
                  <span class="rounded-full bg-blue-50 px-2.5 py-0.5 text-xs font-medium text-blue-600">任务 #{{ task.id }}</span>
                </div>
                <p class="mt-1 text-sm text-gray-500">{{ task.description }}</p>
              </div>
              <div class="flex items-center gap-2 opacity-0 transition-opacity group-hover:opacity-100">
                <button class="!rounded-button p-2 text-gray-400 hover:text-blue-600" title="查看详情">
                  <i class="fas fa-info-circle"></i>
                </button>
                <button class="!rounded-button p-2 text-gray-400 hover:text-green-600" title="预览">
                  <i class="fas fa-eye"></i>
                </button>
              </div>
            </label>
          </div>
        </div>
        <div class="flex items-center justify-between border-t border-gray-100 p-6">
          <div class="flex items-center gap-2 text-sm text-gray-500">
            <i class="fas fa-info-circle text-blue-500"></i>
            <span>已选择 {{ selectedTaskIds.length }} 个任务</span>
          </div>
          <div class="flex justify-end gap-3">
            <button
                type="button"
                @click="showExecuteModal = false"
                class="!rounded-button border border-gray-200 px-5 py-2.5 text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors"
            >
              取消
            </button>
            <button
                type="button"
                @click="executeTask"
                :disabled="selectedTaskIds.length === 0"
                class="!rounded-button bg-gradient-to-r from-blue-600 to-blue-700 px-5 py-2.5 text-sm font-medium text-white hover:from-blue-700 hover:to-blue-800 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-sm"
            >
              确认执行
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
    this.pageSize = 10;
    this.currentPage = 1;
    this.selectedDataset = {};
    this.selectedTypes = [];
    this.selectedStatus = []
    this.searchQuery = "";
    this.fetchDataLabel()
  },
  data() {
    return {
      // 显示弹窗状态
      showCreateModal: false,
      showTypeFilter: false,
      showStatusFilter: false,
      showTypeSelect: false,
      showEditModal: false,
      showViewModal: false,
      selectedFile: null,
      fileInput: null,
      newDataset: {
        name: '',
        type: '',
        description: '',
        resourceUrl: '',
        apiUrl: '',
        jsonPath: ''
      },
      editingDataset: null,
      searchQuery: '',
      currentPage: 1,
      pageSize: 10,
      selectedTypes: [],
      selectedStatus: [],
      dataTypes: ['远程文件', '接口获取'],
      datasetStats: {totalRecords: 2547},
      datasetHeaders: ['FileName', "Label"],
      detailCurrentPage: 1,
      detailPageSize: 5,
      showPageSizeOptions: false,
      showDetailPageSizeOptions: false,
      // dataLabelList: [],
      total: 0,
      showDataTypeFilter: false,
      selectedDataTypes: [],
      dataLabelList: [],
      pollingControllers: {},
      selectedDataset: {},
      executingDataSource: {},
      showExecuteModal: false,
      selectedTaskIds: [],
      marTypeList:[
        {
          id: 1,
          type: '正常',
          description:"能量集中在结构的模态频率附近。"
        },
        {
          id: 2,
          type: '缺失',
          description:"频谱能量几乎全部集中在低频区域(接近0频率)，高频部分能量快速衰减直至消失。"
        },
        {
          id: 3,
          type: '次小',
          description:"能量主要集中在低频区域，高频部分的能量极低，整体特征较弱。"
        },
        {
          id: 4,
          type: '方波',
          description:"能量主要集中在低频区域，并随着频率增加逐渐衰减，展现出阶梯状分布。"
        },
        {
          id: 5,
          type: '趋势',
          description:"时频图中的能量分布随时间变化，表现出明显的趋势项。"
        },
        {
          id: 6,
          type: '漂移',
          description:"能量主要集中在漂移发生的时间段，呈现随时间漂移的特征。"
        },{
          id: 7,
          type: '伪正常',
          description:"时频图中的能量分布无规律，结构模态频率无法清晰辨识，噪声占据主导。"
        },
      ]
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.total / this.pageSize);
    },
    detailTotalPages() {
      return Math.ceil(this.selectedDataset.result_file_content.length / this.detailPageSize);
    },
    currentDetailPageData() {
      const start = (this.detailCurrentPage - 1) * this.detailPageSize;
      const end = start + this.detailPageSize;
      return this.selectedDataset.result_file_content.slice(start, end);
    }
  },
  watch: {
    pageSize: "fetchDataLabel",
    currentPage: "fetchDataLabel"
  },
  beforeUnmount() {
    // 组件卸载时取消所有轮询
    console.log("取消所有轮训")
    Object.values(this.pollingControllers).forEach(controller => {
      console.log(controller)
      controller.abort()
    })
  },
  methods: {
    // 下载项目
    async downloadItem(dataset) {
      try {
        // 检查状态是否为"已执行"，这里双重确认（虽然按钮已经做了限制）
        if (dataset.status !== '已执行') {
          this.$message.warning('请先执行任务再下载')
          return
        }

        // 获取接口
        let response = await apiService.fetchUnsupervisedMarkTaskProgressDetail({}, {task_id: dataset.id});
        if (response.success) {
          let url = response.data.data.result_file;
          const link = document.createElement('a')
          link.href = url
          link.setAttribute('download', "classification_results_1.xlsx")
          document.body.appendChild(link)
          link.click()
          // 清理
          link.remove()

        }else {
          this.$message({type: "error", message:"下载失败"})
        }
      } catch (error) {
        console.error('下载失败:', error)
        this.$message.error('下载失败: ' + (error.response?.data?.message || error.message))
      }
    },
    goToDatSet(){
      this.$router.push({ name: 'system_home' });
    },
    toBeExecuteTask(task){
      this.executingDataSource = task;
      this.showExecuteModal = true;
    },
    async executeTask() {

      let data = {
        "task_id": this.executingDataSource.id,
        "label": this.selectedTaskIds.join(','),
      }
      let response = await apiService.executeUnsupervisedMarkTask(data);
      if (response.success) {
        this.$message({
          type: "success",
          message: "任务提交成功！"
        })
        this.fetchDataLabel();
      } else {
        this.$message({
          type: "error",
          message: "任务执行失败"
        })
      }
    },
    async fetchDataLabel() {
      let params = {
        limit: this.pageSize,
        offset: (this.currentPage - 1) * this.pageSize,
      }
      if (this.selectedTypes.length > 0) {
        params["type"] = this.selectedTypes.join(',');
      }
      if (this.selectedStatus.length > 0) {
        params["status"] = this.selectedStatus.join(',');
      }
      if (this.searchQuery) {
        params["name"] = this.searchQuery;
      }

      let response = await apiService.fetchUnsupervisedDataLabelList({}, params);
      if (response.success) {
        this.total = response.data.data.count;
        this.dataLabelList = response.data.data.results;
        // 检查是否存在待轮训任务
        for (const task of this.dataLabelList) {
          if (task.status === "执行中") {
            this.startPolling(task, task.id)
          }
        }
      } else {
        this.$message({
          type: "error",
          message: "数据集加载失败"
        })
      }
    },

    // 开始轮询任务进度
    startPolling(task, taskId) {
      if (task.id in this.pollingControllers) {
        this.pollingControllers[task.id].abort() // 先中止旧的
        delete this.pollingControllers[task.id]
      } else {
        const controller = new AbortController()
        this.pollingControllers[task.id] = controller

        const poll = async () => {
          // 每次轮询前检查是否已中止
          if (controller.signal.aborted) return
          let index = this.dataLabelList.findIndex(t => t.id === task.id)

          try {
            let response = await apiService.fetchUnsupervisedMarkTaskProgress({}, {"task_id": task.id})
            if (!response.success) throw new Error('请求失败')
            // 更新进度
            if (index !== -1) {
              this.dataLabelList[index].progress = response.data.data.progress
            }
            console.log(response.data.data.progress)
            // 检查是否完成
            if (response.data.data.progress >= 100|| ['已执行', '执行失败'].includes(response.data.data.status)) {
              this.dataLabelList[index].status = response.data.data.status
              delete this.pollingControllers[task.id]
            } else {
              // 继续轮询
              setTimeout(poll, 2000)
            }
          } catch (error) {
            if (error.name !== 'AbortError') {
              this.$message({"type": "error", message: `任务${task.id}轮询失败:`, error})
              delete this.pollingControllers[task.id]
            }
          }
        }

        // 开始轮询
        poll()
      }
    },
    // 停止任务
    stopTask(item) {
      const controller = this.pollingControllers[item.id]
      if (controller) {
        controller.abort()
        this.$set(item, 'status', '执行失败')
        delete this.pollingControllers[item.id]
      }
    },
    handlePageSizeChange() {
      this.currentPage = 1;
    },
    async viewDataset(dataset) {
      let response = await apiService.fetchUnsupervisedMarkTaskProgressDetail({}, {task_id: dataset.id});
      if (response.success) {
        this.selectedDataset = response.data.data;
        this.showViewModal = true;
        this.detailCurrentPage = 1;
      }else {
        this.$message({type: "error", message:"查询失败"})
      }


    }
  }
};
</script>
<style scoped>
.swiper-button-next::after,
.swiper-button-prev::after {
  display: none;
}

:deep(.swiper-custom-pagination) {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  gap: 8px;
  padding: 0;
}

:deep(.swiper-custom-pagination .swiper-pagination-bullet) {
  width: 8px;
  height: 8px;
  background: rgba(0, 0, 0, 0.2);
  opacity: 1;
  border-radius: 4px;
  transition: all 0.3s ease;
}

:deep(.swiper-custom-pagination .swiper-pagination-bullet-active) {
  width: 24px;
  background: #3b82f6;
}
.custom-table__row:hover {
  background-color: rgba(0, 0, 0, 0.02);
}
input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
::-webkit-scrollbar {
  height: 6px;
  width: 6px;
}
::-webkit-scrollbar-thumb {
  background-color: #d1d5db;
  border-radius: 3px;
}
::-webkit-scrollbar-track {
  background-color: #f3f4f6;
}
@keyframes progressPulse {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}
</style>
