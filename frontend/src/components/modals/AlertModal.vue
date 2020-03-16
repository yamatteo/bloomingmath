<template>
  <b-modal id="alert_modal" title="Guacamole!" :header-bg-variant="variant" ok-only ok-variant="secondary" @hide="delete_alert" v-model="visible">
    <p>{{ message }}</p>
  </b-modal>
</template>

<script>
export default {
  props: {},
  data: () => ({
    visible: true
  }),
  computed: {
    message() {
      return this.$store.state.alert.message
    },
    variant() {
      return this.$store.state.alert.variant
    }
  },
  methods: {
    delete_alert() {
      this.$store.commit("no_alert")
    }
  }
};
</script>

<style scoped>
</style>