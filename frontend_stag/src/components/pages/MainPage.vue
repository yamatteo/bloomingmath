<template>
  <BasePage title="I tuoi contenuti">
    <BaseCard v-for="node in nodes" :key="node.id" :title="node.short" collapsed>
      <p>{{ node.long }}</p>
      <BaseListGroup>
        <BaseListGroupItem v-for="content in node.contents" :key="content.id" :onClick="reader(content.id)">
          {{ content.short }}
          <!-- <template v-slot:pills>
            <BasePill icon="thumbs-up" :onClick="() => push_yourself_from(group.id)"></BasePill>
          </template> -->
        </BaseListGroupItem>

        <template v-slot:empty>
          <BaseListGroupItem disabled>Non ci sono contenuti per questo argomento.</BaseListGroupItem>
        </template>
      </BaseListGroup>
    </BaseCard>

      <template v-slot:empty>
        <p>Non hai nessun argomento disponibile. Prova ad entrare nel tuo profilo e selezionare alcuni gruppi di cui far parte.</p>
      </template>
  </BasePage>
</template>

<script>
export default {
  name: "MainPage",
  computed: {
    nodes() {
      if (this.$store.state.current_user)
        return this.$store.state.current_user.nodes;
      else return [];
    }
  },
  methods: {
    reader(id) {
      return () => {
        console.log("read!");
        window.open(`/contents/download/${id}`, '_blank');
      }
    }
  }
};
</script>

<style scoped>
</style>