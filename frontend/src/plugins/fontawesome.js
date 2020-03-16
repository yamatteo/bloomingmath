import Vue from 'vue'

import { library } from '@fortawesome/fontawesome-svg-core'
import { faSave, faSquare, faPowerOff, faUser, faTimesCircle, faThumbsUp, faKey, faEnvelope, faLock, faCheck, faAt, faPlus, faEdit } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faSave, faSquare, faPowerOff, faUser, faTimesCircle, faThumbsUp, faKey, faEnvelope, faLock, faCheck, faAt, faPlus, faEdit)
Vue.component('font-awesome-icon', FontAwesomeIcon)

