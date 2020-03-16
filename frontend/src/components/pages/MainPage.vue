<template>
  <BasePage title="I tuoi contenuti">
    <b-alert variant="warning" show>
      <h4>Situazione temporanea</h4>
      <p>
        Cari studenti,
        <br />come forse potevamo immaginare, il virus ci ha recluso nelle nostre case.
        Ci siamo fatti prendere un po' alla sprovvista, ma la sorpresa è un sentimento che dura poco.
      </p>
      <p>
        Vi chiedo prima di tutto di poter essere in contatto con voi. Vorrei che almeno una persona per gruppo
        (Primo Viña, Primo Valparaíso, Secondo Economico, Secondo Scientifico, Terzo Economico,
        Terzo Scientifico e Quarto Scientifico) mi mandasse una mail
        a mbortolotto
        <font-awesome-icon icon="at"></font-awesome-icon>scuolaitalianavalpo.cl
        <br />A queste persone manderò poi indicazioni per il resto del gruppo.
      </p>
      <hr />
      <p>Non fatevi prendere dal panico. Sapevamo che il virus sarebbe arrivato. Sappiamo anche come farlo andar via.</p>
    </b-alert>

    <BaseCard v-for="node in nodes" :key="node.id" :title="node.short" collapsed>
      <p>{{ node.long }}</p>
      <BaseListGroup>
        <BaseListGroupItem
          v-for="content in node.contents"
          :key="content.id"
          :onClick="reader(content.id)"
        >
          {{ content.short }}
          <!-- <template v-slot:pills>
            <BasePill icon="thumbs-up" :onClick="() => push_yourself_from(group.id)"></BasePill>
          </template>-->
        </BaseListGroupItem>

        <BaseListGroupItem
          v-for="external_content in node.external_contents"
          :key="external_content.id"
          :onClick="external_reader(external_content.url)"
        >
          {{ external_content.short }}
          <template v-slot:pills>
            <BasePill
              v-if="current_user.is_admin"
              icon="edit"
              :onClick="goto('external_content_edit', {external_content_id: external_content.id})"
            ></BasePill>
          </template>
        </BaseListGroupItem>

        <template v-slot:empty>
          <BaseListGroupItem disabled>Non ci sono contenuti per questo argomento.</BaseListGroupItem>
        </template>
        <BaseListGroupItem v-if="current_user.is_admin" :onClick="add_external_content(node.id)">
          <BasePill nostop icon="plus"></BasePill>Aggiungi un contenuto esterno
        </BaseListGroupItem>
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
    current_user() {
      return this.$store.state.current_user;
    },
    nodes() {
      if (this.$store.state.current_user)
        return this.$store.state.current_user.nodes;
      else return [];
    }
  },
  methods: {
    reader(id) {
      return () => {
        window.open(`/contents/download/${id}`, "_blank");
      };
    },
    external_reader(url) {
      return () => {
        window.open(url, "_blank");
      };
    },
    goto(page_name, data) {
      return () => {
        this.$store.commit("page", { name: page_name, ...data });
      };
    },
    add_external_content(node_id) {
      return () => {
        this.$axios
          .post("/external_contents/add", {
            short: "content's short",
            url: "content's url"
          })
          .then(result => {
            let new_content = result.data;
            console.log(new_content, node_id);
            this.$axios
              .post("/nodes/push_external_content", {
                node_id: node_id,
                external_content_id: new_content.id
              })
              .then(result => {
                console.log(result.data);
                this.$store.dispatch("fetch_cu");
              })
              .catch(err => {
                console.log("Error (push external content) >>> ", err);
                this.$store.commit(
                  "warning_alert",
                  "Qualcosa è andato storto."
                );
              });
          })
          .catch(err => {
            console.log("Error (add external_content) >>> ", err);
            this.$store.commit("warning_alert", "Qualcosa è andato storto.");
          });
      };
    }
  },
  mounted() {
    this.$store.dispatch("fetch_cu")
  }
};
</script>

<style scoped>
</style>