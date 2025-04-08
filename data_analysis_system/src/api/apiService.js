import axios from 'axios';
import store from '@/store'; // 引入 Vuex store

// 创建 axios 实例
const instance = axios.create({
    timeout: 10000, // 设置请求超时时间
});

// 获取当前登录的用户信息
function getAccess() {
    return store.state.access || localStorage.getItem("access"); // 从 Vuex 获取用户信息
}

// 设置 JWT Token
function setAuthHeader() {
    const userInfo = getUserInfo();
    if (userInfo && userInfo.token) {
        instance.defaults.headers['Authorization'] = `Bearer ${userInfo.token}`;
    }
}

// 添加请求拦截器，判断用户是否登录
instance.interceptors.request.use(
    (config) => {
        if (config.requiresAuth) {
            const access = getAccess();
            if (access) {
                config.headers['Authorization'] = `Bearer ${access}`;
            } else {
                // todo 可以尝试刷新token
                console.error('用户未登录，请先登录');
                return Promise.reject(new Error('用户未登录'));
            }
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// 处理文件上传和其他数据
function handleFileUpload(data, isFileUpload, fileKey) {
    if (!isFileUpload) return data; // 如果不需要上传文件，直接返回原数据

    const formData = new FormData();

    // 如果 isFileUpload 为 true，处理文件上传
    if (Array.isArray(data[fileKey])) {
        // 如果文件是数组，逐个添加文件，添加索引
        data[fileKey].forEach((file, index) => {
            formData.append(`${fileKey}[${index}]`, file); // 给每个文件添加索引
        });
    } else {
        // 如果是单个文件，直接添加
        formData.append(fileKey, data[fileKey]);
    }

    // 添加其他非文件字段
    Object.keys(data).forEach((key) => {
        if (key !== fileKey) {
            formData.append(key, data[key]);
        }
    });

    return formData; // 返回处理后的 FormData
}

// 统一的请求方法，处理所有不同的请求
// 统一的请求方法，处理所有不同的请求
async function request({ method, url, data, params, pathParams, headers, isFileUpload, fileKey, requiresAuth }) {
    // 替换路径参数
    if (pathParams) {
        Object.keys(pathParams).forEach((key) => {
            url = url.replace(`:${key}`, pathParams[key]);
        });
    }

    // 如果需要文件上传，根据 isFileUpload 和 FileKey 处理数据
    if (isFileUpload) {
        data = handleFileUpload(data, isFileUpload, fileKey);
        headers = { ...headers, 'Content-Type': 'multipart/form-data' };
    } else {
        // 如果没有文件，使用 JSON 格式
        headers = { ...headers, 'Content-Type': 'application/json' };
        data = JSON.stringify(data);
    }

    // 设置请求配置
    const config = {
        method,
        url,
        headers: { ...headers },
        params,  // GET 请求参数
        data,    // POST 请求体数据
        requiresAuth,
    };

    // return await instance(config);
    try {
        // 发起请求
        const response = await instance(config);
        // console.log(123, response);
        // 可以根据需求对返回的数据进行处理（例如统一格式化）
        if (200 <= response.status < 300) {
            // 假设所有响应都包含一个 `data` 字段
            return {
                success: true,
                data: response.data,
            };
        } else {
            // 如果返回的状态码不是 200，返回错误信息
            return {
                success: false,
                error: `请求失败，状态码: ${response.status}`,
            };
        }
    } catch (error) {
        // 捕获请求错误
        console.error(`Request failed for ${url}:`, error);
        return {
            success: false,
            error: error.response ? error.response.data : error.message,
        };
    }
}


// 定义 API 配置对象
const apiConfig = {
    // 示例：GET 请求
    me: {
        method: 'GET',
        url: '/api/user/users/me',
        isFileUpload: false,
    },
    registerUser: {
        method: 'POST',
        url: '/api/user/register/',
        isFileUpload: true,
        fileKey: "avatar",
        requiresAuth: false
    },
    login: {
        method: 'POST',
        url: '/api/user/token/',
        isFileUpload: false,
        requiresAuth: false
    },
    refreshToken: {
        method: 'POST',
        url: '/api/user/token/refresh/',
        isFileUpload: false,
    },
    fetchDataSet: {
        method: 'GET',
        url: '/api/data_manage/datasets/',
        isFileUpload: false,
    },
    uploadDataSet: {
        method: 'POST',
        url: '/api/data_manage/datasets/',
        isFileUpload: true,
        fileKey: "data_set_path",
    },
    editDataSet: {
        method: 'PUT',
        url: '/api/data_manage/datasets/:id/',
        isFileUpload: false,
    },
    deleteDataSet: {
        method: 'DELETE',
        url: '/api/data_manage/datasets/:id/',
        isFileUpload: false,
    },
    dataSetDetail:{
        method: 'GET',
        url: '/api/data_manage/data_detail/',
        isFileUpload: false,
    },
    fetchDataLabelList:{
        method: 'GET',
        url: '/api/data_mark/time/',
        isFileUpload: false,
    },
    executeTimeMarkTask:{
        method: 'POST',
        url: '/api/data_mark/time/execute/',
        isFileUpload: false,
    },
    fetchTimeMarkTaskProgress:{
        method: 'GET',
        url: '/api/data_mark/time/progress/',
        isFileUpload: false,
    },
    fetchTimeMarkTaskProgressDetail:{
        method: 'GET',
        url: '/api/data_mark/time/progress_detail/',
        isFileUpload: false,
    },
    fetchUnsupervisedDataLabelList:{
        method: 'GET',
        url: '/api/data_mark/unsupervised/',
        isFileUpload: false,
    },
    executeUnsupervisedMarkTask:{
        method: 'POST',
        url: '/api/data_mark/unsupervised/execute/',
        isFileUpload: false,
    },
    fetchUnsupervisedMarkTaskProgress:{
        method: 'GET',
        url: '/api/data_mark/unsupervised/progress/',
        isFileUpload: false,
    },
    fetchUnsupervisedMarkTaskProgressDetail:{
        method: 'GET',
        url: '/api/data_mark/unsupervised/progress_detail/',
        isFileUpload: false,
    },
    fetchCleanedData:{
        method: 'GET',
        url: '/api/data_mark/cleaned/',
        isFileUpload: false,
    },
    fetchCleanedDetailData:{
        method: 'GET',
        url: '/api/data_mark/cleaned/data_detail/',
        isFileUpload: false,
    },
};

// 生成 API 请求函数
function createApiMethods(config) {
    const apiMethods = {};

    Object.keys(config).forEach((apiName) => {
        const defaultConfig = {
            method: "GET",
            url: "",
            isFileUpload: false,
            fileKey: "",
            requiresAuth: true,
        }
        const finalConfig = Object.assign({}, defaultConfig, config[apiName]);
        const { method, url, isFileUpload, fileKey, requiresAuth} = finalConfig;
        apiMethods[apiName] = async (data = {}, params = {}, pathParams = {}, headers = {}) => {
            // console.log(`api request ${apiName} from url ${url}`);
            return await request({
                method,
                url,
                data,
                params,
                pathParams,
                headers,
                isFileUpload,
                fileKey,
                requiresAuth,
            });
        };
    });

    return apiMethods;
}

// 通过配置自动生成所有 API 方法
const  apiService = createApiMethods(apiConfig);

export default apiService;
