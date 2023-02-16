import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import axios from 'axios';
import VueAxios from 'vue-axios';

import "./assets/main.css";

import HistogramSlider from "vue3-histogram-slider";
import "vue3-histogram-slider/dist/histogram-slider.css";

import VueMultiselect from 'vue-multiselect'
import "vue-multiselect/dist/vue-multiselect.css"

const app = createApp(App);

app.component(HistogramSlider.name, HistogramSlider)

app.config.productionTip = false;

// Axios Plugin
app.use(VueAxios, axios);
app.provide('axios', app.config.globalProperties.axios)

app.use(router);

app.mount("#app");