<template>
  <!-- <b-badge pill @click="$emit('click')">
    <i :class="`fas fa-${icon}`"></i>
  </b-badge> -->
  <b-button pill @click="$emit('click')">
    <i :class="`fas fa-fw fa-${icon} m-0`"></i>
  </b-button>
</template>

<script>
module.exports = {
  name: "base-badge",
  props: {
    icon: {
      type: String,
      default: "box"
    }
  },
};
</script>

<style scoped>
.btn   {
  width: 2.2em;
  height: 2.2em;
  margin: -0.5em 0.2em;
  padding: 6px 12px 8px 7px;
  text-align: center;
}

.fas {
  font-size: 100%;
}
</style>