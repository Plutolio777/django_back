<template>
  <div class="grid grid-cols-4 gap-6 mb-6">
    <div v-for="(stat, index) in stats"
         :key="index"
         class="bg-white rounded-xl p-6 shadow-sm">
      <div class="flex items-center justify-between mb-4">
        <span class="text-gray-600">{{ stat.name }}</span>
        <i :class="[stat.icon, 'text-blue-600']"></i>
      </div>
      <div class="text-2xl font-semibold">{{ stat.value }}</div>
      <div class="mt-2 text-sm">
        <span :class="stat.trend === '上升' ? 'text-green-500' : 'text-red-500'">
          <i :class="stat.trend === '上升' ? 'fas fa-arrow-up' : 'fas fa-arrow-down'"></i>
          {{ stat.percentage }}
        </span>
        <span class="text-gray-500 ml-1">较上周</span>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted} from 'vue';
import apiService from '@/api/apiService';

const loading = ref(true);
const stats = ref([]);

const loadStatsData = async () => {
  try {
    loading.value = true;
    // 初始化四个卡片数据
    stats.value = [
      { name: '总存储量', value: '加载中...', icon: 'fas fa-database', trend: '持平', percentage: '0%' },
      { name: '已标注数据集', value: '加载中...', icon: 'fas fa-check-circle', trend: '持平', percentage: '0%' },
      { name: '已清洗数据集', value: '加载中...', icon: 'fas fa-tasks', trend: '持平', percentage: '0%' },
      { name: '异常数据', value: '加载中...', icon: 'fas fa-exclamation-triangle', trend: '持平', percentage: '0%' }
    ];

    // 并行请求所有接口
    const [dataSizeRes, labelSizeRes, cleanedSizeRes, errorSizeRes] = await Promise.all([
      apiService.fetchDataSize().catch(() => null),
      apiService.fetchLabelSize().catch(() => null),
      apiService.fetchCleanedSize().catch(() => null),
      apiService.fetchErrorSize().catch(() => null)
    ]);

    // 分别处理每个接口响应
    if (dataSizeRes?.success) {
      stats.value[0] = {
        name: '总存储量',
        value: dataSizeRes.data.data.total_data_size_current_human_readable,
        icon: 'fas fa-database',
        trend: dataSizeRes.data.data.size_change_type === '没有变化' ? '持平' : dataSizeRes.data.data.size_change_type,
        percentage: dataSizeRes.data.data.size_change_percentage
      };
    }

    if (labelSizeRes?.success) {
      stats.value[1] = {
        name: '已标注数据集',
        value: labelSizeRes.data.data.total_label_data.toLocaleString(),
        icon: 'fas fa-check-circle',
        trend: labelSizeRes.data.data.size_change_type === '没有变化' ? '持平' : labelSizeRes.data.data.size_change_type,
        percentage: labelSizeRes.data.data.size_change_percentage
      };
    }

    if (cleanedSizeRes?.success) {
      stats.value[2] = {
        name: '已清洗数据集',
        value: cleanedSizeRes.data.data.total_cleaned_data.toLocaleString(),
        icon: 'fas fa-tasks',
        trend: cleanedSizeRes.data.data.size_change_type === '没有变化' ? '持平' : cleanedSizeRes.data.data.size_change_type,
        percentage: cleanedSizeRes.data.data.size_change_percentage
      };
    }

    if (errorSizeRes?.success) {
      stats.value[3] = {
        name: '异常数据',
        value: errorSizeRes.data.data.total_abnormal_label_data_current.toLocaleString(),
        icon: 'fas fa-exclamation-triangle',
        trend: errorSizeRes.data.data.size_change_type === '没有变化' ? '持平' : errorSizeRes.data.data.size_change_type,
        percentage: errorSizeRes.data.data.size_change_percentage
      };
    }
  } catch (error) {
    console.error('加载统计数据失败:', error);
  } finally {
    loading.value = false;
  }
};

defineExpose({
  loadStatsData
});

onMounted(() => {
  loadStatsData();
});
</script>
