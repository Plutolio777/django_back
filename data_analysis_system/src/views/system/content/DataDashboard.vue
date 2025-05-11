<!-- 代码已包含 CSS：使用 TailwindCSS , 安装 TailwindCSS 后方可看到布局样式效果 -->
<template>
  <div class="min-h-screen bg-gray-50">
    <main class="p-6">
      <!-- 统计卡片 -->
      <StatsCard />
      <!-- 图表区域 -->
      <div class="grid grid-cols-2 gap-6 mb-6">
        <div class="bg-white rounded-xl p-6 shadow-sm">
          <h3 class="text-lg font-medium mb-4">数据标注趋势</h3>
          <div ref="trendChart" class="h-80"></div>
        </div>
        <div class="bg-white rounded-xl p-6 shadow-sm">
          <h3 class="text-lg font-medium mb-4">标注类型统计</h3>
          <div ref="distributionChart" class="h-80"></div>
        </div>
      </div>
      <!-- 实时数据列表 -->
      <!-- <div class="bg-white rounded-xl p-6 shadow-sm">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-medium">实时处理数据</h3>
          <div class="flex gap-2">
            <button class="!rounded-button whitespace-nowrap px-3 py-1.5 bg-gray-100 text-gray-600 text-sm">
              <i class="fas fa-filter mr-2"></i>筛选
            </button>
            <button class="!rounded-button whitespace-nowrap px-3 py-1.5 bg-gray-100 text-gray-600 text-sm">
              <i class="fas fa-sync-alt mr-2"></i>刷新
            </button>
          </div>
        </div>
        <table class="w-full">
          <thead>
          <tr class="text-left text-gray-600 border-b">
            <th class="pb-3 font-medium">数据ID</th>
            <th class="pb-3 font-medium">类型</th>
            <th class="pb-3 font-medium">状态</th>
            <th class="pb-3 font-medium">处理时间</th>
            <th class="pb-3 font-medium">处理人</th>
            <th class="pb-3 font-medium">操作</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="(item, index) in realtimeData"
              :key="index"
              class="border-b last:border-none">
            <td class="py-4">{{ item.id }}</td>
            <td class="py-4">{{ item.type }}</td>
            <td class="py-4">
              <span :class="getStatusClass(item.status)">{{ item.status }}</span>
            </td>
            <td class="py-4">{{ item.time }}</td>
            <td class="py-4">{{ item.processor }}</td>
            <td class="py-4">
              <button class="!rounded-button whitespace-nowrap text-blue-600 hover:text-blue-700">
                <i class="fas fa-eye"></i>
              </button>
            </td>
          </tr>
          </tbody>
        </table>
      </div> -->
    </main>
  </div>
</template>
<script lang="ts" setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import * as echarts from 'echarts';
import apiService from '@/api/apiService';
import StatsCard from './StatsCard.vue';
const activeMenu = ref(0);
const trendChart = ref<HTMLElement | null>(null);
const distributionChart = ref<HTMLElement | null>(null);
onMounted(() => {
});
onBeforeUnmount(() => {
});
const menuItems = [
  { name: '数据概览', icon: 'fas fa-chart-pie' },
  { name: '标注管理', icon: 'fas fa-tags' },
  { name: '数据清洗', icon: 'fas fa-broom' },
  { name: '系统设置', icon: 'fas fa-cog' },
  { name: '用户权限', icon: 'fas fa-user-shield' },
  { name: '报表中心', icon: 'fas fa-file-alt' }
];
const statsCard = ref();
const realtimeData = [
  { id: 'BD2024020801', type: '时频标注', status: '已完成', time: '2024-02-08 14:30', processor: '张工程师' },
  { id: 'BD2024020802', type: '无监督标注', status: '处理中', time: '2024-02-08 14:25', processor: '李数据师' },
  { id: 'BD2024020803', type: '时频标注', status: '待处理', time: '2024-02-08 14:20', processor: '王分析师' },
  { id: 'BD2024020804', type: '无监督标注', status: '已完成', time: '2024-02-08 14:15', processor: '赵工程师' },
  { id: 'BD2024020805', type: '时频标注', status: '异常', time: '2024-02-08 14:10', processor: '刘数据师' }
];
const getStatusClass = (status: string) => {
  const classes = {
    '已完成': 'px-2 py-1 bg-green-50 text-green-600 rounded-full text-sm',
    '处理中': 'px-2 py-1 bg-blue-50 text-blue-600 rounded-full text-sm',
    '待处理': 'px-2 py-1 bg-gray-50 text-gray-600 rounded-full text-sm',
    '异常': 'px-2 py-1 bg-red-50 text-red-600 rounded-full text-sm'
  };
  return classes[status as keyof typeof classes];
};
const trendData = ref([]);
const loading = ref(true);

