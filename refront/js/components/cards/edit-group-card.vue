<template>
  <base-card :title="`Gruppo ${id}`" :over-body="loading">
    <template v-slot:pills>
      <base-badge icon="save" @click="save"></base-badge>
    </template>
    <div v-if="this.group">
      <base-input v-model="group.short"></base-input>
      <base-textarea v-model="group.long"></base-textarea>
      <users-card title="Membri" :find="find_members" collapsed no-add></users-card>
      <nodes-card title="Argomenti" :find="find_nodes" collapsed no-add></nodes-card>
    </div>
  </base-card>
</template>

<script>
module.exports = {
  name: "edit-group-card",
  components: {
    "base-badge": window.httpVueLoader("/js/components/bases/base-badge.vue"),
    "base-card": window.httpVueLoader("/js/components/bases/base-card.vue"),
    "base-input": window.httpVueLoader("/js/components/bases/base-input.vue"),
    "base-textarea": window.httpVueLoader(
      "/js/components/bases/base-textarea.vue"
    ),
    "users-card": window.httpVueLoader("/js/components/cards/users-card.vue"),
    "nodes-card": window.httpVueLoader("/js/components/cards/nodes-card.vue"),
  },
  props: {
    id: {
      type: String
    },
    callback: {
      type: Function,
      default: () => {
        console.log("Default callback");
      }
    }
  },
  data: () => ({
    group: null,
    loading: true
  }),
  computed: {
    find_members() {
      var id_array = new Array();
      for (user of this.group.members) {
        id_array.push(user.id);
      }
      return { id: { $in: id_array } };
    },
    find_nodes() {
      var id_array = new Array();
      for (node of this.group.nodes) {
        id_array.push(node.id);
      }
      return { id: { $in: id_array } };
    },
  },
  methods: {
    fetch() {
      this.loading = true;
      post("/groups/read", {
        find: { id: this.id }
      })
        .then(result => {
          this.group = result.data;
          console.log("This", this.group);
        })
        .catch(error => {
          console.log("POST /groups/read", error);
        })
        .then(() => {
          this.loading = false;
        });
    },
    save() {
      this.loading = true;
      post("/groups/edit", {
        find: { id: this.id },
        data: this.group
      })
        .then(result => {
          console.log(result.data);
          this.callback();
          this.removecard("edit-group", { id: this.id });
        })
        .catch(error => {
          console.log("POST /groups/edit", error);
        })
        .then(() => {
          this.loading = false;
        });
    }
  },
  mounted() {
    this.fetch();
  }
};
</script>

<style scoped>
</style>