import Vue from 'vue'
import './plugins/bootstrap-vue'
import './plugins/axios'
import App from './App.vue'
import './registerServiceWorker'
import store from './store'
import VueSession from 'vue-session'
// import VueLodash from 'vue-lodash'
// import lodash from 'lodash'
 

// Vue.use(VueLodash, {name: "lodash"})
Vue.use(VueSession, {persist: true})
Vue.config.productionTip = false

new Vue({
  store,
  render: h => h(App)
}).$mount('#app')
