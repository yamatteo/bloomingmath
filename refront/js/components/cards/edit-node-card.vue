<template>
  <base-card :title="`Node ${id}`" :over-body="loading">
    <template v-slot:pills>
      <base-badge icon="save" @click="save"></base-badge>
    </template>
    <div>
      <div v-if="!loading">
        <base-input v-model="node.short"></base-input>
        <base-textarea v-model="node.long"></base-textarea>

        <b-container>
          <b-row v-for="(external, index) in node.externals"
            :key="index" class="mt-2">
            <b-col>
            <base-input v-model="external.short"></base-input>
            <base-input v-model="external.url"></base-input>
            <base-textarea v-model="external.long"></base-textarea>
            </b-col>
            </b-row>
            <b-row class="mt-2">
              <b-col>
              <base-button @click="add_external">Nuovo contenuto</base-button>
              </b-col>
            </b-row>
        </b-container>
      </div>
    </div>
  </base-card>
</template>

<script>
module.exports = {
  name: "edit-node-card",
  components: {
    "base-badge": window.httpVueLoader("/js/components/bases/base-badge.vue"),
    "base-button": window.httpVueLoader("/js/components/bases/base-button.vue"),
    "base-card": window.httpVueLoader("/js/components/bases/base-card.vue"),
    "base-input": window.httpVueLoader("/js/components/bases/base-input.vue"),
    "base-textarea": window.httpVueLoader(
      "/js/components/bases/base-textarea.vue"
    ),
    "users-card": window.httpVueLoader("/js/components/cards/users-card.vue")
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
    node: null,
    loading: true
  }),
  computed: {
    // find_members() {
    //   var id_array = new Array();
    //   for (user of this.group.members) {
    //     id_array.push(user.id);
    //   }
    //   return { id: { $in: id_array } };
    // }
  },
  methods: {
    add_external() {
      this.node.externals.push({
        short: "",
        url: "",
        long: ""
      })
    },
    fetch() {
      this.loading = true;
      post("/nodes/read", {
        find: { id: this.id }
      })
        .then(result => {
          this.node = result.data;
          console.log("This", this.node);
        })
        .catch(error => {
          console.log("POST /nodes/read", error);
        })
        .then(() => {
          this.loading = false;
        });
    },
    save() {
      this.loading = true;
      post("/nodes/edit", {
        find: { id: this.id },
        data: this.node
      })
        .then(result => {
          console.log(result.data);
          this.callback();
          this.removecard("edit-node", { id: this.id });
        })
        .catch(error => {
          console.log("POST /nodes/edit", error);
        })
        .then(() => {
          this.loading = false;
        });
    },
    getkey(obj) {
      return "external" + Math.random().toString(36)
    }
  },
  mounted() {
    this.fetch();
  }
};
</script>

<style scoped>
</style>