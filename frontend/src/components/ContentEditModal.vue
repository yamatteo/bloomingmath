<template>
  <b-modal
    id="ContentEditModal"
    v-model="visible"
    @ok.prevent="save"
    okTitle="Salva"
    @hide="destroy"
    cancelTitle="Annulla"
  >
    <template v-slot:modal-header>
      <h5 class="modal-title">Modifica contenuto</h5>
    </template>

    <div class="form-group mb-2">
      <label for="edit_content_modal_short">Short</label>
      <b-form-input
        type="text"
        class="form-control"
        id="edit_content_modal_short"
        placeholder="Titolo del contenuto"
        v-model="content.short"
      />
    </div>

    <div class="form-group mb-2">
      <label for="edit_content_modal_long">Long</label>
      <b-form-textarea
        v-model="content.long"
        placeholder="Descrizione del contenuto..."
        rows="3"
        max-rows="6"
        class="form-control"
        id="edit_content_modal_long"
      ></b-form-textarea>
    </div>
    
    

    <div class="form-group mb-2">
      <label for="edit_content_modal_long">File ({{ content.original_filename }})</label>
      <LittleForm :path="'/contents/upload/' + content.id" confirmation>
        <b-form-file
          v-model="file"
          name="data"
          placeholder="Choose a file or drop it here..."
          drop-placeholder="Drop file here..."
        ></b-form-file>
        <input type="submit" size="sm" value="Upload"/>
      </LittleForm>
    </div>

    <div class="mb-2">
      <LittleForm path="/contents/delete" :success="destroy_and_update_admin" :hidden_data="{'id': content.id}" confirmation>
        <b-button class="w-100" type="submit" variant="outline-danger">Elimina il contenuto</b-button>
      </LittleForm>
    </div>


  </b-modal>
</template>

<script>
export default {
  components: {
    ListGroupItem: () => import("@/components/ListGroupItem"),
    LgiButton: () => import("@/components/LgiButton"),
    LittleForm: () => import("@/components/LittleForm")
  },
  props: {
    content: Object,
    destroy: Function
  },
  data: () => ({
    visible: true,
    file: null
  }),
  computed: {},
  methods: {
    destroy_and_update_admin() {
      this.$store.commit("admin_update", true)
      this.destroy()
    },
    save() {
      console.log("Saving content", this.content);
      this.axios
        .post("/contents/edit", {
          find: {
            id: this.content.id
          },
          data: this.content
        })
        .then(response => {
          console.log("Success (content edit) >>", response.data);
          this.$store.commit("admin_update", true);
        })
        .catch(err => {
          console.log("Error (content edit) >>", err);
        });
    }
  }
};
</script>

<style scoped>
.scrollable {
  max-height: 12em;
  overflow-y: auto;
}
</style>