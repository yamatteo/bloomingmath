<template>
  <error-card v-if="!card.name"></error-card>
  <edit-group-card v-else-if="card.name == 'edit-group'" :id="card.id" :callback="card.callback"></edit-group-card>
  <edit-node-card v-else-if="card.name == 'edit-node'" :id="card.id" :callback="card.callback"></edit-node-card>
  <groups-card v-else-if="card.name == 'groups'"></groups-card>
  <login-card v-else-if="card.name == 'login'"></login-card>
  <main-card v-else-if="card.name == 'main'"></main-card>
  <message-card v-else-if="card.name == 'message'" :variant="card.variant">
    {{ card.message }}
  </message-card>
  <nodes-card v-else-if="card.name == 'nodes'"></nodes-card>
  <reset-card v-else-if="card.name == 'reset'"></reset-card>
  <signup-card v-else-if="card.name == 'signup'"></signup-card>
  <users-card v-else-if="card.name == 'users'"></users-card>
  <error-card v-else></error-card>
</template>

<script>
module.exports = {
  name: "card-gen",
  props: ["card"],
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