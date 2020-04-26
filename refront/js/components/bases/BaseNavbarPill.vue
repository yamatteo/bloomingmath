<template>
  <b-button pill class="px-2 m-1" @click="onClick">
    <slot>
      <i :class="`fas fa-${icon} mx-1`"></i>
      <span class="d-sm-none mx-2">{{ text }}</span>
    </slot>
  </b-button>
</template>

<script>
module.exports = {
  name: "BaseNavbarPill",
  props: {
    icon: {
      type: String,
      default: "square"
    },
    text: {
      type: String,
      default: "Click here"
    },
    onClick: {
      type: Function,
      default: () => {
        return false;
      }
    }
  }
};
</script>

<style scoped>
</style>