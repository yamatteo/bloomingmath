<template>
  <div id="app">
    <ModalLayer></ModalLayer>
    <Navbar :brandClick="goto('main')">
      <template v-slot:brand>Bloomingmath</template>

      <NavbarPill v-if="logged" icon="user" text="Profilo" :onClick="goto('profile')"></NavbarPill>
      <NavbarPill v-if="logged" icon="power-off" text="Esci" :onClick="logout"></NavbarPill>
    </Navbar>

    <MainPage v-if="page == 'main'"></MainPage>
    <ProfilePage v-else-if="page == 'profile'"></ProfilePage>
    <NotThisPage v-else></NotThisPage>
  </div>
</template>

<script>
export default {
  name: "App",
  components: {
    ModalLayer: () => import("@/components/ModalLayer"),
    Navbar: () => import("@/components/BaseNavbar"),
    NavbarPill: () => import("@/components/BaseNavbarPill"),

    MainPage: () => import("@/components/pages/MainPage"),
    ProfilePage: () => import("@/components/pages/ProfilePage"),
    NotThisPage: () => import("@/components/pages/NotThisPage"),
  },
  computed: {
    logged() {
      return this.$store.state.authtoken != null
    },
    page() {
      return this.$store.state.page
    }
  },
  methods: {
    logout() {
      this.$session.destroy();
      this.$store.dispatch("auth_refresh");
    },
    goto(page_name) {
      return () => {
        this.$store.commit("page", page_name)
      }
    }
  },
  mounted () {
    this.$store.dispatch("auth_refresh");
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
  color: #334;
}
</style>
