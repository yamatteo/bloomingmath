<template>
  <component v-bind:is="computedComponent" :card_data="computedData"></component>
</template>

<script>
module.exports = {
  name: "card-gen",
  props: {
    card: {
      type: Object,
      default: () => ({name: "error", data: {}})
    },
  },
  computed: {
    computedComponent() {
      try {
        return `${this.$props.card.name}-card`
      } catch {
        return "error-card"
      }
    },
    computedData() {
      try {
        return this.$props.card.data
      } catch {
        return new Object;
      }
    }
  },
  components: {
    "edit-group-card": window.httpVueLoader("/js/components/cards/edit-group-card.vue"),
    "edit-node-card": window.httpVueLoader("/js/components/cards/edit-node-card.vue"),
    "error-card": window.httpVueLoader("/js/components/cards/ErrorCard.vue"),
    "groups-card": window.httpVueLoader("/js/components/cards/groups-card.vue"),
    "login-card": window.httpVueLoader("/js/components/cards/login-card.vue"),
    "main-card": window.httpVueLoader("/js/components/cards/main-card.vue"),
    "message-card": window.httpVueLoader("/js/components/cards/message-card.vue"),
    "nodes-card": window.httpVueLoader("/js/components/cards/nodes-card.vue"),
    "reset-card": window.httpVueLoader("/js/components/cards/reset-card.vue"),
    "signup-card": window.httpVueLoader("/js/components/cards/signup-card.vue"),
    "users-card": window.httpVueLoader("/js/components/cards/users-card.vue"),
  }
};
</script>

<style scoped>
</style>