import Vue from 'vue'
import Vuelidate from 'vuelidate';
import VueNotifications from 'vue-notifications';
import App from './App.vue'
import router from './router'
import { notificationOptions } from './services/notification';

Vue.config.productionTip = false

Vue.use(Vuelidate);
Vue.use(VueNotifications, notificationOptions)

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
