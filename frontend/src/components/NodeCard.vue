<template>
  <div class="card bg-light mb-3">
    <h5 class="card-header" href="#" @click.prevent="toggle">{{ node.short }}</h5>
    <div class="card-body" v-if="expand">
      <p v-if="node.long" class="card-text">{{ node.long }}</p>
      <ul v-if="node.contents.length" class="card-text">
        <b>Contenuti:</b>
        <li v-for="content in node.contents" :key="content.id">
          <a :href="'/contents/'+content.id">{{ content.short }}</a>
        </li>
      </ul>
      <p v-else class="card-text">Spiacenti, a quanto pare questo nodo non ha argomenti.</p>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    node: Object
  },
  data: () => ({
    expand: false
  }),
  computed: {},
  methods: {
    toggle() {
      this.expand = !this.expand;
    }
  }
};
</script>

<style scoped>
.card-header {
  cursor: pointer;
}
</style>