import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    authtoken: null,
    current_user: null,
    alert: null,
    page: null,
  },
  mutations: {
    authtoken(state, payload) {
      Vue.axios.defaults.headers.common['Authorization'] = 'Bearer' + ' ' + payload;
      state.authtoken = payload
    },
    current_user(state, payload) {
      state.current_user = payload
    },
    page(state, payload) {
      state.page = payload
    },
    warning_alert(state, payload) {
      state.alert = {
        variant: "warning",
        message: payload
      }
    },
    success_alert(state, payload) {
      state.alert = {
        variant: "success",
        message: payload
      }
    },
    no_alert(state) {
      state.alert = null
    },

  },
  actions: {
    async auth_refresh(context) {
      const authtoken = this._vm.$session.get("authtoken", null)
      context.commit("authtoken", authtoken)
      console.log("Auth token?", authtoken)

      if (authtoken) {
        Vue.axios.post("/users/current").then((response) => {
          context.commit("current_user", response.data)
          context.commit("page", {name: "main"})
        }).catch((err) => {
          console.log(err);
          this._vm.$session.set("authtoken", null)
          context.commit("authtoken", null)
          context.commit("current_user", null)
          context.commit("page", null)
        })
      }
      else {
        context.commit("current_user", null)
      }
    },
    async fetch_cu(context) {
      Vue.axios.post("/users/current").then((response) => {
        context.commit("current_user", response.data)
      }).catch((err) => {
        console.log(err);
        this._vm.$session.set("authtoken", null)
        context.commit("authtoken", null)
        context.commit("current_user", null)
      })
    }
  },
  modules: {
  }
})
