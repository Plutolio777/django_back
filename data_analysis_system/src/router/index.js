import { createRouter, createWebHistory } from 'vue-router'
import HomeView from "@views/content/HomeView.vue";
import UniqueAdvantages from "@views/content/UniqueAdvantages.vue";
import StudyExchange from "@views/content/StudyExchange.vue";
import DataService from "@views/content/DataService.vue";
import FeatureIntro from "@views/content/FeatureIntro.vue";
import SystemMainView from "@views/system/SystemMainView.vue";
import DataSetView from "@views/system/content/DataSetView.vue";
import DataSourceView from "@views/system/content/DataSourceView.vue";
import TagManageView from "@views/system/content/TagManageView.vue";
import FrequencyLabel from "@views/system/content/FrequencyLabel.vue";
import UnsupervisedLabel from "@views/system/content/UnsupervisedLabel.vue";
import DataAnnotation from "@views/system/content/DataAnnotation.vue";
import DataClean from "@views/system/content/DataClean.vue";
import DataDashboard from "@views/system/content/DataDashboard.vue";
import Dashboard from "@views/system/content/Dashboard.vue";







const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: "Home",
      component: HomeView,
      children: [
        {
          path: 'feature-intro',
          component: FeatureIntro,
          name: "HomeIndex",
        },
        {
          path: 'data-service',
          component: DataService
        },
        {
          path: 'unique-advantages',
          component: UniqueAdvantages
        },
        {
          path: 'study-exchange',
          component: StudyExchange
        },
      ]
    },
    {
      path: '/system',
      name: "system_home",
      component: SystemMainView,
      meta: { requiresAuth: true },
      children: [
        {
          path: 'data-set',
          name: "DataSetView",
          component: DataSetView
        },
        {
          path: 'data-source',
          component: DataSourceView
        },

        {
          path: 'tag-manage',
          component: TagManageView
        },
        {
          path: 'frequency-label',
          component: FrequencyLabel
        },
        {
          path: 'unsupervised-label',
          component: UnsupervisedLabel
        },
        {
          path: 'data-annotation',
          component: DataAnnotation
        },

        {
          path: 'data-clean',
          component: DataClean
        },
        {
          path: 'data-dashboard',
          component: DataDashboard
        },

        {
          path: 'dashboard',
          component: Dashboard
        },
      ]
    }
  ]
})


router.beforeEach((to, from, next) => {
  // 如果目标路由需要登录
  console.log(to, from, next)
  if (to.name === "Home") {
    next({ name: 'HomeIndex' });
    return
  }
  if (to.name === "system_home") {
    next({ name: 'DataSetView' });
    return
  }
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // 判断用户是否已登录（这里使用 localStorage 判断登录状态）
    const isLoggedIn = localStorage.getItem('user');  // 假设登录成功后 token 存储在 localStorage 中

    if (!isLoggedIn) {
      // 如果未登录，跳转到登录页面
      next({ name: 'HomeIndex' });
    } else {
      // 如果已登录，继续访问目标页面
      next();
    }
  } else {
    // 不需要登录的页面直接访问
    next();
  }
});

export default router
