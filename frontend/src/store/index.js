import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    see_page: null,
    modal: 'login',
    authtoken: null,
    current_user: null,
    groups: [],
    nodes: []
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
    // nodes (state, payload) {
    //   console.log("Commit >> nodes = ", payload);
      
    //   state.nodes = payload
    // }
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
      
      Vue.axios.get("/users/current").then((response) => {
        context.commit("current_user", response.data)
      }).catch((err) => {
        console.log("Error >>", err);
        
        context.commit("authtoken", null)
        context.commit("current_user", null)
      });

      // context.dispatch("fetch_nodes")
      await context.dispatch("fetch_groups")
    },
    // fetch_nodes (context) {
    //   console.log("Action >> fetch_nodes ...");
    //   Vue.axios.get("/nodes/current").then((response) => {
    //     console.log("Backend >> ", response.data);
    //     context.commit("nodes", response.data)
    //   }).catch((err) => {
    //     console.log("Error >> ", err);
        
    //   })
      
    // }
  },
  modules: {
  }
})
