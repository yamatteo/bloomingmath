<template>
  <base-card title="I tuoi contenuti" forced collapsed>This not you see</base-card>
</template>

<script>
module.exports = {
  name: "error-card",
  components: {
    "base-card": window.httpVueLoader("/js/components/bases/base-card.vue")
  },
  props: {},
  data: () => ({
    nodes: null
  }),
  computed: {},
  methods: {},
  mounted() {
    if (!this.nodes) {
      console.log("Fetching nodes");

      axiosget("/nodes/current")
        .then(result => {
          console.log(result.data);

          this.nodes = result.data;
          for (node in this.nodes) {
            this.queuecard("node", node);
          }
        })
        .catch(err => {
          console.log("Error (fetching nodes) >>> ", err);
          this.nodes = [];
        });

      post("/users/current")
        .then(response => {
          console.log("current_user", response.data);
        })
        .catch(err => {
          console.log(err);
        });
    }
  }
};
</script>

<style scoped>
</style>