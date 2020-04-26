<template>
  <b-button block @click="$emit('click', $event)">
    <slot>Click</slot>
  </b-button>
</template>

<script>
module.exports = {
  name: "base-button",
  props: {
    value: {
      type: String,
      default: ""
    },
    icon: {
      type: String,
      default: "user"
    },
    placeholder: {
      type: String,
      default: "Write here..."
    },
    type: {
      type: String,
      default: "text"
    }
  },
};
</script>

<style scoped>
.input-group-text {
  width: 3em;
  text-align: center;
}
</style>