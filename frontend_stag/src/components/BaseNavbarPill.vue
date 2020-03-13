<template>
  <b-button pill class="px-2 m-1" @click="onClick">
    <slot>
      <font-awesome-icon :icon="icon" class="mx-1"></font-awesome-icon>
      <span class="d-sm-none mx-2">{{ text }}</span>
    </slot>
  </b-button>
</template>

<script>
export default {
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