<template>
  <el-row style="height: 100%">
    <el-col :span="20" style="height: 100%">
      <el-row style="height: 100%">
        <el-col :span="3" style="height: 100%; display: flex; align-items: center;">
          <el-image fit="fill" src="/static/images/logo.png" style="height: 70%"></el-image>
        </el-col>
        <el-col :span="21" style="display: flex; align-items: center; height: 100%;">
          <h2 style="color: #183080;letter-spacing: 5px; padding: 5px">——基于大模型驱动的桥梁数据清洗平台</h2>
        </el-col>
      </el-row>
    </el-col>
    <el-col :span="4">
      <!-- 用户状态栏 -->
      <div v-if="user" class="fixed top-4 right-4">
        <div class="flex items-center cursor-pointer" @click="isDropdownOpen=!isDropdownOpen" ref="userStatusRef">
          <div class="w-9 h-9 rounded-full overflow-hidden mr-2">
            <img :src="user.avatar ? user.avatar : defaultAvatarUrl" alt="用户头像" class="w-full h-full object-cover" />
          </div>
          <span class="text-gray-700 text-sm mr-1">{{ user.username }}</span>
          <el-icon class="transition-transform duration-300" :class="{ 'rotate-180': isDropdownOpen }">
            <ArrowDown />
          </el-icon>
        </div>

        <div v-if="isDropdownOpen" class="absolute right-0 top-12 w-64 bg-white rounded-lg shadow-lg py-4 z-50">
          <div class="px-4 py-3 border-b border-gray-100">
            <div class="flex items-center mb-1">
              <div class="w-8 h-8 rounded-full overflow-hidden mr-2">
                <img :src="user.avatar ? user.avatar : defaultAvatarUrl" alt="用户头像" class="w-full h-full object-cover" />
              </div>
              <h3 class="font-bold text-gray-800 mb-1">{{ user.username }}</h3>
            </div>
            <div class="flex items-center text-gray-600 text-sm mb-1">
              <el-icon class="mr-2"><Message /></el-icon>
              {{ user.email }}
            </div>
            <div class="flex items-center text-gray-600 text-sm">
              <el-icon class="mr-2"><Phone /></el-icon>
              {{ user.phone }}
            </div>
          </div>

          <div class="px-4 pt-1">
            <button
                class="flex items-center w-full px-3 py-1 text-blue-500 hover:bg-blue-50 rounded-lg transition-colors !rounded-button"
                @click="handleEnterProcess"
            >
              <el-icon class="mr-2"><CirclePlus /></el-icon>
              创建项目
            </button>
          </div>
          <div class="px-4 pt-1">
            <button
                class="flex items-center w-full px-3 py-1 text-red-500 hover:bg-red-50 rounded-lg transition-colors !rounded-button"
                @click="handleLogout"
            >
              <el-icon class="mr-2"><SwitchButton /></el-icon>
              退出登录
            </button>
          </div>
        </div>
      </div>

      <div v-else style="display: flex; justify-content: center; align-items: center; height: 100%;">
        <el-button @click="loginDialogVisible = true; isLogin=true" style="border: 2px solid #183080;color: #183080;">登录</el-button>
        <el-button @click="loginDialogVisible = true; isLogin=false" style="border: 2px solid #183080;color: #183080;">注册</el-button>
      </div>

      <el-dialog
          v-model="logoutDialogVisible"
          title="确认退出"
          width="400px"
          center
      >
        <span class="text-gray-600">确定要退出登录吗？</span>
        <template #footer>
      <span class="dialog-footer">
        <el-button @click="logoutDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmLogout" class="!rounded-button">
          确定
        </el-button>
      </span>
        </template>
      </el-dialog>


    </el-col>
  </el-row>


  <!-- 登录弹窗 -->
  <div v-if="loginDialogVisible" class="fixed inset-0 flex items-center justify-center z-50 bg-gray-500 bg-opacity-50">
    <div class="relative w-[420px] bg-white shadow-xl rounded-xl p-8">
      <!-- 关闭按钮 -->
      <button @click="loginDialogVisible = false" class="absolute top-4 right-4 text-gray-500 hover:text-gray-700">
        <i class="fas fa-times"></i> <!-- 关闭图标 -->
      </button>

      <!-- 登录表单 -->
      <div v-if="isLogin" class="space-y-6">
        <h2 class="text-2xl font-bold text-center text-gray-800 mb-8">登录</h2>

        <div class="relative">
          <input
              type="text"
              v-model="loginForm.username"
              placeholder="请输入用户名"
              class="w-full px-4 py-3 pl-12 text-sm border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
          >
          <i class="fas fa-user absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
        </div>

        <div class="relative">
          <input
              :type="showLoginPassword ? 'text' : 'password'"
              v-model="loginForm.password"
              placeholder="请输入密码"
              class="w-full px-4 py-3 pl-12 text-sm border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
          >
          <i class="fas fa-lock absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
          <button @click="showLoginPassword = !showLoginPassword" class="absolute right-4 top-1/2 -translate-y-1/2">
            <i :class="showLoginPassword ? 'fas fa-eye' : 'fas fa-eye-slash'" class="text-gray-400"></i>
          </button>
        </div>

        <div class="text-right">
          <a href="#" class="text-sm text-blue-600 hover:text-blue-800">忘记密码？</a>
        </div>

        <!-- 登录按钮和加载图标 -->
        <div class="flex items-center justify-between">
          <button
              @click="handleLogin"
              class="w-full py-3 text-white bg-blue-600 hover:bg-blue-700 transition-colors !rounded-button whitespace-nowrap"
          >
            <i v-if="isLoading" class="fas fa-spinner fa-spin mr-2"></i>
            <span >登录</span>
          </button>
        </div>

        <div class="text-center">
          <button @click="toggleForm" class="text-sm text-gray-600 hover:text-blue-600 whitespace-nowrap">
            还没有账号？立即注册
          </button>
        </div>
      </div>

      <!-- 注册表单 -->
      <div v-else class="space-y-4">
        <h2 class="text-2xl font-bold text-center text-gray-800 mb-8">注册</h2>
        <!--   用户头像     -->
        <div class="flex flex-col items-center mb-4">
          <div class="relative w-24 h-24 rounded-full overflow-hidden border-2 border-gray-300 mb-2">
            <img
                ref="myImg"
                :src="registerForm.avatar?registerForm.avatar:defaultAvatarUrl"
                class="w-full h-full object-cover"
                alt="用户头像"
            >

            <div class="absolute inset-0 bg-black bg-opacity-40 opacity-0 hover:opacity-100 flex items-center justify-center">
              <input
                  type="file"
                  accept="image/*"
                  @change="handleAvatarUpload"
                  class="absolute inset-0 opacity-0 cursor-pointer "
              >
              <i class="fas fa-camera text-white text-xl"></i>
            </div>


          </div>
          <span class="text-sm text-gray-500">点击上传头像</span>
        </div>
        <!--   用户名     -->
        <div class="relative">
          <input
              type="text"
              v-model="registerForm.username"
              placeholder="请输入用户名"
              class="w-full px-4 py-3 pl-12 text-sm border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
          >
          <i class="fas fa-user absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
        </div>
        <!--   密码     -->
        <div class="relative">
          <input
              :type="showRegisterPassword ? 'text' : 'password'"
              v-model="registerForm.password"
              placeholder="请输入密码"
              class="w-full px-4 py-3 pl-12 text-sm border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
          >
          <i class="fas fa-lock absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
          <button
              @click="showRegisterPassword = !showRegisterPassword"
              class="absolute right-4 top-1/2 -translate-y-1/2"
          >
            <i :class="showRegisterPassword ? 'fas fa-eye' : 'fas fa-eye-slash'" class="text-gray-400"></i>
          </button>
        </div>
        <!--   确认密码     -->
        <div class="relative">
          <input
              :type="showConfirmPassword ? 'text' : 'password'"
              v-model="registerForm.confirmPassword"
              placeholder="请确认密码"
              class="w-full px-4 py-3 pl-12 text-sm border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
          >
          <i class="fas fa-lock absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
          <button
              @click="showConfirmPassword = !showConfirmPassword"
              class="absolute right-4 top-1/2 -translate-y-1/2"
          >
            <i :class="showConfirmPassword ? 'fas fa-eye' : 'fas fa-eye-slash'" class="text-gray-400"></i>
          </button>
        </div>
        <!--   邮箱     -->
        <div class="relative">
          <input
              type="email"
              v-model="registerForm.email"
              placeholder="请输入邮箱"
              class="w-full px-4 py-3 pl-12 text-sm border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
          >
          <i class="fas fa-envelope absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
        </div>
        <!--   手机号     -->
        <div class="relative">
          <input
              type="tel"
              v-model="registerForm.phone"
              placeholder="请输入手机号"
              class="w-full px-4 py-3 pl-12 text-sm border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
          >
          <i class="fas fa-phone absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
        </div>
        <!-- 注册按钮和加载图标 -->
        <div class="flex items-center justify-between">
          <button
              @click="handleRegister"
              class="w-full py-3 text-white bg-blue-600 hover:bg-blue-700 transition-colors !rounded-button whitespace-nowrap"
              :disabled="isLoading"
          >
            <i v-if="isLoading" class="fas fa-spinner fa-spin mr-2"></i>
            <span >注册</span>
          </button>
        </div>

        <div class="text-center">
          <button @click="toggleForm" class="text-sm text-gray-600 hover:text-blue-600 whitespace-nowrap">
            已有账号？立即登录
          </button>
        </div>
      </div>

      <!-- 错误提示 -->
      <div v-if="errorMessage" class="absolute -top-16 left-1/2 -translate-x-1/2 px-4 py-2 bg-red-100 text-red-700 rounded-lg">
        {{ errorMessage }}
      </div>
    </div>
  </div>


