<template>
<!--  <div class="z-1">-->
<!--    <el-image style="height: 100%" src="/static/images/home-banner.png" fit="contain"></el-image>-->
<!--  </div>-->
<!--  <div style="height: 50%;" >-->
<!--    <el-menu-->
<!--        class="custom-menu"-->
<!--        mode="horizontal"-->
<!--        style="width: 100%; font-size: 30px;  display: flex; justify-content: center; align-items: center;"-->
<!--        :ellipsis="false"-->
<!--        text-color="#888888"-->
<!--        active-text-color="#409eff"-->
<!--        background-color="white"-->
<!--        popper-class="custom-tooltip"-->
<!--        router-->
<!--    >-->
<!--      <el-row  style="width: 90%; font-weight: bolder; color: #888888" >-->
<!--        <el-col :span="6" style="display: flex; justify-content: center;">-->
<!--          <el-menu-item index="/feature-intro">功能介绍</el-menu-item>-->
<!--        </el-col>-->
<!--        <el-col :span="6" style="display: flex; justify-content: center;">-->
<!--          <el-menu-item index="/data-service">数据服务</el-menu-item>-->
<!--        </el-col>-->
<!--        <el-col :span="6" style="display: flex; justify-content: center;">-->
<!--          <el-menu-item index="/unique-advantages">特色优势</el-menu-item>-->
<!--        </el-col>-->
<!--        <el-col :span="6" style="display: flex; justify-content: center;">-->
<!--          <el-menu-item index="/study-exchange">学习交流</el-menu-item>-->
<!--        </el-col>-->
<!--      </el-row>-->

<!--    </el-menu>-->
<!--    <router-view ></router-view>-->
<!--  </div>-->
  <div class="min-h-screen bg-white">
    <!-- Hero Section https://ai-public.mastergo.com/ai/img_res/bdaa185cbbe4112b2b6381931f1e0749.jpg-->
    <section class="relative h-[600px] overflow-hidden">
      <div class="absolute inset-0">
        <el-image src="/static/images/home-banner.png"
             class="w-full h-full object-cover" alt="hero background"/>
      </div>
      <div class="container mx-auto px-4 h-full relative z-10">
        <div class="flex items-center h-full">
          <div class="w-1/2">
