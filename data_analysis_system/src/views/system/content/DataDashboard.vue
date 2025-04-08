<!-- 代码已包含 CSS：使用 TailwindCSS , 安装 TailwindCSS 后方可看到布局样式效果 -->
<template>
  <div class="min-h-screen bg-gray-50">
    <main class="p-6">
      <!-- 统计卡片 -->
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
      <!-- 3D模型展示区域 -->
      <div class="bg-white rounded-xl p-6 shadow-sm mb-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-medium">3D 模型预览</h3>
          <div class="flex gap-2">
            <button class="!rounded-button whitespace-nowrap px-3 py-1.5 bg-gray-100 text-gray-600 text-sm">
              <i class="fas fa-cube mr-2"></i>切换模型
            </button>
            <button @click="enterFullscreen" class="!rounded-button whitespace-nowrap px-3 py-1.5 bg-blue-600 text-white text-sm">
              <i class="fas fa-expand-arrows-alt mr-2"></i>全屏查看
            </button>
          </div>
        </div>
        <div
            class="w-full aspect-[2/1] rounded-xl overflow-hidden shadow-sm relative group cursor-pointer"
            :class="{'fixed inset-0 z-[100] !rounded-none': isFullscreen}"
        >
          <div class="absolute top-4 right-4 z-10" v-if="isFullscreen">
            <button @click="exitFullscreen" class="!rounded-button whitespace-nowrap px-3 py-1.5 bg-gray-800 bg-opacity-50 text-white text-sm hover:bg-opacity-70">
              <i class="fas fa-compress-alt mr-2"></i>退出全屏
            </button>
          </div>
          <img src="https://ai-public.mastergo.com/ai/img_res/2345cfe07d14515d97455ffdfb8e14a8.jpg"
               alt="桥梁模型"
               :class="{'w-full h-full object-contain': isFullscreen, 'w-full h-full object-cover': !isFullscreen}">
          <div class="absolute inset-0 bg-black bg-opacity-40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center"
               :class="{'!bg-opacity-60': isFullscreen}">
            <div class="text-white text-center">
              <p class="font-medium mb-2">斜拉桥模型 2024版</p>
              <p class="text-sm text-gray-200">最后更新: 2024-02-08</p>
            </div>
          </div>
        </div>
      </div>
      <!-- 实时数据列表 -->
      <div class="bg-white rounded-xl p-6 shadow-sm">
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
      </div>
    </main>
  </div>
</template>
<script lang="ts" setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import * as echarts from 'echarts';
const activeMenu = ref(0);
const trendChart = ref<HTMLElement | null>(null);
const distributionChart = ref<HTMLElement | null>(null);
const isFullscreen = ref(false);
const enterFullscreen = () => {
  isFullscreen.value = true;
  document.body.style.overflow = 'hidden';
};
const exitFullscreen = () => {
  isFullscreen.value = false;
  document.body.style.overflow = '';
};
const handleEscKey = (event: KeyboardEvent) => {
  if (event.key === 'Escape' && isFullscreen.value) {
    exitFullscreen();
  }
};
onMounted(() => {
  document.addEventListener('keydown', handleEscKey);
});
onBeforeUnmount(() => {
  document.removeEventListener('keydown', handleEscKey);
});
const menuItems = [
  { name: '数据概览', icon: 'fas fa-chart-pie' },
  { name: '标注管理', icon: 'fas fa-tags' },
  { name: '数据清洗', icon: 'fas fa-broom' },
  { name: '系统设置', icon: 'fas fa-cog' },
  { name: '用户权限', icon: 'fas fa-user-shield' },
  { name: '报表中心', icon: 'fas fa-file-alt' }
];
const stats = [
  { name: '总存储量', value: '125,430', icon: 'fas fa-database', trend: '上升', percentage: '15%' },
  { name: '已标注数据集', value: '98,342', icon: 'fas fa-check-circle', trend: '上升', percentage: '12%' },
  { name: '已清洗数据集', value: '78,342', icon: 'fas fa-tasks', trend: '上升', percentage: '8%' },
  { name: '异常数据', value: '1,234', icon: 'fas fa-exclamation-triangle', trend: '下降', percentage: '5%' }
];
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
onMounted(() => {
  if (trendChart.value && distributionChart.value) {
    const trend = echarts.init(trendChart.value);
    const distribution = echarts.init(distributionChart.value);
    trend.setOption({
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
        data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
      },
      yAxis: {
        type: 'value'
      },
      series: [{
        data: [820, 932, 901, 934, 1290, 1330, 1320],
        type: 'line',
        smooth: true,
        areaStyle: {
          opacity: 0.1
        },
        lineStyle: {
          width: 3
        },
        itemStyle: {
          color: '#3B82F6'
        }
      }]
    });
    distribution.setOption({
      animation: false,
      tooltip: {
        trigger: 'item'
      },
      legend: {
        orient: 'vertical',
        right: 10,
        top: 'center'
      },
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
        data: [
          { value: 1280, name: '时频标注' },
          { value: 860, name: '无监督标注' }
        ]
      }]
    });
    window.addEventListener('resize', () => {
      trend.resize();
      distribution.resize();
    });
  }
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
