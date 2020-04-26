<template>
  <base-card
    :title="title"
    collapsed
    :over-body="loading"
    @header_click="() => { if(!this.users) fetch() }"
  >
    <b-list-group flush>
      <b-list-group-item
        button
        v-for="user in users"
        :key="user.id"
        class="d-flex justify-content-between align-items-center"
      >
        {{ user.email }}
        <span>
          <base-badge></base-badge>
          <base-badge></base-badge>
        </span>
      </b-list-group-item>
      <b-list-group-item v-if="!noAdd" button variant="secondary">Aggiungi uno</b-list-group-item>
    </b-list-group>
  </base-card>
</template>

<script>
module.exports = {
  name: "users-card",
  components: {
    "base-card": window.httpVueLoader("/js/components/bases/base-card.vue"),
    "base-badge": window.httpVueLoader("/js/components/bases/base-badge.vue")
  },
  props: {
    title: {
      type: String,
      default: "Utenti"
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
    users: null,
    loading: false
  }),
  computed: {},
  methods: {
    // edit(id) {
    //   this.pushcard("edit-group", { id: id, callback: this.fetch.bind(this) });
    // },
    // add() {
    //   post("/groups/add", {
    //     short: "new group's name"
    //   })
    //     .then(result => {
    //       this.fetch();
    //     })
    //     .catch(error => {
    //       console.log("POST /groups/add", error);
    //     });
    // },
    fetch() {
      this.loading = true;
      console.log("...fetching", this.find);

      post("/users/browse", this.find)
        .then(result => {
          this.users = result.data;
        })
        .catch(error => {
          console.log("POST /users/browse", error);
          this.users = [];
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