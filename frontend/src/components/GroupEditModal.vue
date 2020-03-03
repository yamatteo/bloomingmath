<template>
  <b-modal
    id="GroupEditModal"
    v-model="visible"
    @ok.prevent="save"
    okTitle="Salva"
    @hide="destroy"
    cancelTitle="Annulla"
  >
    <template v-slot:modal-header>
      <h5 class="modal-title">Modifica gruppo</h5>
    </template>

    <div class="form-group mb-2">
      <label for="edit_group_modal_short">Short</label>
      <b-form-input
        type="text"
        class="form-control"
        id="edit_group_modal_short"
        placeholder="Breve nome del gruppo"
        v-model="group.short"
      />
    </div>

    <div class="form-group mb-2">
      <label for="edit_group_modal_long">Long</label>
      <b-form-textarea
        v-model="group.long"
        placeholder="Descrizione del gruppo..."
        rows="3"
        max-rows="6"
        class="form-control"
        id="edit_group_modal_long"
      ></b-form-textarea>
    </div>

    <div class="form-group mb-2 scrollable">
      <label for="edit_group_modal_nodes">Argomenti</label>
      <ul v-if="group.nodes.length" class="list-group list-group-flush">
        <ListGroupItem v-for="(node, index) in group.nodes" :key="node.id" :text="node.short">
          <LgiButton :click_handler="() => pull_node(node, index)" icon="x" />
        </ListGroupItem>
      </ul>
      <div v-else class="mb-2">
        <b>Nessun argomento per questo gruppo.</b>
      </div>
      <ul v-if="group.other_nodes.length"  class="list-group list-group-flush">
        <b>Aggiungine alcuno <b-icon-arrow-up /></b>
        <ListGroupItem v-for="(node, index) in group.other_nodes" :key="node.id" :text="node.short">
          <LgiButton :click_handler="() => push_node(node, index)" icon="plus" />
        </ListGroupItem>
      </ul>
    </div>

    <div class="mb-2">
      <LittleForm path="/groups/delete" :success="destroy_and_update_admin" :hidden_data="{'id': group.id}" confirmation>
        <b-button class="w-100" type="submit" value="Elimina il " variant="outline-danger">Elimina il gruppo</b-button>
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
    group: Object,
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
      console.log("Saving group", this.group);
      this.axios
        .post("/groups/edit", {
          find: {
            id: this.group.id
          },
          data: this.group
        })
        .then(response => {
          console.log("Success (group edit) >>", response.data);
          this.$store.commit("admin_update", true);
        })
        .catch(err => {
          console.log("Error (group edit) >>", err);
        });
    },
    push_node(node, index) {
      if (this.group.other_nodes.includes(node)) {
        this.group.nodes.push(node);
        this.group.other_nodes.splice(index, 1);
      }
    },
    pull_node(node, index) {
      if (this.group.nodes.includes(node)) {
        this.group.other_nodes.push(node);
        this.group.nodes.splice(index, 1);
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