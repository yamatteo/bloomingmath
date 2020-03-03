<template>
  <a
    class="list-group-item list-group-item-action d-flex justify-content-between align-items-center"
    @click="main"
  >
    {{ text }}
    <span>
      <slot></slot>
    </span>
  </a>
</template>

<script>
  export default {
    props: {
      text: String,
      main: {
        type: Function,
        default: () => {console.log("click")}
      }
    }
  }
</script>

<style scoped>
.list-group-item  {
  padding: .25rem .75rem;
}
</style>