const fetchTrendData = async () => {
  try {
    const res = await apiService.fetchLabelTrendDaily();
    if (res.success) {
      trendData.value = res.data.datas;
      initTrendChart();
    }
  } catch (error) {
    console.error('获取标注趋势数据失败:', error);
  } finally {
    loading.value = false;
  }
};

const fetchLabelTypeData = async () => {
  try {
    const res = await apiService.fetchLabelTypeDistribution();
    if (res.success) {
      initDistributionChart(res.data);
    }
  } catch (error) {
    console.error('获取标注类型数据失败:', error);
  }
};

const initDistributionChart = (data) => {
  if (!distributionChart.value) return;
  
  const chart = echarts.init(distributionChart.value);
  
  // 检查是否有数据
  const hasData = data && (data.time_freq > 0 || data.unsupervised > 0);
  
  const option = {
    animation: false,
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      right: 10,
      top: 'center'
    },
    graphic: !hasData ? {
      type: 'text',
      left: 'center',
      top: 'middle',
      style: {
        text: '暂无数据',
        fill: '#999',
        fontSize: 16,
        fontWeight: 'bold'
      }
    } : undefined,
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: false
      },
      emphasis: {
        label: {
          show: true,
          fontSize: '14',
          fontWeight: 'bold'
        }
      },
      labelLine: {
        show: false
      },
      data: hasData ? [
        { value: data.time_freq, name: '时频标注' },
        { value: data.unsupervised, name: '无监督标注' }
      ] : []
    }]
  };
  chart.setOption(option);
  
  window.addEventListener('resize', () => {
    chart.resize();
  });
};

const initTrendChart = () => {
  if (!trendChart.value) return;
  
  const chart = echarts.init(trendChart.value);
  const option = {
    animation: false,
    tooltip: {
      trigger: 'axis'
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: trendData.value.map(item => item.date)
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '时频标注',
        type: 'line',
        smooth: true,
        data: trendData.value.map(item => item.time_freq),
        areaStyle: { opacity: 0.1 },
        lineStyle: { width: 3 },
        itemStyle: { color: '#3B82F6' }
      },
      {
        name: '无监督标注', 
        type: 'line',
        smooth: true,
        data: trendData.value.map(item => item.unsupervised),
        areaStyle: { opacity: 0.1 },
        lineStyle: { width: 3 },
        itemStyle: { color: '#10B981' }
      },
      {
        name: '总量',
        type: 'line',
        smooth: true,
        data: trendData.value.map(item => item.total),
        areaStyle: { opacity: 0.1 },
        lineStyle: { width: 3 },
        itemStyle: { color: '#F59E0B' }
      }
    ]
  };
  chart.setOption(option);
  
  window.addEventListener('resize', () => {
    chart.resize();
  });
};

onMounted(() => {
  fetchTrendData();
  fetchLabelTypeData();
});
</script>
<style scoped>
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}
input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
:deep(.fixed) {
  background-color: rgb(0 0 0 / 0.9);
}
</style>
