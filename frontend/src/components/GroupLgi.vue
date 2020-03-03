<template>
  <a
    class="list-group-item list-group-item-action d-flex justify-content-between align-items-center"
  >
    {{ group.short }}
    <span>
      <LgiButton :click_handler="() => pull_yourself_from(group.id)" icon="x" />
      <LgiButton v-if="is_admin" :click_handler="edit" icon="pencil" />
    </span>
  </a>
</template>

<script>
export default {
  components: {
    LgiButton: () => import("@/components/LgiButton")
  },
  props: {
    group: Object,
    active_group_setter: Function,
    pull_yourself_from: Function
  },
  data: () => ({}),
  computed: {
    is_admin() {
      try {
        return this.$store.state.current_user.is_admin;
      } catch {
        return false;
      }
    }
  },
  methods: {
    edit() {
      this.axios
        .post("/groups/read", {
          find: { id: this.group.id },
          with_nodes: true,
          with_other_nodes: true
        })
        .then(response => {
          this.$store.commit("active_modal", {
            name: "GroupEditModal",
            props: { group: response.data }
          });
        }).catch((err) => {
          console.log("Error (edit group) >>", err);
          
        });
    }
  }
};
</script>

<style scoped>
.badge {
  cursor: pointer;
}
</style>