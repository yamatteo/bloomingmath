<template>
  <base-card
    :title="title"
    collapsed
    :over-body="loading"
    @header_click="() => { if(!this.nodes) fetch() }"
  >
    <b-list-group flush>
      <b-list-group-item
        button
        v-for="node in nodes"
        :key="node.id"
        class="d-flex justify-content-between align-items-center"
      >
        {{ node.short }}
        <span>
          <base-badge></base-badge>
          <base-badge pill icon="edit" @click="edit(node.id)">
        </span>
      </b-list-group-item>
      <b-list-group-item v-if="!noAdd" button variant="secondary" @click="add">Aggiungi uno</b-list-group-item>
    </b-list-group>
  </base-card>
</template>

<script>
module.exports = {
  name: "nodes-card",
  components: {
    "base-card": window.httpVueLoader("/js/components/bases/base-card.vue"),
    "base-badge": window.httpVueLoader("/js/components/bases/base-badge.vue"),
  },
  props: {
    title: {
      type: String,
      default: "Argomenti"
    },
    noAdd: {
      type: Boolean,
      default: false
    },
    find: {
      type: Object,
      default: () => ({})
    }
  },
  data: () => ({
    nodes: null,
    loading: false
  }),
  computed: {},
  methods: {
    edit(id) {
      this.pushcard("edit-node", { id: id, callback: this.fetch.bind(this) });
    },
    add() {
      post("/nodes/add", {
        short: "new node's name"
      })
        .then(result => {
          this.fetch();
        })
        .catch(error => {
          console.log("POST /nodes/add", error);
        });
    },
    fetch() {
      this.loading = true;
      console.log("...fetching", this.find);

      post("/nodes/browse", this.find)
        .then(result => {
          this.nodes = result.data;
        })
        .catch(error => {
          console.log("POST /nodes/browse", error);
          this.nodes = [];
        })
        .then(() => {
          this.loading = false;
        });
    }
  }
};
</script>

<style scoped>
</style>