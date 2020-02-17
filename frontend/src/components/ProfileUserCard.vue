<template>
  <b-card header-tag="header">
    <template v-slot:header>
      <h6 class="mb-0">Informazioni utente</h6>
    </template>
    <p><b>La tua email:</b> {{ current_user.email }}</p>
  </b-card>
</template>

<script>
export default {
  computed: {
    current_user() {
      return this.$store.state.current_user
    }
  }
};
</script>