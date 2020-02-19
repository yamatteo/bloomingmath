<template>
  <div>
    <Navbar />
    <b-container>
      <b-row>
        <b-col></b-col>
        <b-col cols="12" sm="10" md="8">
          <h1>I tuoi contenuti</h1>
          <div v-if="nodes.length">
            <NodeCard v-for="node in nodes" :key="node.id" :node="node" />
          </div>
          <div v-else>
            <p>Non hai nessun argomento disponibile. Prova ad entrare nel tuo profilo e selezionare alcuni gruppi di cui far parte.</p>
          </div>
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
    NodeCard: () => import("@/components/NodeCard")
  },
  computed: {
    nodes() {
      if (this.$store.state.current_user)
        return this.$store.state.current_user.nodes;
      else return [];
    }
  }
};
</script>

<style scoped>
.container {
  margin-top: 50px;
}
</style>