<template>
  <b-modal v-model="modalShow" id="content-modal" @ok.prevent="save" okTitle="Salva" @hide="quit" cancelTitle="Annulla">
    <template v-slot:modal-header>
      <h5 class="modal-title">Modifica contenuto</h5>
    </template>
    <b-alert
      v-if="alert_message"
      show
      dismissible
      variant="warning"
      @dismissed="dismiss_alert_message"
    >{{ alert_message }}</b-alert>
    <p>Modifiche al contenuto {{ content.short }}...</p>
  </b-modal>
</template>

<script>
export default {
  props: {
    content: Object,
    active_content_setter: Function
  },
  data: () => ({
    alert_message: null,
    modalShow: true
  }),
  computed: {
    is_admin() {
      try {
        return this.$store.state.current_user.is_admin;
      } catch {
        return false;
      }
    },
  },
  methods: {
    save() {
      console.log("save method...")
    },
    quit() {
      this.active_content_setter(null)
    }
  }
};
</script>

<style scoped>
</style>