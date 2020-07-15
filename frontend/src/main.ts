import Vue from 'vue'
import Vuelidate from 'vuelidate';
import VueNotifications from 'vue-notifications';
import VueGoodTablePlugin from 'vue-good-table';
import App from './App.vue'
import router from './router'
import { notificationOptions } from './services/notification';
import { currencyFilter } from './filters';

Vue.config.productionTip = false

Vue.use(VueGoodTablePlugin);
Vue.use(Vuelidate);
Vue.use(VueNotifications, notificationOptions);

Vue.filter('currency', currencyFilter);

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
