<template>
  <b-alert :variant="variant" show dismissible>
    <slot>{{ message }}</slot>
  </b-alert>
</template>

<script>
module.exports = {
  name: "message-card",
  components: {},
  props: {
    card_data: {
      type: Object,
      default: () => ({
        message: "Qualcosa è andato storto.",
        variant: "primary"
      })
    }
  },
  data() {
    return {
      message: this.card_data.message,
      variant: this.card_data.variant
    };
  },
  computed: {},
  methods: {}
};
</script>

<style scoped>
</style>