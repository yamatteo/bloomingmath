<template>
  <div>
    <base-navbar :brand-click="() => {}">
      <template v-slot:brand>Bloomingmath</template>

      <b-dropdown no-caret toggle-class="rounded-pill" v-if="is_admin" class="px-2 m-1">
        <template v-slot:button-content>
          <i class="fas fa-tools mx-1"></i>
        </template>
        <b-dropdown-item @click="() => goto('admin-externals')">Externals</b-dropdown-item>
        <b-dropdown-item @click="() => goto('admin-groups')">Groups</b-dropdown-item>
        <b-dropdown-item @click="() => goto('admin-nodes')">Nodes</b-dropdown-item>
        <b-dropdown-divider></b-dropdown-divider>
        <b-dropdown-item @click="() => goto('admin-relevance')">Relevance</b-dropdown-item>
      </b-dropdown>

      <base-navbar-pill
        v-if="is_logged"
        icon="home"
        text="Contenuti"
        :on-click="() => goto('home')"
      ></base-navbar-pill>
      <base-navbar-pill
        v-if="is_logged"
        icon="user"
        text="Profilo"
        :on-click="() => goto('profile')"
      ></base-navbar-pill>
      <base-navbar-pill v-if="is_logged" icon="power-off" text="Esci" :on-click="logout"></base-navbar-pill>
    </base-navbar>
    <b-container class="mt-3">
      <b-row v-for="(alert, index) in alerts" :key="index">
        <b-col>
          <b-alert v-bind="alert">{{ alert.message }}</b-alert>
        </b-col>
      </b-row>
    </b-container>
    <page :name="page.name" :args="page.args" />
    <!-- <b-container class="mt-3">
      <b-row v-for="card in cards" :key="card.name">
        <b-col>
          <card-gen :card="card"></card-gen>
        </b-col>
      </b-row>
      <b-row v-if="!cards.length">
        <b-col>
          <card-gen :card="{name: 'main', data: {}}"></card-gen>
        </b-col>
      </b-row>
    </b-container>-->
    <meta-functional-component tag="base-input" :args="{show: true}" />
  </div>
</template>

<script>
module.exports = {
  name: "Bloomingmath",
  components: {
    "base-navbar-pill": window.httpVueLoader(
      "/js/components/bases/BaseNavbarPill.vue"
    ),
    "base-navbar": window.httpVueLoader("/js/components/bases/BaseNavbar.vue"),
    "card-gen": window.httpVueLoader("/js/components/cards/card-gen.vue"),
    "meta-functional-component": window.httpVueLoader(
      "/js/components/meta-functional-component.vue"
    ),
    page: window.httpVueLoader("/js/components/pages/meta.vue")
  },
  data: () => ({
    loggedAdmin: false
  }),
  computed: {
    cards() {
      return store.state.cards;
    },
    is_logged() {
      if (store.state.authtoken) {
        return true;
      } else {
        return false;
      }
    },
    is_admin() {
      try {
        return store.state.current_user.is_admin;
      } catch {
        return false;
      }
    },
    page() {
      let state_page = store.state.page;
      if (this.is_logged) {
        return state_page;
      } else {
        try {
          if (state_page.name.match(/^(login|signup|reset)$/)) {
            return state_page;
          } else {
            return { name: "login" };
          }
        } catch {
          return { name: "login" };
        }
      }
    },
    alerts() {
      return store.state.alerts;
    }
  },
  methods: {
    logout() {
      store.commit("authtoken", null);
      this.goto("login");
    }
  },
  mounted() {
    store
      .dispatch("update_authtoken", localStorage.getItem("authtoken", null))
      .then(() => {
        this.goto("home");
      })
      .catch(() => {
        store
          .dispatch(
            "update_authtoken",
            new URLSearchParams(location.search).get("authtoken", null)
          )
          .then(() => {
            this.goto("home");
          })
          .catch(() => {
            this.goto("login");
          });
      });
    // storage_value = localStorage.getItem("authtoken", null);
    // query_value = new URLSearchParams(location.search).get("authtoken", null);
    // if (query_value != null) {
    //   store.commit("authtoken", query_value);
    //   this.goto("main");
    // } else if (storage_value != null) {
    //   store.commit("authtoken", storage_value);
    //   this.goto("main");
    // } else {
    //   this.goto("login");
    // }
  }
};
</script>

<style scoped>
</style>