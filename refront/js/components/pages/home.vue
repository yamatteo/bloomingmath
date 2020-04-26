<template>
  <b-container class="my-4">
    <b-row class="mb-3">
      <b-col>
        <h2>I tuoi contenuti</h2>
      </b-col>
    </b-row>
    <b-row v-for="node in nodes" :key="node.id">
      <b-col>
        <base-card :title="node.short" collapsed>
          <div v-if="node.long">{{ node.long }}</div>
          <b-list-group flush>
            <b-list-group-item
              button
              v-for="(external, index) in node.externals"
              :key="node.id + 'external' + index"
              class="d-flex justify-content-between align-items-center"
              @click="external_reader(external.url)"
            >{{ external.short }}</b-list-group-item>
          </b-list-group>
        </base-card>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
module.exports = {
  name: "home-page",
  components: {
    "base-card": window.httpVueLoader("/js/components/bases/base-card.vue")
  },
  props: {
    message: {
      type: String,
      default: null
    }
  },
  computed: {
    nodes() {
      return store.state.current_user.nodes;
    }
  },
  methods: {
    external_reader(url) {
      window.open(url, "_blank");
    }
  },
  mounted() {
    get("/users/current")
      .then(result => {
        store.commit("current_user", result.data);
      })
      .catch(error => {
        store.commit("authtoken", null);
        store.commit("current_user", null);
      });
  }
};
</script>

<style scoped>
</style>