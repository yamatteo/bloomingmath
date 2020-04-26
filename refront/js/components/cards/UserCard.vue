<template>
  <base-card title="Profilo" :show="showing" :on-header-click="head_click">
  <div v-if="user_data">
    You are {{ user_data.email }}
  </div>
  <div v-else>
    <b-spinner label="Spinning"></b-spinner>
  </div>
  </base-card>
</template>

<script>
module.exports = {
  name: "user-card",
  components: {
    "base-card": window.httpVueLoader("/js/components/bases/BaseCard.vue")
  },
  props: {},
  data: () => ({
    user_data: null,
    opened: false,
    showing: false,
  }),
  computed: {},
  watch: {
    opened: function () {
      console.log("Opening");
      
      post("/users/current").then(res => {
        this.user_data = res.data
      }).catch(err => console.log(err))
    }
  },
  methods: {
    head_click() {
      this.opened = true;
      this.showing = !this.showing;
    }
  },
};
</script>

<style scoped>
</style>