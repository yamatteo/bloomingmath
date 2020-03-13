<template>
  <b-list-group flush>
    <slot name="header"></slot>
    <slot>
      <slot name="empty">
      </slot>
    </slot>
  </b-list-group>
</template>

<script>
export default {
  name: "BaseListGroup"
};
</script>

<style scoped>
</style>