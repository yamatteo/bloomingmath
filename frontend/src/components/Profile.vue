<template>
  <div>
    <Navbar />
    <b-container>
      <b-row>
        <b-col></b-col>
        <b-col cols="12" sm="10" md="8">
          <h1>Profilo</h1>
          <ProfileUserCard />
          <ProfileGroupsCard />
        </b-col>
        <b-col></b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
export default {
  props: {},
  components: {
    Navbar: () => import("@/components/Navbar"),
    ProfileUserCard: () => import("@/components/ProfileUserCard.vue"),
    ProfileGroupsCard: () => import("@/components/ProfileGroupsCard.vue"),
  }
};
</script>

<style scoped>
.container {
  margin-top: 50px;
}
</style>