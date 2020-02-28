<template>
  <a
    class="list-group-item list-group-item-action d-flex justify-content-between align-items-center"
    :href="'/contents/download/' + content.id"
  >
    {{ content.short }}
    <span v-if="is_admin">
      <span class="badge badge-secondary badge-pill" @click.stop.prevent="active_content_setter(content)"><b-icon-pencil font-scale="2"/></span>
    </span>
  </a>
</template>

<script>
export default {
  props: {
    content: Object,
    active_content_setter: Function
  },
  data: () => ({}),
  computed: {
    is_admin() {
      try {
        return this.$store.state.current_user.is_admin
      } catch {
        return false
      }
    }
  },
  methods: {}
};
</script>

<style scoped>
.list-group-item {
  background: #f8f9fa;
}
</style>