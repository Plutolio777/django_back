import {createStore} from 'vuex';
import apiService from "@/api/apiService.js";

async function getUserInformation(){
    let response = await apiService.me()
    console.log(response)
    console.log(response)
    if (response.success) {
        return response.data.data;
    }
    return null
}

function getLocalUser(){
    let localUser = localStorage.getItem('user') || null
    try {
        if (localUser) {
            return JSON.parse(localUser);
        }
    }catch(err){
        localStorage.clear();
    }
    return null
}

export default createStore({
    state: {
        // 存储你的状态数据
        user: getLocalUser(),
        access: localStorage.getItem('access') || '',
        refresh: localStorage.getItem('refresh') || '',
    },
    mutations: {
        // 更改状态
        setUser(state, user) {
            state.user = user;
        },
        setAccess(state, access) {
            state.access = access;
        },
        setRefresh(state, refresh) {
            state.refresh = refresh;
        },
        clearUser(state) {
            localStorage.clear();
            state.user = null;
            state.access = "";
            state.refresh = "";
        }
    },
    actions: {
        // 异步操作
        async doLogin({ commit }, token, refresh) {
            commit("setAccess", token);
            localStorage.setItem("access", token);
            commit("setRefresh", refresh);
            localStorage.setItem("refresh", refresh);
            let response = await apiService.me()
            console.log(response)
            if (response.success) {
                let user=  response.data.data
                commit("setUser", user);
                localStorage.setItem("user", JSON.stringify(user));
            }
        },
        async doLogout({ commit }) {
            commit("clearUser");
        }

    },
    getters: {
        // 访问状态的 getter
        user: (state) => state.user,
        access: (state) => state.access,
        refresh: (state) => state.refresh,
    },
});