</template>

<script>
import apiService from "@/api/apiService"
import {mapActions, mapState} from "vuex";
import {ArrowDown, CirclePlus, Message, Phone, SwitchButton} from "@element-plus/icons-vue";

export default {

  name: "HeadView",
  components: {CirclePlus, Phone, Message, SwitchButton, ArrowDown},
  data() {
    return {
      logoutDialogVisible: false,
      isLoading: false,
      defaultAvatarUrl: '/static/images/default_avatar.png',
      isDropdownOpen:false,
      errorMessage: "",
      isLogin: true,
      showConfirmPassword: false,
      showRegisterPassword: false,
      showLoginPassword: false,
      loginDialogVisible: false,
      regDialogVisible: false,
      registerForm: {
        username: '',
        password: '',
        confirmPassword: '',
        avatar: null,
        avatarFile: null,
        email: "",
        phone: "",
      },
      loginForm: {
        username: '',
        password: ''
      },
      regForm: {
        username: '',
        password: '',
        avatar: null
      },
      rules: {
        username: [
          {required: true, message: '请输入用户名', trigger: 'blur'}
        ],
        password: [
          {required: true, message: '请输入密码', trigger: 'blur'},
          {min: 6, message: '密码长度不能小于6位', trigger: 'blur'}
        ]
      },
    }
  },
  methods: {
    ...mapActions(['doLogin', 'doLogout']),
    handleAvatarUpload(event){
      const file = event.target.files[0]; // 获取上传的文件
      if (file) {
        // 验证文件类型
        const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
        if (!allowedTypes.includes(file.type)) {
          this.$message.error('只允许上传 JPEG、PNG 或 GIF 格式的图片');
          return;
        }

        // 验证文件大小，限制为 2MB
        if (file.size > 2 * 1024 * 1024) {
          this.$message.error('文件大小不能超过 2MB');
          return;
        }
        let avatarUrl = URL.createObjectURL(file);
        // 将文件保存到 formData 中
        this.registerForm.avatar = avatarUrl;  // 保存文件到注册表单的数据模型中
        this.registerForm.avatarFile = file
        // // 生成头像预览
        // const reader = new FileReader();
        // reader.onloadend = () => {
        //   this.avatarPreview = reader.result;  // 获取文件的 URL
        // };
        // reader.readAsDataURL(file);  // 将文件读取为 Data URL 以便预览
      }
    },
    toggleForm() {
      this.isLogin = !this.isLogin;
      this.errorMessage = '';
    },
    handleLogout() {
      this.logoutDialogVisible = true;
    },
    handleEnterProcess() {
      this.$router.push({ name: 'system_home' });
    },
    async confirmLogout() {
      await this.doLogout();
      this.logoutDialogVisible = false;
      this.$router.push({ name: 'HomeIndex' });
    },
    async handleLogin() {
      if (!this.loginForm.username || !this.loginForm.password) {
          this.$message({type: "error", message: "请填写完整的登录信息"})
      }
      this.isLoading = true;
      let res = await apiService.login(this.loginForm)
      if (res.success) {
        console.log(res.data.data)
        await this.doLogin(res.data.data.access, res.data.data.refresh)
        this.$message({
          type: 'success',
          message: '登录成功'
        });
        this.loginDialogVisible = false;
      } else {
        this.$message({
          type: 'error',
          message: '登录失败'
        });
      }
      this.isLoading = false
    },
    async handleRegister() {
      if (!this.registerForm.username || !this.registerForm.password ||!this.registerForm.confirmPassword) {
        this.$message({type: "error", message:"请输入正确的账号和密码"})
      }
      if (this.registerForm.password !== this.registerForm.confirmPassword) {
        this.$message({type: "error", message:"密码输入不一致，请重新填写"})
      }
      let data = {
        username:this.registerForm.username,
        password:this.registerForm.password,
      }
      if (this.registerForm.email){
        data.email = this.registerForm.email;
      }
      if (this.registerForm.phone){
        data.phone = this.registerForm.phone;
      }
      if (this.registerForm.avatar){
        data.avatar = this.registerForm.avatarFile;
      }else {
        const response = await fetch(this.$refs.myImg.src);
        const blob = await response.blob();

        // 2. 将 Blob 转为 File 对象
        data.avatar = new File([blob], "default_avatar.png", { type: blob.type });
      }
      this.isLoading = true;
      let response = await apiService.registerUser(data)
      if (response.success) {
        this.$message({
          type: 'success',
          message: '注册成功'
        });
        this.loginDialogVisible = false;
      }else {
        this.$message({
          type: 'error',
          message: '注册失败'
        });
      }
      this.isLoading = false;
    },
    handleAvatarSuccess(file) {
      this.regForm.avatar = file.raw;
      this.avatarPreview = URL.createObjectURL(file.raw);
    }
  },
  computed: {
    ...mapState(['user'])
  }
}
</script>

<style scoped>

/* 移除number类型input的箭头 */
input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
</style>
