<template>
  <div class="card bg-light mb-3">
    <h5 class="card-header" href="#" @click.prevent="toggle">{{ node.short }}</h5>
    <div class="card-body" v-if="expand">
      <p v-if="node.long" class="card-text" style="white-space: pre-line;">{{ node.long }}</p>
      <ul v-if="node.contents.length" class="card-text">
        <b>Contenuti:</b>
        <li v-for="content in node.contents" :key="content.id">
          <a :href="'/contents/'+content.id">{{ content.short }}</a>
        </li>
      </ul>
      <p v-else class="card-text">Spiacenti, a quanto pare questo argomento non ha contenuti.</p>
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