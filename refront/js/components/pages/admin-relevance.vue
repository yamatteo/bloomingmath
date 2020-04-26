<template>
  <b-container class="mt-4">
    <b-row class="mb-3">
      <b-col>
        <h2 class="mb-3">Admin relevance</h2>
      </b-col>
    </b-row>
    <b-row v-if="ready" class="mb-3">
      <b-col>
        <b-form-select v-model="selected_group" :options="groups_options"></b-form-select>
      </b-col>
      <b-col>
        <b-form-select v-model="selected_node" :options="nodes_options"></b-form-select>
      </b-col>
    </b-row>
    <b-row v-if="ready && selected_group && selected_node">
      <b-col>
        <b-button
          block
          :variant="relevant ? 'warning' : 'success'"
          @click="event => {
            if (relevant) {
              pull_node(selected_group, selected_node)
            } else {
              push_node(selected_group, selected_node)
            }
          }"
        >{{ relevant ? 'Remove relevance' : 'Make it relevant'}}</b-button>
      </b-col>
    </b-row>
    <b-row v-if="!ready">
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
  name: "admin-relevance-page",
  components: {
    "base-card": window.httpVueLoader("/js/components/bases/base-card.vue"),
    "base-list": window.httpVueLoader("/js/components/bases/base-list.vue")
  },
  props: {
    preselected_group: {
      type: String,
      default: null
    },
    preselected_node: {
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
      groups: null,
      nodes: null,
      selected_group: this.preselected_group,
      selected_node: this.preselected_node,
      waiting: false
    };
  },
  computed: {
    ready() {
      return !this.waiting && this.groups != null && this.nodes != null;
    },
    groups_dict() {
      try {
        return this.groups.reduce(
          (acc, group) => Object.assign(acc, { [group.id]: group }),
          new Object()
        );
      } catch {
        return new Object();
      }
    },
    groups_options() {
      try {
        return [
          { value: null, text: "Scegli un gruppo" },
          ...this.groups.map(group => ({
            value: group.id,
            text: group.short
          }))
        ];
      } catch {
        return [{ value: null, text: "No group to choose" }];
      }
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
    relevant() {
      try {
        return this.groups_dict[this.selected_group].nodes
          .map(node => node.id)
          .includes(this.selected_node);
      } catch {
        return null;
      }
    }
  },
  methods: {
    async fetch_groups() {
      const result = await post("/groups/browse");
      this.groups = result.data;
    },
    async fetch_nodes() {
      const result = await post("/nodes/browse");
      this.nodes = result.data;
    },
    async pull_node(group_id, node_id) {
      this.waiting = true;
      await post("/groups/pull_node", {
        node_id: node_id,
        group_id: group_id
      });
      this.unatantum_action_callback();
      await this.fetch_groups();
      this.waiting = false;
    },
    async push_node(group_id, node_id) {
      this.waiting = true;
      await post("/groups/push_node", {
        node_id: node_id,
        group_id: group_id
      });
      this.unatantum_action_callback();
      await this.fetch_groups();
      this.waiting = false;
    }
  },
  mounted() {
    this.fetch_groups();
    this.fetch_nodes();
  }
};
</script>

<style scoped>
</style>