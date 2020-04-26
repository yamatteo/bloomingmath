<template>
  <component :is="name" v-bind="args">
      <error />
  </component>
</template>

<script>
module.exports = {
  name: "meta-page",
  components: {
      "admin-externals": window.httpVueLoader("/js/components/pages/admin-externals.vue"),
      "admin-groups": window.httpVueLoader("/js/components/pages/admin-groups.vue"),
      "admin-nodes": window.httpVueLoader("/js/components/pages/admin-nodes.vue"),
      "admin-relevance": window.httpVueLoader("/js/components/pages/admin-relevance.vue"),
      "edit-group": window.httpVueLoader("/js/components/pages/edit-group.vue"),
      "error": window.httpVueLoader("/js/components/pages/error.vue"),
      "home": window.httpVueLoader("/js/components/pages/home.vue"),
      "login": window.httpVueLoader("/js/components/pages/login.vue"),
      "profile": window.httpVueLoader("/js/components/pages/profile.vue"),
      "reset": window.httpVueLoader("/js/components/pages/reset.vue"),
      "signup": window.httpVueLoader("/js/components/pages/signup.vue"),
  },
  props: {
    name: {
        type: String,
        default: "error"
    },
    args: {
      type: Object,
      default: () => {
        return new Object();
      }
    }
  }
};
</script>

<style scoped>
</style>