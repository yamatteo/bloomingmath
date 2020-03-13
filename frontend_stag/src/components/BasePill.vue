<template>
  <b-button pill @click.stop="onClick">
    <slot>
      <font-awesome-icon :icon="icon"></font-awesome-icon>
      <span v-if="text != ''" class="mx-2">{{ text }}</span>
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
      default: ""
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
.btn {
  padding: .3rem;
  margin: -0.3rem 0.3rem;
}
svg {
  margin: 0rem .3rem;
}
</style>