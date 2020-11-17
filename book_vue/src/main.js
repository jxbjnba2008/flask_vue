import Vue from 'vue';
import App from './App.vue';
import router from './router';
// import store from './store/index';
import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue';

// import Mint from 'mint-ui';
// import 'mint-ui/lib/style.css';
// import './components/lib/mui/css/mui.css';
// import mui from './components/lib/mui/js/mui.min.js';
// import './components/lib/mui/fonts/mui.ttf';

import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);

Vue.config.productionTip = false;

new Vue({
  router,
  // store,
  render: h => h(App)
}).$mount('#app');