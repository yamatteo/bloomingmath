<template>
  <a class="badge badge-secondary badge-pill" @click.stop.prevent="click_handler">
    <b-icon :icon="icon" font-scale="2"></b-icon>
  </a>
</template>

<script>
export default {
  props: {
    click_handler: Function,
    icon: String
  }
};
</script>

<style scoped>
</style>