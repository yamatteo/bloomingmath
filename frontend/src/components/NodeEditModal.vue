<template>
  <b-modal
    id="NodeEditModal"
    v-model="visible"
    @ok.prevent="save"
    okTitle="Salva"
    @hide="destroy"
    cancelTitle="Annulla"
  >
    <template v-slot:modal-header>
      <h5 class="modal-title">Modifica argomento</h5>
    </template>

    <div class="form-group mb-2">
      <label for="edit_node_modal_short">Short</label>
      <b-form-input
        type="text"
        class="form-control"
        id="edit_node_modal_short"
        placeholder="Titolo dell'argomento"
        v-model="node.short"
      />
    </div>

    <div class="form-group mb-2">
      <label for="edit_node_modal_long">Long</label>
      <b-form-textarea
        v-model="node.long"
        placeholder="Descrizione del argomento..."
        rows="3"
        max-rows="6"
        class="form-control"
        id="edit_node_modal_long"
      ></b-form-textarea>
    </div>

    <div class="form-group mb-2 scrollable">
      <label for="edit_group_modal_contents">Contenuti</label>
      <ul v-if="node.contents.length" class="list-group list-group-flush">
        <ListGroupItem v-for="(content, index) in node.contents" :key="content.id" :text="content.short">
          <LgiButton :click_handler="() => pull_content(content, index)" icon="x" />
        </ListGroupItem>
      </ul>
      <div v-else class="mb-2">
        <b>Nessun contenuto per questo argomento.</b>
      </div>
      <ul v-if="node.other_contents.length"  class="list-group list-group-flush">
        <b>Aggiungine alcuno <b-icon-arrow-up /></b>
        <ListGroupItem v-for="(content, index) in node.other_contents" :key="content.id" :text="content.short">
          <LgiButton :click_handler="() => push_content(content, index)" icon="plus" />
        </ListGroupItem>
      </ul>
    </div>

    <div class="mb-2">
      <LittleForm path="/nodes/delete" :success="destroy_and_update_admin" :hidden_data="{'id': node.id}" confirmation>
        <b-button class="w-100" type="submit" variant="outline-danger">Elimina l'argomento</b-button>
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
    node: Object,
    destroy: Function
  },
  data: () => ({
    visible: true
  }),
  computed: {},
  methods: {
    destroy_and_update_admin() {
      this.$store.commit("admin_update", true)
      this.destroy()
    },
    save() {
      console.log("Saving argument", this.group);
      this.axios
        .post("/nodes/edit", {
          find: {
            id: this.node.id
          },
          data: this.node
        })
        .then(response => {
          console.log("Success (node edit) >>", response.data);
          this.$store.commit("admin_update", true);
        })
        .catch(err => {
          console.log("Error (node edit) >>", err);
        });
    },
    push_content(content, index) {
      if (this.node.other_contents.includes(content)) {
        this.node.contents.push(content);
        this.node.other_contents.splice(index, 1);
      }
    },
    pull_content(content, index) {
      if (this.node.contents.includes(content)) {
        this.node.other_contents.push(content);
        this.node.contents.splice(index, 1);
      }
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