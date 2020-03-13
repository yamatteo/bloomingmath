import Vue from 'vue'

import { library } from '@fortawesome/fontawesome-svg-core'
import { faSquare, faPowerOff, faUser, faTimesCircle, faThumbsUp } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faSquare, faPowerOff, faUser, faTimesCircle, faThumbsUp)
Vue.component('font-awesome-icon', FontAwesomeIcon)

