<template>
  <div>
    <LoginModal v-if="!authorized && see_login_modal"/>
    <SignupModal v-if="!authorized && see_signup_modal" />
    <Landing v-if="authorized && (see_page=='landing' | see_page == null)" />
    <Profile v-if="authorized && see_page=='profile'" />
  </div>
</template>

<script>
export default {
  components: {
    Landing: () => import("@/components/Landing.vue"),
    Profile: () => import("@/components/Profile.vue"),
    LoginModal: () => import("@/components/LoginModal.vue"),
    SignupModal: () => import("@/components/SignupModal.vue")
  },
  props: {},
  data: () => ({}),
  computed: {
    authorized() {
      return this.$store.state.authtoken != null;
    },
    see_login_modal() {
      return this.$store.state.modal == 'login' | this.$store.state.modal == null
    },
    see_signup_modal() {
      return this.$store.state.modal == 'signup'
    },
    see_page() {
      return this.$store.state.see_page
    }
  },
  mounted () {
    this.$store.dispatch("login_actualization", this.$session.get("authtoken", null))
  }
};
</script>

<style>
.container {
  margin-top: 50px;
}
</style>