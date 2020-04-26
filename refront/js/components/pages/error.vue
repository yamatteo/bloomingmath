<template>
  <b-container class="mt-3">
    <b-row>
      <b-col>
        <base-card title="C'è stato un errore">
          <div v-if="message">
            <p>L'applicazione ha segnalato il seguente messaggio.</p>
            <pre>{{ message }}</pre>
          </div>
          <div v-else>
            <p>Non è possibile stabilire al momento la causa dell'errore, ma qualcosa è andato storto.</p>
            <p>Prova a terminare la sessione (logout), ricaricare la pagina e compiere di nuovo la stessa azione.</p>
            <p>Se il problema persiste, contattare l'amministratore.</p>
          </div>
        </base-card>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
module.exports = {
  name: "error-page",
  components: {
    "base-card": window.httpVueLoader("/js/components/bases/base-card.vue")
  },
  props: {
    message: {
      type: String,
      default: null
    }
  }
};
</script>

<style scoped>
</style>