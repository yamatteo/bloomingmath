<template>
  <base-card title="Errore">
  <h3>C'è qualcosa che non va.</h3>
  </base-card>
</template>

<script>
module.exports = {
  name: "error-card",
  components: {
    "base-card": window.httpVueLoader("/js/components/bases/BaseCard.vue")
  },
  props: {},
  data: () => ({}),
  computed: {},
  methods: {},
};
</script>

<style scoped>
</style>