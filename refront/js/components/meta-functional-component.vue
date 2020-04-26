<template>
  <component :is="tag" v-bind="args">
  </component>
</template>

<script>
module.exports = {
  name: "meta-functional-component",
  components: {},
  props: ["tag", "args"]
};
</script>

<style scoped>
</style>