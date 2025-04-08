<template>
  <div class="min-h-screen bg-gray-50 p-4 max-w-[1980px] mx-auto">
    <!-- 标题区域 -->
    <div class="mb-6 bg-gradient-to-r from-white to-blue-50 p-6 rounded-xl shadow-sm border border-gray-100">
      <div class="flex items-center gap-4">
        <div class="p-3 bg-blue-500 bg-opacity-10 rounded-xl">
          <i class="fas fa-clock text-2xl text-blue-600"></i>
        </div>
        <div>
          <h1 class="text-2xl font-bold bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent">标签组管理</h1>
          <p class="mt-2 text-gray-600">管理和组织系统标签，支持多级标签分组和灵活的标签应用</p>
        </div>
      </div>
      <div class="mt-4 flex gap-4">
        <div class="flex items-center gap-2">
          <div class="w-2 h-2 rounded-full bg-green-500"></div>
          <span class="text-gray-600">已启用标签：156</span>
        </div>
        <div class="flex items-center gap-2">
          <div class="w-2 h-2 rounded-full bg-blue-500"></div>
          <span class="text-gray-600">标签组：12</span>
        </div>
        <div class="flex items-center gap-2">
          <div class="w-2 h-2 rounded-full bg-purple-500"></div>
          <span class="text-gray-600">未启用：18</span>
        </div>
      </div>
    </div>
    <!-- 功能栏区域 -->
    <div class="mb-6 bg-white p-4 rounded-xl shadow-sm flex flex-wrap items-center justify-between gap-4">
      <div class="relative flex-1 max-w-md">
        <i class="fas fa-search absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
        <input
            v-model="searchQuery"
            type="text"
            placeholder="搜索标签组名称"
            class="!rounded-button w-full bg-gray-50 border border-gray-200 pl-11 pr-4 py-2.5 text-gray-700 placeholder-gray-400 focus:bg-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all duration-200"
        >
      </div>
    </div>
    <!-- 数据集列表 -->
    <div class="mb-6 overflow-x-auto rounded-lg bg-white shadow">
      <table class="min-w-full table-auto relative">
        <thead class="bg-gray-50 sticky top-0 z-10">
        <tr>
          <th class="w-16 px-6 py-3 text-left text-sm font-semibold text-gray-900 bg-gray-50 sticky left-0 z-20">序号</th>
          <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900 w-32">数据类型</th>
          <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">时频域特征</th>
        </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
        <template v-if="currentPageData.length">
          <tr v-for="(item, index) in currentPageData" :key="item.id" class="hover:bg-gray-50">
            <td class="w-16 px-6 py-4 bg-white sticky left-0 z-10">{{ index + 1 }}</td>
            <td class="px-6 py-4">
              <span class="rounded-full bg-blue-100 px-3 py-1 text-sm text-blue-800">{{ item.type }}</span>
            </td>
            <td class="px-6 py-4 text-sm text-gray-700">{{item.description}}</td>
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
  </div>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue';

const searchQuery = ref('');
const currentPage = ref(1);
const pageSize = ref(10);
const showPageSizeOptions = ref(false);

const mockData = [
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
  }
];

const filteredData = computed(() => {
  let result = [...mockData];
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    result = result.filter(item => item.type.toLowerCase().includes(query));
  }
  return result;
});

const totalPages = computed(() => Math.ceil(filteredData.value.length / pageSize.value));

const currentPageData = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  return filteredData.value.slice(start, end);
});

const handlePageSizeChange = () => {
  currentPage.value = 1;
};
</script>

<style scoped>
.custom-table__row:hover {
  background-color: rgba(0, 0, 0, 0.02);
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
</style>