<script setup>
  import { inject, ref, reactive } from "vue";
  // import VueMultiselect from 'vue-multiselect'
  const axios = inject('axios');
  const times = await axios.get(
    'http://127.0.0.1:5000/api/v1/times'
  ).then(
      response => {
        return response.data.map(d => new Date(d))
      })

  const prettify = function(ts) {
      return new Date(ts).toLocaleDateString("en", {
             year: "numeric",
             month: "short",
             day: "numeric"
            });
          }

  const state = reactive({
    user_repos: await get_repos(),
    users: Object.keys(await get_repos())
  })

  async function get_repos(date_min, date_max) {
    if (date_min == undefined) {
      date_min = new Date(Math.min.apply(null, times));
    }
    if (date_max == undefined) {
      date_max = new Date(Math.max.apply(null, times));
    }

    const data = await axios.get('http://127.0.0.1:5000/api/v1/user_repos', {
      params: {
        start_date: date_min.toISOString().substr(0,10),
        end_date: date_max.toISOString().substr(0,10)
      }
    }).then(
      response => {
        return response.data
      })

  return data
  }

async function get_filtered(values) {
    console.log(values)
    if (!values) {
      state.user_repos = await get_repos()
      state.users =  await Object.keys(state.user_repos)
    } else {
      const value_min = new Date(values.from)
      const value_max = new Date (values.to)
      state.user_repos = await get_repos(value_min, value_max)
      state.users = await Object.keys(state.user_repos)
    }
  }
  </script>

  <template>
    <main>
      <HistogramSlider
      :width="1280"
      :bar-height="200"
      :data="times"
      :prettify="prettify"
      :drag-interval="true"
      :force-edges="false"
      @finish="get_filtered"
    />

<div id="title-bar">
  <h1>ProgressBoard</h1>
  <!-- <VueMultiselect -->
  <!--     :value="value" -->
  <!--     :options="state.users" -->
  <!--     :multiple="true" -->
  <!--     :close-on-select="true" -->
  <!--     placeholder='Filter for users' -->
  <!--     label='filter-users' -->
  <!--     track-by='filter-users' -->
  <!--     > -->
  <!-- </VueMultiselect> -->
</div>
    <div id="table-wrapper">
<table id="man-heatmap">
  <tr class='header'>
    <th class='color title'></th>
    <th v-for="session in 15" :key="session" class='color session'><a href='#'>{{session}}</a></th>
  </tr>
  <tr v-for="(repos, user) in state.user_repos">
    <th class='color name'>
            <a :href="repos[0]['user_url']">
              <img :src="repos[0]['avatar']" :alt="user">
            </a>
            <a :href="repos[0]['user_url']">
              {{user}}
            </a>
    </th>
    <td v-for="session in 15" :key="session">
            <ul class='color'>
              <template v-for="repo in repos">
              <li v-if="repo['session'] == session" :key="session">
                <a :href="repo['latest_commit_url']">
                <button :class="[repo.status]" type="button" :title="[repo.name]">
                  {{ repo.exercise }}
                </button>
                </a>
              </li>
              </template>
            </ul>
        </td>
      </tr>
    </table>
    </div>
</main>
</template>
<style src="vue-multiselect/dist/vue-multiselect.css"></style>
<style>
    div#title-bar {
      background-color: #0091ff;
      max-width: 1280px;
      margin-top: 1em;
    }

    div#title-bar h1 {
      color: #fff !important;
      padding: 0 0 0 .5em;
      font-size: 180%;
      font-weight: bold;
      text-align: left;
      vertical-align: top;
    }

    .color_0, .color_1 { background-color: #949494; }
    .color_2, .color_3 { background-color: #AEAEAE; }
    .color_4, .color_5 { background-color: #EEECF1; }
    .color_6, .color_7 { background-color: #ADC3D1; }
    .color_8, .color_9 { background-color: #8FB1CC; }
    .color_10          { background-color: #759CC9; }


    div#table-wrapper {
      max-width: 1280px;
      overflow: auto;
    }

    table#man-heatmap {
      border-collapse:collapse;
      margin: 0;
      table-layout: fixed;
      max-width: 1280px;
      overflow: auto;
    }

    table#man-heatmap tr th.name {
      color: #0091ff !important;
      aspect-ratio: 1;
      border-color: #0091ff;
      border-style: solid;
      border-width: .2em 0 0 0 !important;
      vertical-align: top;
      text-align: left;
      background-color: #fff;
      padding: .5em 2em 2em 0;
      position: sticky;
      top: 0;
      left: 0;
      z-index: 10;
    }

    table#man-heatmap th a {
      text-decoration: none;
      color: #0091ff;
    }

    table#man-heatmap th.name img {
      width: 50%;
      height: 50%;
      margin: .3em 0 .3em 0;
      display: block;
    }

    table#man-heatmap tr.header th {
      background-color: #fff;
    }

    table#man-heatmap td {
      vertical-align: top;
      border-color: #0091ff;
      border-width: .2em .1em;
      border-style: solid dotted;
      padding: .8em 2em 2em .5em;
    }

    table#man-heatmap td ul {
      border-radius: 5%;
      padding: 0;
      display: grid;
      grid-template-columns: 1fr 1fr 1fr 1fr;
      grid-gap: 3% 5%;
      list-style-type: none;
    }

    table#man-heatmap button {
      cursor: pointer;
      border-radius: 20% !important;
      aspect-ratio: 1;
    }

    table#man-heatmap button.completed {background-color: #BEE5B0; border-color: #BEE5B0; color: #fff; }
    table#man-heatmap button.failing {background-color: #FB6962; border-color: #FB6962; color: #fff; }
    table#man-heatmap button.not-started {background-color: #fff; color: #AEAEAE; border-color: #fff; }
    table#man-heatmap button.rework {background-color: #FCFC99; color: #AEAEAE; border-color:  #FCFC99; }

    table#man-heatmap button:hover {
      filter: brightness(90%);
      width: 93%;
      height: 93%;
      /* font-weight: bold; */
    }
</style>
