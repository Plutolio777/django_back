<template>
  <div ref="canvasContainer" class="three-canvas-container"></div>
</template>

<script>
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'; // 引入 OrbitControls

export default {
  name: 'ThreeDModelViewer',
  mounted() {
    this.init3DScene();
  },
  methods: {
    init3DScene() {
      const width = this.$refs.canvasContainer.clientWidth;
      const height = this.$refs.canvasContainer.clientHeight;
      const scene = new THREE.Scene();

      // 创建相机
      const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 10000); // 设置远裁剪面为 5000
      camera.position.set(0, 5, 10); // 设置相机位置 (x, y, z)
      camera.lookAt(0, 0, 0); // 相机始终看向模型

      const renderer = new THREE.WebGLRenderer();
      renderer.setClearColor(0x808080, 1); // 设置背景颜色为灰色
      renderer.setSize(width, height);
      this.$refs.canvasContainer.appendChild(renderer.domElement);

      // 添加环境光，提供基础的均匀照明
      const ambientLight = new THREE.AmbientLight(0x404040, 1); // 灰色环境光，强度为1
      scene.add(ambientLight);

      // 添加方向光，模拟太阳光
      const directionalLight = new THREE.DirectionalLight(0xffffff, 1); // 白色方向光
      directionalLight.position.set(5, 5, 5); // 设置方向光的位置
      scene.add(directionalLight);

      // 添加点光源，模拟局部光源，例如灯泡
      const pointLight = new THREE.PointLight(0xff0000, 1, 100); // 红色点光源，强度为1，最大范围100
      pointLight.position.set(0, 50, 0); // 设置点光源的位置
      scene.add(pointLight);

      // 添加聚光灯，模拟聚焦的光源
      const spotLight = new THREE.SpotLight(0x00ff00, 1, 100, Math.PI / 4, 0.5, 2); // 绿色聚光灯
      spotLight.position.set(10, 50, 10); // 设置聚光灯的位置
      spotLight.target.position.set(0, 0, 0); // 设置聚光灯照射的目标位置
      scene.add(spotLight);
      scene.add(spotLight.target); // 必须将目标添加到场景中
      const gridHelper = new THREE.GridHelper(12000, 20); // 参数分别是网格的大小和每个网格的分段数
      scene.add(gridHelper);
      // 加载GLTF模型
      const loader = new GLTFLoader();
      loader.load(
          '/models/model.glb',  // 从 public/models/ 目录加载模型
          (gltf) => {
            scene.add(gltf.scene);
            gltf.scene.scale.set(3, 3, 3); // 设置模型的大小
            gltf.scene.position.set(0, 0, 0); // 设置模型的位置
          },
          undefined,
          (error) => {
            console.error(error);
          }
      );
      camera.position.y = 1000;
      camera.position.z = 1000;

      // 让相机看向模型
      camera.lookAt(0, 0, 0);
      // 添加 OrbitControls 控制器
      const controls = new OrbitControls(camera, renderer.domElement);

      // 渲染循环
      const animate = () => {
        requestAnimationFrame(animate);
        controls.update(); // 更新控制器
        renderer.render(scene, camera);
      };
      animate();
    }
  },
};
</script>

<style scoped>
.three-canvas-container {
  position: fixed; /* 使用 fixed 定位 */
  bottom: 0; /* 底部对齐 */
  left: 0;
  right: 0;  /* 设置右边界 */
  margin-left: auto; /* 左右边距自动，居中 */
  margin-right: auto; /* 让右边距自动 */
  width: 80%; /* 宽度设为80%，可以调整 */
  height: 80%; /* 高度为80% */
  background-color: #f0f0f0;
  z-index: 1; /* 确保渲染器在其他内容之上 */
}
</style>