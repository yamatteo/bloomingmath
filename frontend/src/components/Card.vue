<template>
  <b-card header-tag="header" class="mb-2" :body-class="scroll ? 'scroll' : ''">
    <template v-slot:header>
      <h6 class="mb-0">{{ title }}</h6>
    </template>
    <slot></slot>
  </b-card>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      default: "*** card title ***"
    },
    scroll: {
      type: Boolean,
      default: true
    }
  }
};
</script>

<style scoped>
.scroll {
    max-height: 600px;
    overflow-y: auto;
}
</style>