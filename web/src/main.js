import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import axios from 'axios';
import VueAxios from 'vue-axios';

import "./assets/main.css";

import HistogramSlider from "vue3-histogram-slider";
import "vue3-histogram-slider/dist/histogram-slider.css";

import ganttastic from '@infectoone/vue-ganttastic'

const app = createApp(App);

app.component(HistogramSlider.name, HistogramSlider)

app.config.productionTip = false;

// Axios Plugin
app.use(VueAxios, axios);
app.provide('axios', app.config.globalProperties.axios)

app.use(router);
app.use(ganttastic);

app.mount("#app");
