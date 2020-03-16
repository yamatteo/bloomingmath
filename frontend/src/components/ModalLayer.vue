<template>
  <div id="modal-layer">
    <AlertModal v-if="alert"></AlertModal>
    <LoginModal v-else-if="!logged && login"></LoginModal>
    <BaseModal v-else-if="!logged && !login" id="signup_modal" title="Crea un profilo" force></BaseModal>
  </div>
</template>

<script>
export default {
  components: {
    BaseModal: () => import("@/components/modals/BaseModal"),
    AlertModal: () => import("@/components/modals/AlertModal"),
    LoginModal: () => import("@/components/modals/LoginModal"),
  },
  data: () => ({
    login: true
  }),
  computed: {
    logged() {
      return this.$store.state.authtoken != null;
    },
    alert() {
      return this.$store.state.alert
    }
  }
};
</script>

<style scoped>
</style>