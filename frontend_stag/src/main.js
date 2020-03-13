import '@babel/polyfill'
import 'mutationobserver-shim'
import Vue from 'vue'
import './plugins/bootstrap-vue'
import './plugins/axios'
import './plugins/fontawesome'
import App from './App.vue'
import './registerServiceWorker'
import store from './store'
import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue'

import VueSession from 'vue-session'

Vue.use(VueSession, {persist: true})
Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)

Vue.config.productionTip = false


Vue.component("BaseCard", () => import("@/components/BaseCard"))
Vue.component("BasePill", () => import("@/components/BasePill"))
Vue.component("BaseListGroup", () => import("@/components/BaseListGroup"))
Vue.component("BaseListGroupItem", () => import("@/components/BaseListGroupItem"))
Vue.component("BasePage", () => import("@/components/pages/BasePage"))

new Vue({
  store,
  render: h => h(App)
}).$mount('#app')
