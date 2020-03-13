<template>
  <b-list-group-item class="d-flex align-items-center" :disabled="disabled">
    <span class="m-0 flex-grow-1" :style="onClick ? 'cursor: pointer;' : ''" @click="clicker">
      <slot>LGI short</slot>
    </span>
    <slot name="pills"></slot>
  </b-list-group-item>
</template>

<script>
export default {
  props: {
    onClick: {
      default: null
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    clicker() {
      if (this.onClick==null) return () => {}
      else return this.onClick
    }
  }

};
</script>

<style scoped>
</style>