<template>
  <b-card header-tag="header">
    <template v-slot:header>
      <h6 class="mb-0">Gruppi di appartenenza</h6>
    </template>

    <div v-if="current_user.groups">
      Questi sono i gruppi di cui fai parte:
      <ul>
        <li v-for="group in current_user.groups" :key="group.id">{{ group.short }}</li>
      </ul>
    </div>
    <div v-else>Non fai parte di nessun gruppo.</div>

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

    <b-form-group v-if="current_user.groups.length" label="Esci da un gruppo" label-for="pull_self">
      <b-input-group>
      <b-form-select
        id="pull_self"
        v-model="selected_group_to_pull_yourself_from"
        :options="current_groups_options"
      ></b-form-select>
      <b-button @click="pull_self">Esci</b-button>
      </b-input-group>
    </b-form-group>
  </b-card>
</template>

<script>
export default {
  data: () => ({
    selected_group_to_push_yourself_into: null,
    selected_group_to_pull_yourself_from: null,
  }),
  computed: {
    current_user() {
      return this.$store.state.current_user;
    },
    groups() {
      return this.$store.state.groups;
    },
    available_groups () {
      console.log("current_user", this.current_user);
      
      const used_groups_ids = this.current_user.groups.map(group => group.id)
      console.log("used_groups_ids", used_groups_ids);
      
      return this.$store.state.groups.filter((group) => {
        if (used_groups_ids.includes(group.id)) {
          return false
        } else {
          return true
        }
      });
    },
    available_groups_options () {
      return this.available_groups.map((group) => ({
        value: group.id,
        text: group.short
      }))
    },
    current_groups_options () {
      return this.current_user.groups.map((group) => ({
        value: group.id,
        text: group.short
      }))
    },
  },
  methods: {
    push_self() {
      this.axios.post("/groups/push_self", {
        "group_id": this.selected_group_to_push_yourself_into
      }).then((response) => {
        console.log("Backend >> ", response.data);
        this.$store.dispatch("fetch_current_user")
        
      }).catch((err) => {
        console.log("Error >> ", err)
      })
    },
    pull_self() {
      console.log("TEMP", this.selected_group_to_pull_yourself_from);
      
      this.axios.post("/groups/pull_self", {
        "group_id": this.selected_group_to_pull_yourself_from
      }).then((response) => {
        console.log("Backend >> ", response.data);
        this.$store.dispatch("fetch_current_user")
        
      }).catch((err) => {
        console.log("Error >> ", err)
      })
    },
  }
};
</script>