<!--            <h1 class="text-6xl font-bold text-white mb-6">桥智学</h1>-->
<!--            <p class="text-xl text-gray-200 mb-8">基于大模型驱动的桥梁数据清洗平台</p>-->
<!--            <button class="bg-blue-600 text-white px-8 py-3 !rounded-button whitespace-nowrap hover:bg-blue-700 transition-colors">-->
<!--              立即体验-->
<!--            </button>-->
          </div>
        </div>
      </div>
    </section>
    <!-- Features Section -->
    <section class="py-20 bg-gray-50">
      <div class="container mx-auto px-4">
        <h2 class="text-4xl font-bold text-center mb-16">核心功能</h2>
        <div class="grid grid-cols-3 gap-8">
          <div class="feature-card bg-white p-8 rounded-lg shadow-lg hover:shadow-xl transition-shadow">
            <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mb-6">
              <i class="fas fa-chart-line text-2xl text-blue-600"></i>
            </div>
            <h3 class="text-xl font-bold mb-4">可视化数据管理</h3>
            <p class="text-gray-600">提供直观的数据可视化界面，轻松管理和分析桥梁数据</p>
          </div>
          <div class="feature-card bg-white p-8 rounded-lg shadow-lg hover:shadow-xl transition-shadow">
            <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mb-6">
              <i class="fas fa-database text-2xl text-blue-600"></i>
            </div>
            <h3 class="text-xl font-bold mb-4">数据采集与清洗</h3>
            <p class="text-gray-600">专业的数据采集、标注和清洗服务，确保数据质量</p>
          </div>
          <div class="feature-card bg-white p-8 rounded-lg shadow-lg hover:shadow-xl transition-shadow">
            <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mb-6">
              <i class="fas fa-cube text-2xl text-blue-600"></i>
            </div>
            <h3 class="text-xl font-bold mb-4">三维模型展示</h3>
            <p class="text-gray-600">实时展示三维模型场景，直观呈现桥梁结构</p>
          </div>
        </div>
      </div>
    </section>
    <!-- Services Section -->
    <section class="py-20">
      <div class="container mx-auto px-4">
        <h2 class="text-4xl font-bold text-center mb-16">数据服务</h2>
        <div class="grid grid-cols-2 gap-12">
          <div class="service-visualization">
            <div ref="chartRef" class="w-full h-[400px]"></div>
          </div>
          <div class="grid grid-cols-2 gap-6">
            <div class="service-card p-6 bg-gray-50 rounded-lg">
              <i class="fas fa-tasks text-2xl text-blue-600 mb-4"></i>
              <h3 class="text-xl font-bold mb-2">数据管理</h3>
              <p class="text-gray-600">全面的数据管理方案</p>
            </div>
            <div class="service-card p-6 bg-gray-50 rounded-lg">
              <i class="fas fa-cloud text-2xl text-blue-600 mb-4"></i>
              <h3 class="text-xl font-bold mb-2">数据服务</h3>
              <p class="text-gray-600">专业的数据服务支持</p>
            </div>
            <div class="service-card p-6 bg-gray-50 rounded-lg">
              <i class="fas fa-cogs text-2xl text-blue-600 mb-4"></i>
              <h3 class="text-xl font-bold mb-2">数据处理</h3>
              <p class="text-gray-600">高效的数据处理能力</p>
            </div>
            <div class="service-card p-6 bg-gray-50 rounded-lg">
              <i class="fas fa-clock text-2xl text-blue-600 mb-4"></i>
              <h3 class="text-xl font-bold mb-2">实时数据</h3>
              <p class="text-gray-600">实时数据监控分析</p>
            </div>
          </div>
        </div>
      </div>
    </section>
    <!-- Advantages Section -->
    <section class="py-20 bg-gray-50">
      <div class="container mx-auto px-4">
        <h2 class="text-4xl font-bold text-center mb-16">我们的优势</h2>
        <div class="grid grid-cols-4 gap-8">
          <div class="advantage-card text-center">
            <div class="w-20 h-20 mx-auto mb-6">
              <img src="https://ai-public.mastergo.com/ai/img_res/592376731982108558523196264f7591.jpg"
                   class="w-full h-full object-cover rounded-lg" alt="data service"/>
            </div>
            <h3 class="text-xl font-bold mb-4">全面丰富的数据服务</h3>
            <p class="text-gray-600">提供完整的数据生命周期服务</p>
          </div>
          <div class="advantage-card text-center">
            <div class="w-20 h-20 mx-auto mb-6">
              <img src="https://ai-public.mastergo.com/ai/img_res/b73dc9a9939c6cf11ad81520cc40fa60.jpg"
                   class="w-full h-full object-cover rounded-lg" alt="data quality"/>
            </div>
            <h3 class="text-xl font-bold mb-4">高质量数据加工</h3>
            <p class="text-gray-600">专业团队确保数据质量</p>
          </div>
          <div class="advantage-card text-center">
            <div class="w-20 h-20 mx-auto mb-6">
              <img src="https://ai-public.mastergo.com/ai/img_res/08feef1bda0ce6d225b7d18595c739df.jpg"
                   class="w-full h-full object-cover rounded-lg" alt="security"/>
            </div>
            <h3 class="text-xl font-bold mb-4">完善的安全服务</h3>
            <p class="text-gray-600">全方位数据安全保障</p>
          </div>
          <div class="advantage-card text-center">
            <div class="w-20 h-20 mx-auto mb-6">
              <img src="https://ai-public.mastergo.com/ai/img_res/28b6bf231d8ae20a7df742c3f360e047.jpg"
                   class="w-full h-full object-cover rounded-lg" alt="ai integration"/>
            </div>
            <h3 class="text-xl font-bold mb-4">AI 开发接轨</h3>
            <p class="text-gray-600">深度整合人工智能技术</p>
          </div>
        </div>
      </div>
    </section>
    <!-- Contact Section -->
    <section class="py-20 bg-gradient-to-b from-white to-gray-50">
      <div class="container mx-auto px-4">
        <h2 class="text-4xl font-bold text-center mb-4">联系我们</h2>
        <p class="text-gray-600 text-center mb-16">我们期待与您沟通交流，为您提供专业的服务支持</p>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 max-w-6xl mx-auto">
          <div class="bg-white rounded-xl shadow-xl overflow-hidden">
            <div class="p-8">
              <div class="space-y-6">
                <div>
                  <label class="block text-gray-700 text-sm font-bold mb-2">您的姓名</label>
                  <div class="relative">
                    <i class="fas fa-user absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"></i>
                    <input type="text" class="w-full pl-10 pr-4 py-3 bg-gray-50 border-none rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all" placeholder="请输入您的姓名"/>
                  </div>
                </div>
                <div>
                  <label class="block text-gray-700 text-sm font-bold mb-2">电子邮箱</label>
                  <div class="relative">
                    <i class="fas fa-envelope absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"></i>
                    <input type="email" class="w-full pl-10 pr-4 py-3 bg-gray-50 border-none rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all" placeholder="请输入您的邮箱"/>
                  </div>
                </div>
                <div>
                  <label class="block text-gray-700 text-sm font-bold mb-2">联系电话</label>
                  <div class="relative">
                    <i class="fas fa-phone absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"></i>
                    <input type="tel" class="w-full pl-10 pr-4 py-3 bg-gray-50 border-none rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all" placeholder="请输入您的联系电话"/>
                  </div>
                </div>
                <div>
                  <label class="block text-gray-700 text-sm font-bold mb-2">留言内容</label>
                  <div class="relative">
                    <i class="fas fa-comment absolute left-3 top-3 text-gray-400"></i>
                    <textarea class="w-full pl-10 pr-4 py-3 bg-gray-50 border-none rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all h-32" placeholder="请输入您的留言内容"></textarea>
                  </div>
                </div>
                <button class="w-full bg-blue-600 text-white py-3 !rounded-button whitespace-nowrap hover:bg-blue-700 transition-colors flex items-center justify-center space-x-2">
                  <i class="fas fa-paper-plane"></i>
                  <span>提交留言</span>
                </button>
              </div>
            </div>
          </div>
          <div class="bg-white rounded-xl shadow-xl overflow-hidden">
            <div class="p-8 h-full flex flex-col">
              <h3 class="text-2xl font-bold mb-6">更多联系方式</h3>
              <div class="space-y-8 flex-grow">
                <div class="flex items-center space-x-4">
                  <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                    <i class="fas fa-map-marker-alt text-xl text-blue-600"></i>
                  </div>
                  <div>
                    <h4 class="font-bold text-gray-700">公司地址</h4>
                    <p class="text-gray-600">北京市海淀区中关村科技园区</p>
                  </div>
                </div>
                <div class="flex items-center space-x-4">
                  <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                    <i class="fas fa-phone-alt text-xl text-blue-600"></i>
                  </div>
                  <div>
                    <h4 class="font-bold text-gray-700">联系电话</h4>
                    <p class="text-gray-600">400-888-9999</p>
                  </div>
                </div>
                <div class="flex items-center space-x-4">
                  <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                    <i class="fas fa-envelope text-xl text-blue-600"></i>
                  </div>
                  <div>
                    <h4 class="font-bold text-gray-700">电子邮箱</h4>
                    <p class="text-gray-600">contact@bridgeai.com</p>
                  </div>
                </div>
                <div class="flex items-center space-x-4">
                  <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                    <i class="fas fa-clock text-xl text-blue-600"></i>
                  </div>
                  <div>
                    <h4 class="font-bold text-gray-700">工作时间</h4>
                    <p class="text-gray-600">周一至周五 9:00-18:00</p>
                  </div>
                </div>
              </div>
              <div class="mt-8 flex space-x-4">
                <button class="flex-1 bg-gray-100 text-gray-700 py-3 !rounded-button whitespace-nowrap hover:bg-gray-200 transition-colors flex items-center justify-center">
                  <i class="fab fa-weixin mr-2"></i>
                  微信咨询
                </button>
                <button class="flex-1 bg-gray-100 text-gray-700 py-3 !rounded-button whitespace-nowrap hover:bg-gray-200 transition-colors flex items-center justify-center">
                  <i class="fab fa-qq mr-2"></i>
                  QQ 咨询
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  name: 'HomeView',
  data() {
    return {
      chartInstance: null
    }
  },
  mounted() {
    this.initChart();
    window.addEventListener('resize', this.handleResize);
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.handleResize);
    if (this.chartInstance) {
      this.chartInstance.dispose();
    }
  },
  methods: {
    initChart() {
      const chartDom = this.$refs.chartRef;
      if (!chartDom) return;

      this.chartInstance = echarts.init(chartDom);
      const option = {
        animation: false,
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['数据处理量', '服务请求量']
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: ['1月', '2月', '3月', '4月', '5月', '6月']
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: '数据处理量',
            type: 'line',
            data: [150, 232, 201, 154, 190, 330],
            smooth: true,
            lineStyle: {
              color: '#4299e1'
            },
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                {
                  offset: 0,
                  color: 'rgba(66, 153, 225, 0.3)'
                },
                {
                  offset: 1,
                  color: 'rgba(66, 153, 225, 0.1)'
                }
              ])
            }
          },
          {
            name: '服务请求量',
            type: 'line',
            data: [120, 182, 191, 234, 290, 330],
            smooth: true,
            lineStyle: {
              color: '#48bb78'
            },
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                {
                  offset: 0,
                  color: 'rgba(72, 187, 120, 0.3)'
                },
                {
                  offset: 1,
                  color: 'rgba(72, 187, 120, 0.1)'
                }
              ])
            }
          }
        ]
      };
      this.chartInstance.setOption(option);
    },
    handleResize() {
      if (this.chartInstance) {
        this.chartInstance.resize();
      }
    }
  }
}
</script>

<style scoped>
/* 样式部分保持不变 */
.hero-background::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to right, rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.3));
}
.feature-card {
  transition: transform 0.3s ease;
}
.feature-card:hover {
  transform: translateY(-5px);
}
.service-card {
  transition: all 0.3s ease;
}
.service-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}
.advantage-card {
  transition: transform 0.3s ease;
}
.advantage-card:hover {
  transform: translateY(-5px);
}
</style>