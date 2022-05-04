<script lang="ts">
  import SessionCard from "./SessionCard.svelte";

  export let name: string;
  let users: List = [];
  // const groupByKey = (list, key) =>
  //   list.reduce(
  //     (hash, obj) => ({
  //       ...hash,
  //       [obj[key]]: (hash[obj[key]] || []).concat(obj),
  //     }),
  //     {}
  //   );
  async function fetchUsers() {
    const response = await fetch("http://localhost:5000/api/v1/users");
    users = await response.json();
    users = Object.entries(users);
    console.log("users:", users);
  }
</script>

<main>
  <h1>Hello {name}!</h1>
  <button on:click={fetchUsers}>Fetch Repo Data!</button>
  <div class="grid">
    {#each users as [user, sessions]}
      <div>{user}</div>
      {#each sessions as session}
        <SessionCard {session} />
      {/each}
    {/each}
  </div>
</main>

<style>
  main {
    text-align: center;
    padding: 40px 0;
    margin: 0 auto;
  }
  h1 {
    color: #ff3e00;
    text-transform: uppercase;
    font-size: 4em;
    font-weight: 100;
  }
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 30px;
  }
  @media (min-width: 640px) {
    main {
      max-width: 1600px;
      padding: 40px 20px;
    }
  }
</style>
