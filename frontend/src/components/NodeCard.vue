<template>
  <div class="card bg-light mb-3">
    <ContentModal v-if="show_modal" :content="active_content" :active_content_setter="active_content_setter"/>
    <h5 class="card-header" href="#" @click.prevent="toggle">{{ node.short }}</h5>
    <div class="card-body" v-if="expand">
      <p v-if="node.long" class="card-text" style="white-space: pre-line;">{{ node.long }}</p>

      <ul v-if="node.contents.length" class="list-group list-group-flush">
        <b>Contenuti:</b>
        <ContentLgi v-for="content in node.contents" :key="content.id" :content="content" :active_content_setter="active_content_setter"/>
      </ul>
      <p v-else class="card-text">Spiacenti, a quanto pare questo argomento non ha contenuti.</p>
    </div>
  </div>
</template>

<script>
export default {
  components: {
    ContentLgi: () => import("@/components/ContentLgi"),
    ContentModal: () => import("@/components/ContentModal")
  },
  props: {
    node: Object
  },
  data: () => ({
    expand: false,
    active_content: null
  }),
  computed: {
    show_modal() {
      if (this.active_content==null) {
        return false
      } else {
        return true
      }
    }
  },
  methods: {
    toggle() {
      this.expand = !this.expand;
    },
    active_content_setter(content) {
      console.log("set active content", content)
      if (content != null) this.active_content = {...content}
      else this.active_content = null
    }
  }
};
</script>

<style scoped>
.card-header {
  cursor: pointer;
}

.list-group-item {
  background: #f8f9fa;
}
</style>