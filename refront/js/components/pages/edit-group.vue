<template>
  <b-container class="mt-4">
    <b-row v-if="ready" class="mb-3">
      <b-col>
        <h2 class="mb-3">Edit group</h2>
        <base-card :title="group.short">
          <base-input icon="tag" v-model="group.short"></base-input>
          <base-card title="Nodes" class="mt-3">
            <boolean-list :array="node_selection_array" :boolean-toggler="toggle_node"></boolean-list>
          </base-card>
        </base-card>
        <b-button block @click="save">Done</b-button>
      </b-col>
    </b-row>
    <b-row v-if="!ready" class="mb-3">
      <b-col>
        <div class="text-center">
          <b-spinner></b-spinner>
        </div>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
module.exports = {
  name: "edit-group-page",
  components: {
    "base-card": window.httpVueLoader("/js/components/bases/base-card.vue"),
    "base-input": window.httpVueLoader("/js/components/bases/base-input.vue"),
    "base-list": window.httpVueLoader("/js/components/bases/base-list.vue"),
    "boolean-list": window.httpVueLoader("/js/components/boolean-list.vue")
  },
  props: {
    group_id: {
      type: String,
      default: null
    },
    unatantum_action_callback: {
      type: Function,
      default: function() {}
    }
  },
  data() {
    return {
      group: null,
      nodes: null,
      waiting: false
    };
  },
  computed: {
    ready() {
      return !this.waiting && this.group != null && this.nodes != null;
    },
    nodes_dict() {
      try {
        return this.nodes.reduce(
          (acc, node) => Object.assign(acc, { [node.id]: node }),
          new Object()
        );
      } catch {
        return new Object();
      }
    },
    nodes_options() {
      try {
        return [
          { value: null, text: "Select a node" },
          ...this.nodes.map(node => ({
            value: node.id,
            text: node.short
          }))
        ];
      } catch {
        return [{ value: null, text: "No node to choose" }];
      }
    },
    node_selection_array() {
      return this.nodes.map(node => {
        const relevant = this.group.nodes.map(gnode => gnode.id).includes(node.id)
        
        return {id: node.id, short: node.short, boolean_value: relevant}
      });
    }
  },
  methods: {
    async fetch_group() {
      const result = await post("/groups/read", {
        find: { id: this.group_id }
      });
      this.group = result.data;
    },
    async fetch_nodes() {
      const result = await post("/nodes/browse");
      this.nodes = result.data;
    },
    async pull_node(node_id) {
      this.waiting = true;
      await post("/groups/pull_node", {
        group_id: this.group_id,
        node_id: node_id
      });
      await this.fetch_group();
      this.waiting = false;
    },
    async push_node(node_id) {
      this.waiting = true;
      await post("/groups/push_node", {
        group_id: this.group_id,
        node_id: node_id
      });
      await this.fetch_group();
      this.waiting = false;
    },
    async save() {
      this.waiting = true;
      await post("/groups/edit", {
        find: { id: this.group_id },
        data: this.group
      });
      this.unatantum_action_callback();
      this.waiting = false;
    },
    async toggle_node(item, index) {
      const action = item.boolean_value ? '/groups/pull_node' : '/groups/push_node'
      await post(action, {
        group_id: this.group_id,
        node_id: item.id
      })
      await this.fetch_group()
      console.log("toggle_node is done");
      
      return 2
    }
  },
  mounted() {
    this.fetch_group();
    this.fetch_nodes();
  }
};
</script>

<style scoped>
</style>