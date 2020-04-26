<template>
  <base-card
    title="Gruppi"
    collapsed
    :over-body="loading"
    @header_click="() => { if(!this.groups) fetch() }"
  >
    <b-list-group flush>
      <b-list-group-item
        button
        v-for="group in groups"
        :key="group.id"
        class="d-flex justify-content-between align-items-center"
      >
        {{ group.short }}
        <span>
        <base-badge pill>
        </base-badge>
        <base-badge pill icon="edit" @click="edit(group.id)">
        </base-badge>
        </span>
      </b-list-group-item>
      <b-list-group-item button variant="secondary" @click="add">Aggiungi uno</b-list-group-item>
    </b-list-group>
  </base-card>
</template>

<script>
module.exports = {
  name: "groups-card",
  components: {
    "base-card": window.httpVueLoader("/js/components/bases/base-card.vue"),
    "base-badge": window.httpVueLoader("/js/components/bases/base-badge.vue")
  },
  props: {},
  data: () => ({
    groups: null,
    loading: false
  }),
  computed: {},
  methods: {
    edit(id) {
        this.pushcard('edit-group', {id: id, callback: this.fetch.bind(this)})
    },
    add() {
      post("/groups/add", {
        short: "new group's name"
      })
        .then(result => {
          this.fetch();
        })
        .catch(error => {
          console.log("POST /groups/add", error);
        });
    },
    fetch() {
      this.loading = true;
      console.log("...fetching");

      post("/groups/browse")
        .then(result => {
          this.groups = result.data;
        })
        .catch(error => {
          console.log("POST /groups/browse", error);
          this.groups = [];
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