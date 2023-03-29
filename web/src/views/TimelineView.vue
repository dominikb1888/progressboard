<script setup>
   import { inject, ref, reactive, toRaw } from "vue";
   import Multiselect from '@vueform/multiselect'

   const axios = inject('axios');

   const prettify = function(ts) {
       return new Date(ts).toLocaleDateString("en", {
              year: "numeric",
              month: "short",
              day: "numeric"
             });
           }

   const all_repos = await get_repos()

   function flatten_repos(user_repos) {
     let flat_repos = []
     for (const user in user_repos) {
       for (const repo of user_repos[user]) {
         flat_repos.push(repo)
       }
     }
   console.log(flat_repos)
     flat_repos = flat_repos.sort((a,b) => {
         return new Date(b['commits'][0]['commit']['author']['date']) - new Date(a['commits'][0]['commit']['author']['date']); // descending
     })

     return flat_repos
   }

   const state = reactive({
     user_repos: await get_repos(),
     repos: flatten_repos(all_repos),
     users: await get_users(),
     selected_users: null,
     selected_dates: null
   })


    async function get_repos(date_min, date_max) {
     if (date_min == undefined) {
       // date_min = new Date(Math.min.apply(null, times));
       date_min = new Date("2022-03-19T09:44:50Z")
     }
     if (date_max == undefined) {
       date_max = new Date();
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

  async function get_users() {
   const data = await axios.get('http://127.0.0.1:5000/api/v1/users').then(
       response => {
         return response.data
       })
   return data
   }

 function get_times(repos) {
     const times = []
     for (const repo of repos) {
       for (const commit of repo['commits']) {
         times.push(new Date(commit['commit']['author']['date']))
       }
     }
    return times
   }

   const times = get_times(flatten_repos(all_repos))



 async function get_date_filtered(values) {
     if (!values) {
       state.user_repos = await get_repos()
       state.repos = flatten_repos(state.user_repos)
       state.users =  await Object.keys(all_repos)
     } else {
       const value_min = new Date(values.from)
       const value_max = new Date(values.to)
       state.user_repos = await get_repos(value_min, value_max)
       state.repos = flatten_repos(state.user_repos)
       state.users = await Object.keys(state.user_repos)
     }
   }

 async function get_user_filtered() {
     let repos = new Object()
     let selected_users = toRaw(state.selected_users)
     for (var i =0; i < selected_users.length; i++) {
       let user = selected_users[i]
       repos[user] = all_repos[user]
     }
     state.user_repos = repos
 }
 </script>

 <template>
     <main>
   <div id="title-bar">
     <h1>ProgressBoard</h1>
     <Multiselect
         v-model="state.selected_users"
         mode="tags"
         placeholder="Select Users"
         valueProp="login"
         track-by="login"
         label="login"
         :close-on-select="false"
         :searchable="true"
         :options="state.users"
         @select="get_user_filtered"
         @deselect="get_user_filtered"
     >
         <template v-slot:tag="{ option, handleTagRemove, disabled }">
         <div
           class="multiselect-tag is-user"
           :class="{
             'is-disabled': disabled
           }"
         >
           <img height="20" :src="option.avatar_url">
           {{ option.login }}
           <span
             v-if="!disabled"
             class="multiselect-tag-remove"
             @click="handleTagRemove(option, $event)"
           >
             <span class="multiselect-tag-remove-icon"></span>
           </span>
         </div>
       </template>
       </Multiselect>
   </div>

   <table id="man-timeline">
     <tr class='header'>
       <th class='color title'></th>
       <th v-for="session in 31" :key="session" class='color session'><a href='#'>{{session}}</a></th>
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
       <td v-for="session in 31" :key="session">
               <ul class='color' v-for="repo in repos">
                 <template v-for="commit in repo['commits']">
                 <li v-if="(new Date(commit['commit']['author']['date'])).getDay() == session" :key="session">
                   <a :href="repo['latest_commit_url']" rel="noopener noreferrer" target="_blank">
                   <button :class="[repo.status]" type="button" :title="[repo.name]">
                       {{repo.session}}-{{repo.exercise}}
                   </button>
                   </a>
                 </li>
                 </template>
               </ul>
           </td>
         </tr>
       </table>
   </main>
 </template>

 <style src="@vueform/multiselect/themes/default.css"></style>

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


    table#man-timeline {
       border-collapse:collapse;
       margin: 0;
       table-layout: fixed;
       min-width: 19000px;
     }

     table#man-timeline tr th.name {
       color: #0091ff !important;
       aspect-ratio: 1;
       border-color: #0091ff;
       border-style: solid;
       border-width: .2em 0 0 0 !important;
       vertical-align: top;
       text-align: left;
       background-color: #fff;
       position: sticky;
       top: 0;
       left: 0;
       z-index: 10;
     }

     table#man-timeline th a {
       text-decoration: none;
       color: #0091ff;
     }

     table#man-timeline th.name img {
       width: 50%;
       height: 50%;
       margin: .3em 0 .3em 0;
       display: block;
     }

     table#man-timeline tr.header th {
       background-color: #fff;
     }

     table#man-timeline td {
       vertical-align: top;
       border-color: #0091ff;
       border-width: .2em .1em;
       border-style: solid dotted;
       width: 900px !important;
     }

     table#man-timeline td ul {
       border-radius: 5%;
       padding: 0;
     }

     table#man-timeline ul {
      clear: right;
     }

     table#man-timeline li {
       display: inline;
     }

     table#man-timeline button {
       cursor: pointer;
       padding: 0;
       margin: .2em;
       border-radius: 20% !important;
       aspect-ratio: 1;
     }

     table#man-timeline button.completed {background-color: #BEE5B0; border-color: #BEE5B0; color: #fff; }
     table#man-timeline button.failing {background-color: #FB6962; border-color: #FB6962; color: #fff; }
     table#man-timeline button.not-started {background-color: #fff; color: #AEAEAE; border-color: #fff; }
     table#man-timeline button.rework {background-color: #FCFC99; color: #AEAEAE; border-color:  #FCFC99; }

     table#man-timeline button:hover {
       filter: brightness(90%);
     }

 </style>

