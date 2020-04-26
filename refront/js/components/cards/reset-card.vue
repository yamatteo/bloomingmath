<template>
  <base-card title="Recupera l'accesso" forced :over_body="attempting">
    <div>
      <p>
        Se non hai un profilo, vai alla pagina di
        <a href="#" @click.prevent="() => goto('signup')">registrazione</a>.
      </p>
      <p>
        Prima di reimpostare la password prova ad accedere normalmente con la pagina di
        <a href="#" @click.prevent="() => goto('login')">accesso</a> facendo attenzione alle maiuscole e ad altri possibili errori di battitura.
      </p>

      <p>Se non riesci ad accedere al tuo profilo, puoi reimpostare la password. Inserisci il tuo indirizzo email. Ti verrà inviato un codice con il quale puoi reimpostare la password.</p>
    </div>

    <div v-if="!code_sent">
      <base-input v-model="email" icon="envelope" placeholder="Email"></base-input>
      <base-button @click="send_code">Invia codice</base-button>
    </div>
    <div v-else>
      <b-alert show>Il codice è stato inviato</b-alert>
      <base-input v-model="reset_code" icon="key" placeholder="Codice"></base-input>
      <base-input v-model="password" icon="lock" placeholder="Password" type="password"></base-input>
      <base-input
        v-model="password_confirmation"
        icon="check"
        placeholder="Password (conferma)"
        type="password"
      ></base-input>
      <base-button @click="attempt_reset">Reimposta password</base-button>
    </div>

    <p class="my-3">
      Non riesci ad accedere al tuo profilo? Puoi
      <a
        href="#"
        @click.prevent="() => goto('reset')"
      >reimpostare la password</a>.
    </p>
  </base-card>
</template>

<script>
module.exports = {
  name: "reset-card",
  components: {
    "base-button": window.httpVueLoader("/js/components/bases/base-button.vue"),
    "base-card": window.httpVueLoader("/js/components/bases/base-card.vue"),
    "base-input": window.httpVueLoader("/js/components/bases/base-input.vue")
  },
  props: {},
  data: () => ({
    email: null,
    password: null,
    password_confirmation: null,
    reset_code: null,
    code_sent: false,
    attempting: false
  }),
  computed: {},
  methods: {
    send_code() {
      this.code_sent = true;
      post("/users/password_reset_request", { email: this.$data.email })
        .then(result => {
          console.log("Backend (code request) >>", result.data);
        })
        .catch(err => {
          console.log("Error (code request)", err);
        });
    },
    attempt_reset() {
      this.attempting = true;
      post("/users/password_reset", {
        email: this.$data.email,
        token: this.$data.reset_code,
        password: this.$data.password,
        password_confirmation: this.$data.password_confirmation
      })
        .then(result => {
          console.log("Backend (reset request) >>", result.data);
          this.goto("login");
          this.pushcard("message", {
            message:
              "La password è stata reimpostata. Prova ad effettuare l'accesso.",
            variant: "success"
          });
        })
        .catch(err => {
          console.log("Error (reset request)", err);
          this.pushcard("message", {
            message:
              "Non ha funzionato. Controlla di aver scritto giusto il codice e che le due password coincidano. Se non hai mai usato questa applicazione, devi creare un account nella pagina di registrazione. Se il problema persiste contatta l'amministratore del sito.",
            variant: "warning"
          });
        })
        .then(() => {
          this.attempting = false;
        });
    }
  }
};
</script>

<style scoped>
</style>