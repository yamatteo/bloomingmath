<template>
  <router-view />
</template>

<script>
  export default {
    components: {
      // Baseline: () => import('@/views/Baseline.vue')
    },
    props: {
      source: String,
    },
    data: () => ({
      drawer: null,
    }),
  }
</script>