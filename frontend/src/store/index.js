import Vue from 'vue'
import Vuex from 'vuex'
import lodash from 'lodash'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    see_page: null,
    active_modal: null,
    modal: 'login',
    authtoken: null,
    current_user: null,
    groups: [],
    nodes: [],
    admin_update: false
  },
  mutations: {
    see_modal (state, payload) {
      console.log("Commit >> modal = ", payload);
      
      state.modal = payload
    },
    authtoken (state, payload) {
      console.log("Commit >> authtoken", payload);
      
      Vue.axios.defaults.headers.common['Authorization'] = 'Bearer' + ' ' + payload;
      state.authtoken = payload
    },
    current_user (state, payload) {
      console.log("Commit >> current_user", payload);
      
      state.current_user = payload
    },
    see_page (state, payload) {
      console.log("Commit >> see_page = ", payload);
      
      state.see_page = payload
    },
    groups (state, payload) {
      console.log("Commit >> groups = ", payload);
      state.groups = payload
    },
    active_modal (state, payload) {
      console.log("Commit >> active_modal = ", payload);
      state.active_modal = lodash.cloneDeep(payload)
    },
    admin_update (state, payload) {
      state.admin_update = payload
    }
  },
  actions: {
    async login_actualization (context, payload) {
      console.log("Action >> login_actualization", payload);

      context.commit("authtoken", payload)
      if (payload != null) {
        await context.dispatch("fetch_current_user");
      }
    },
    async fetch_groups (context) {
      console.log("Action >> fetch_groups ...");
      
      Vue.axios.get("/groups/browse").then((response) => {
        console.log("Backend >> ", response.data);
        context.commit("groups", response.data)
      }).catch((err) => {
        console.log("Error >> ", err);
        
      })
    },
    async fetch_current_user (context) {
      console.log("Action >> fetch_current_user ...");
      
      Vue.axios.post("/users/current").then((response) => {
        context.commit("current_user", response.data)
      }).catch((err) => {
        console.log("Error >>", err);
        
        context.commit("authtoken", null)
        context.commit("current_user", null)
      });

      // context.dispatch("fetch_nodes")
      // await context.dispatch("fetch_groups")
    },
  },
  modules: {
  }
})
