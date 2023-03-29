<script setup>
import { RouterLink, RouterView } from "vue-router";
</script>
<template>
  <header>
    <div class="wrapper">
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/timeline"> Timeline</RouterLink>
      </nav>
    </div>
  </header>

  <Suspense>
  <RouterView />
  </Suspense>
</template>
<style scoped>
</style>
