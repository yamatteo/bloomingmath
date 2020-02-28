<template>
  <b-modal
    v-model="modalShow"
    id="content-modal"
    @ok.prevent="save"
    okTitle="Salva"
    @hide="quit"
    cancelTitle="Annulla"
  >
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
    <b-input-group prepend="Short" class="my-2">
      <b-form-input v-model="content.short" placeholder="Breve descrizione"></b-form-input>
    </b-input-group>

    <b-input-group prepend="Type" class="my-2">
      <b-form-input v-model="content.filetype" placeholder="Estensione"></b-form-input>
    </b-input-group>

    <b-form-file
      v-model="file_to_upload"
      :state="Boolean(file_to_upload)"
      placeholder="Scegli un file da sostituire come contenuto"
      drop-placeholder="Drop file here..."
      browse-text="Browse"
    ></b-form-file>
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
    modalShow: true,
    file_to_upload: null
  }),
  computed: {
    is_admin() {
      try {
        return this.$store.state.current_user.is_admin;
      } catch {
        return false;
      }
    }
  },
  methods: {
    save() {
      console.log(
        "Saving content",
        this.content,
        "withi file",
        this.file_to_upload
      );
      this.axios
        .post("/contents/edit", {
          find: {
            id: this.content.id
          },
          data: this.content
        })
        .then(response => {
          console.log("Success (content edit) >>", response.data);

          if (this.file_to_upload != null) {
            let formData = new FormData();
            formData.append("data", this.file_to_upload);
            this.axios
              .post("/contents/upload/" + this.content.id, formData, {
                headers: {
                  "Content-Type": "multipart/form-data"
                }
              })
              .then(response => {
                console.log("Success (save) >>", response.data);
                this.$store.dispatch("fetch_current_user");
              })
              .catch(err => {
                console.log("Error (save) >>", err);
              });
          } else {
            this.$store.dispatch("fetch_current_user");
          }
        })
        .catch(err => {
          console.log("Error (content edit) >>", err);
        });
    },
    quit() {
      this.active_content_setter(null);
    }
  }
};
</script>

<style scoped>
</style>