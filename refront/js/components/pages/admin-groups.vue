<template>
  <b-container class="mt-4">
    <b-row class="mb-3">
      <b-col>
        <h2 class="mb-3">Admin groups</h2>
      </b-col>
    </b-row>
    <b-row v-if="ready">
      <b-col>
        <base-card title="Groups">
          <base-list
            :array="groups"
            :pills="[
              {icon: 'pencil-alt', callback: item => edit(item.id)},
              {icon: 'times', callback: item => remove(item.id)},
            ]"
          ></base-list>
          <b-button block @click="add">Add one</b-button>
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
  name: "admin-groups-page",
  components: {
    "base-card": window.httpVueLoader("/js/components/bases/base-card.vue"),
    "base-list": window.httpVueLoader("/js/components/bases/base-list.vue")
  },
  data() {
    return {
      groups: null,
      waiting: false
    };
  },
  computed: {
    ready() {
      return !this.waiting && this.groups != null;
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
    async fetch_groups() {
      const result = await post("/groups/browse");
      this.groups = result.data;
    },
    async add() {
      this.waiting = true;
      await post("/groups/add", {
        short: "new group"
      });
      await this.fetch_groups();
      this.waiting = false;
    },
    async remove(group_id) {
      this.waiting = true;
      await post("/groups/delete", {
        id: group_id
      });
      await this.fetch_groups();
      this.waiting = false;
    },
    edit(group_id) {
      this.goto("edit-group", {
        group_id: group_id,
        unatantum_action_callback: () => this.goto("admin-groups")
      });
    }
  },
  mounted() {
    this.fetch_groups();
  }
};
</script>

<style scoped>
</style>