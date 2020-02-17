<template>
  <b-navbar toggleable="sm" type="dark" variant="dark" class="py-1">
    <b-navbar-brand href="#" @click.prevent="goto_null">Bloomingmath</b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <!-- <b-navbar-nav>
        <b-nav-item href="#">Link</b-nav-item>
        <b-nav-item href="#" disabled>Disabled</b-nav-item>
      </b-navbar-nav> -->

      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        <!-- <b-nav-form>
          <b-form-input size="sm" class="mr-sm-2" placeholder="Search"></b-form-input>
          <b-button size="sm" class="my-2 my-sm-0" type="submit">Search</b-button>
        </b-nav-form> -->

        <!-- <b-nav-item-dropdown text="Lang" right>
          <b-dropdown-item href="#">EN</b-dropdown-item>
          <b-dropdown-item href="#">ES</b-dropdown-item>
          <b-dropdown-item href="#">RU</b-dropdown-item>
          <b-dropdown-item href="#">FA</b-dropdown-item>
        </b-nav-item-dropdown> -->

        <!-- <b-nav-item-dropdown right>
          <template v-slot:button-content>
            <em>User</em>
          </template>
          <b-dropdown-item href="#">Profile</b-dropdown-item>
          <b-dropdown-item href="#">Sign Out</b-dropdown-item>
        </b-nav-item-dropdown> -->
        <b-button pill class="px-2 m-1" @click="goto_profile"><b-icon-person-fill font-scale="1.5"/></b-button>
        <b-button pill class="px-2 m-1" @click="logout"><b-icon-box-arrow-right font-scale="1.5"/></b-button>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<script>
export default {
  methods: {
    logout () {
      this.$session.destroy();
      this.$store.dispatch("login_actualization", null);
    },
    goto_profile () {
      this.$store.commit("see_page", 'profile')
    },
    goto_null() {
      this.$store.commit("see_page", null)
    }
  }
}
</script>

<style scoped>

</style>