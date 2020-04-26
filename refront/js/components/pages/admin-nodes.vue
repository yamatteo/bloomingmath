<template>
  <b-container class="mt-4">
    <b-row class="mb-3">
      <b-col>
        <h2 class="mb-3">Amministra nodi</h2>
      </b-col>
    </b-row>
    <b-row v-if="ready" class="mb-3">
      <b-col>
        <b-form-select v-model="selected_group" :options="groups_options"></b-form-select>
      </b-col>
    </b-row>
    <b-row v-if="ready">
      <b-col>
        <base-card :title="selected_group ? 'Nodes' : 'Orphan nodes'">
          <base-list
            :array="restricted_nodes"
            :pills="[
              {
                icon: selected_group ? 'unlink' : 'link',
                callback: selected_group ? (item) => {pull_node(item.id, selected_group)} : (item) => {push_node(item.id, selected_group)}
              }
            ]"
          ></base-list>
        </base-card>
      </b-col>
    </b-row>
    <b-row v-else>
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
  name: "admin-nodes-page",
  components: {
    "base-card": window.httpVueLoader("/js/components/bases/base-card.vue"),
    "base-list": window.httpVueLoader("/js/components/bases/base-list.vue")
  },
  data() {
    return {
      groups: null,
      nodes: null,
      selected_group: null
    };
  },
  computed: {
    ready() {
      return this.groups != null && this.nodes != null;
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
    restricted_nodes() {
      let groups_dict = this.groups_dict;
      let selected_group = this.selected_group;

      if (this.selected_group != null) {
        return this.nodes.filter(function(node) {
          let group = groups_dict[selected_group];
          for (gnode of group.nodes) {
            if (node.id == gnode.id) {
              return true;
            }
          }
          return false;
        });
      } else {
        return this.nodes.filter(function(node) {
          for (id in groups_dict) {
            for (gnode of groups_dict[id].nodes) {
              if (node.id == gnode.id) {
                return false;
              }
            }
          }
          return true;
        });
      }
    }
  },
  methods: {
    fetch() {
      post("/nodes/browse")
        .then(result => {
          this.nodes = result.data;
        })
        .catch(error => {
          console.log("/nodes/browse", error);
        });
      post("/groups/browse")
        .then(result => {
          this.groups = result.data;
        })
        .catch(error => {
          console.log("/groups/browse", error);
        });
    },
    pull_node(node_id, group_id) {
      post("/groups/pull_node", {
        node_id: node_id,
        group_id: group_id
      })
        .then(result => {
          this.fetch();
        })
        .catch(error => {
          console.log("/groups/pull_node", error);
        });
    },
    push_node(node_id, group_id) {
      console.log(node_id, group_id);
      
      this.goto("admin-relevance", {
        preselected_node: node_id,
        preselected_group: group_id
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