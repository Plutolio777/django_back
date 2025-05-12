<template>
  <div ref="container" class="w-full h-full"></div>
</template>

<script>
import { defineComponent, markRaw } from 'vue';
import * as THREE from 'three';
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader.js';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

export default defineComponent({
  props: {
    modelPath: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      scene: null,
      camera: null,
      renderer: null,
      controls: null,
      model: null
    };
  },
  mounted() {
    this.initThreeJS();
    this.loadModel();
    this.animate();
  },
  beforeUnmount() {
    cancelAnimationFrame(this.animationId);
    window.removeEventListener('resize', this.handleResize);
  },
  methods: {
    initThreeJS() {
      const width = this.$refs.container.clientWidth;
      const height = this.$refs.container.clientHeight;
      
      // 创建场景(使用markRaw防止响应式转换)
      this.scene = markRaw(new THREE.Scene());
      this.scene.background = new THREE.Color(0x808080); // 灰色背景

      // 创建相机(使用markRaw防止响应式转换)
      this.camera = markRaw(new THREE.PerspectiveCamera(
        75,
        width / height,
        0.1,
        100000  // 极大增加远裁剪面
      ));
      this.camera.position.set(0, 1000, 1000); // 更高更远的初始位置
      this.camera.lookAt(0, 0, 0);

      // 创建渲染器(使用markRaw防止响应式转换)
      this.renderer = markRaw(new THREE.WebGLRenderer({ antialias: true }));
      this.renderer.setSize(width, height);
      this.$refs.container.appendChild(this.renderer.domElement);

      // 添加轨道控制器(使用markRaw防止响应式转换)
      this.controls = markRaw(new OrbitControls(this.camera, this.renderer.domElement));
      this.controls.enableDamping = true;

      // 添加多种光源
      const ambientLight = new THREE.AmbientLight(0x404040, 1); // 环境光
      this.scene.add(ambientLight);

      const directionalLight = new THREE.DirectionalLight(0xffffff, 1); // 方向光
      directionalLight.position.set(5, 5, 5);
      this.scene.add(directionalLight);

      const pointLight = new THREE.PointLight(0xff0000, 1, 100); // 点光源
      pointLight.position.set(0, 50, 0);
      this.scene.add(pointLight);

      const spotLight = new THREE.SpotLight(0x00ff00, 1, 100, Math.PI/4, 0.5, 2); // 聚光灯
      spotLight.position.set(10, 50, 10);
      spotLight.target.position.set(0, 0, 0);
      this.scene.add(spotLight);
      this.scene.add(spotLight.target);

      // 添加网格辅助
      const gridHelper = new THREE.GridHelper(1000, 20);
      this.scene.add(gridHelper);

      // 添加坐标轴辅助
      const axesHelper = new THREE.AxesHelper(500);
      this.scene.add(axesHelper);

      // 窗口大小变化处理
      window.addEventListener('resize', this.handleResize);
    },
    loadModel() {
      console.log('正在加载模型:', this.modelPath);
      const loader = new OBJLoader();
      loader.load(
        this.modelPath,
        (object) => {
          console.log('模型加载完成:', object);
          this.model = markRaw(object);
          
          // 强制添加高亮材质确保可见
          object.traverse(child => {
            if (child.isMesh) {
              child.material = new THREE.MeshStandardMaterial({
                color: 0x00aaff, // 亮蓝色
                roughness: 0.1,
                metalness: 0.9,
                wireframe: false
              });
              child.castShadow = true;
              child.receiveShadow = true;
              console.log('已为模型添加材质:', child);
            }
          });

          // 缩放模型
          object.scale.set(3, 3, 3);
          this.scene.add(object);

          // 居中模型并调整相机
          const box = new THREE.Box3().setFromObject(object);
          const size = box.getSize(new THREE.Vector3()).length();
          const center = box.getCenter(new THREE.Vector3());
          
          object.position.sub(center);
          this.camera.position.copy(center);
          this.camera.position.y = size * 2; // 更高视角
          this.camera.position.z = size * 3; // 更远距离
          this.camera.lookAt(center);
          
          // 更新控制器目标
          this.controls.target.copy(center);
          this.controls.update();

          // 添加边界框辅助查看
          const bboxHelper = new THREE.Box3Helper(box, 0xffff00);
          this.scene.add(bboxHelper);
        },
        (xhr) => {
          console.log((xhr.loaded / xhr.total) * 100 + '% loaded');
        },
        (error) => {
          console.error('模型加载失败:', error);
          // 添加错误提示元素
          const errorDiv = document.createElement('div');
          errorDiv.className = 'absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white';
          errorDiv.innerHTML = `
            <div class="text-center p-4 bg-gray-800 rounded-lg">
              <i class="fas fa-exclamation-triangle text-2xl mb-2"></i>
              <p>模型加载失败</p>
              <p class="text-sm text-gray-300">${this.modelPath}</p>
            </div>
          `;
          this.$refs.container.appendChild(errorDiv);
        }
      );
    },
    animate() {
      if (!this.$refs.container) return; // 检查容器是否存在
      
      try {
        this.animationId = requestAnimationFrame(this.animate.bind(this));
        this.controls.update();
        
        // 检查模型是否仍在场景中
        if (this.model && !this.scene.children.includes(this.model)) {
          console.warn('模型已从场景中移除，重新添加');
          this.scene.add(this.model);
        }
        
        this.renderer.render(this.scene, this.camera);
      } catch (error) {
        console.error('渲染错误:', error);
      }
    },
    handleResize() {
      this.camera.aspect = this.$refs.container.clientWidth / this.$refs.container.clientHeight;
      this.camera.updateProjectionMatrix();
      this.renderer.setSize(
        this.$refs.container.clientWidth,
        this.$refs.container.clientHeight
      );
    }
  }
});
</script>

<style scoped>
.w-full {
  width: 100%;
}
.h-full {
  height: 100%;
}
</style>
