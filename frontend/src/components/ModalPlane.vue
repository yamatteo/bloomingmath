<template>
  <div>
    <ContentModal v-if="modal_name == 'ContentEditModal'" :content="modal_props.content" :destroy="destroy"/>
    <NodeEditModal v-if="modal_name == 'NodeEditModal'" :node="modal_props.node" :destroy="destroy"/>
    <GroupEditModal v-if="modal_name == 'GroupEditModal'" :group="modal_props.group" :destroy="destroy"/>
  </div>
</template>

<script>
  export default {
    components: {
      ContentModal: () => import("@/components/ContentModal"),
      NodeEditModal: () => import("@/components/NodeEditModal"),
      GroupEditModal: () => import("@/components/GroupEditModal")
    },
    computed: {
      modal_name() {
        try {
          return this.$store.state.active_modal.name
        } catch {
          return null
        }
      },
      modal_props() {
        try {
          return this.$store.state.active_modal.props
        } catch {
          return null
        }
      }
    },
    methods: {
      destroy() {
        this.$store.commit("active_modal", null)
      }
    }
  }
</script>

<style scoped>

</style>