<template>
  <b-card header-tag="header">
    <template v-slot:header>
      <h6 class="mb-0">Gruppi di appartenenza</h6>
    </template>

    <ul v-if="current_user.groups.length" class="list-group list-group-flush">
      <b>Gruppi di cui fai parte:</b>
      <GroupLgi
        v-for="group in current_user.groups"
        :key="group.id"
        :group="group"
        :active_group_setter="active_group_setter"
        :pull_yourself_from="pull_yourself_from"
      />
    </ul>
    <div v-else class="mb-2">
      <b>Non fai parte di nessun gruppo.</b>
    </div>
    

    <b-form-group v-if="available_groups.length" label="Entra in un gruppo" label-for="push_self">
      <b-input-group>
        <b-form-select
          id="push_self"
          v-model="selected_group_to_push_yourself_into"
          :options="available_groups_options"
        ></b-form-select>
        <b-button @click="push_self">Entra</b-button>
      </b-input-group>
    </b-form-group>

  </b-card>
</template>

<script>
export default {
  components: {
    GroupLgi: () => import("@/components/GroupLgi"),
    // ContentModal: () => import("@/components/ContentModal")
  },
  data: () => ({
    selected_group_to_push_yourself_into: null,
    selected_group_to_pull_yourself_from: null,
    active_group: null
  }),
  computed: {
    current_user() {
      return this.$store.state.current_user;
    },
    groups() {
      return this.$store.state.groups;
    },
    available_groups() {
      return this.current_user.available_groups
    },
    available_groups_options() {
      return this.available_groups.map(group => ({
        value: group.id,
        text: group.short
      }));
    },
    current_groups_options() {
      return this.current_user.groups.map(group => ({
        value: group.id,
        text: group.short
      }));
    }
  },
  methods: {
    push_self() {
      this.axios
        .post("/groups/push_self", {
          group_id: this.selected_group_to_push_yourself_into
        })
        .then(response => {
          console.log("Backend >> ", response.data);
          this.$store.dispatch("fetch_current_user");
        })
        .catch(err => {
          console.log("Error >> ", err);
        });
    },
    pull_self() {
      this.axios
        .post("/groups/pull_self", {
          group_id: this.selected_group_to_pull_yourself_from
        })
        .then(response => {
          console.log("Backend >> ", response.data);
          this.$store.dispatch("fetch_current_user");
        })
        .catch(err => {
          console.log("Error >> ", err);
        });
    },
    active_group_setter(group) {
      console.log("set active group", group)
      if (group != null) this.active_group = {...group}
      else this.active_group = null
    },
    pull_yourself_from(group_id) {
      console.log("pull yourself from", group_id, "...")
      this.axios
        .post("/groups/pull_self", {
          group_id: group_id
        })
        .then(response => {
          console.log("Backend (pull yourself from) >>", response.data);
          this.$store.dispatch("fetch_current_user");
        })
        .catch(err => {
          console.log("Error (pull yourself from) >>", err);
        });
    }
  }
};
</script>