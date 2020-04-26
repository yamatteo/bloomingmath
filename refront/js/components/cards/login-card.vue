<template>
  <base-card title="Accedi" forced :over_body="attempting">
    <div>
      <p>
        Per usare questa applicazione è necessario avere un
        <b>profilo</b>.
      </p>
      <p>
        Per favore, inserisci i tuoi dati. Se non hai un profilo, vai alla pagina di
        <a
          href="#"
          @click.prevent="() => goto('signup')"
        >registrazione</a>.
      </p>
    </div>

    <base-input v-model="email" icon="envelope" placeholder="Email"></base-input>
    <base-input
      v-model="password"
      icon="lock"
      placeholder="Password"
      type="password"
      @keyup.enter="attempt_login"
    ></base-input>
    <base-button @click="attempt_login">Accedi</base-button>

    <p class="my-3">
      Non riesci ad accedere al tuo profilo? Puoi
      <a href="#" @click.prevent="() => goto('reset')">reimpostare la password</a>.
    </p>
  </base-card>
</template>

<script>
module.exports = {
  name: "login-card",
  components: {
    "base-button": window.httpVueLoader("/js/components/bases/base-button.vue"),
    "base-card": window.httpVueLoader("/js/components/bases/base-card.vue"),
    "base-input": window.httpVueLoader("/js/components/bases/base-input.vue"),
  },
  props: {},
  data: () => ({
    email: null,
    password: null,
    attempting: false
  }),
  computed: {},
  methods: {
    attempt_login() {
      this.attempting = true;
      post("/users/login", {
        email: this.$data.email,
        password: this.$data.password
      })
        .then(result => {
          console.log("Backend >> ", result.data);
          store.dispatch("update_authtoken", result.data.access_token);
          this.goto("main");
          this.pushcard("message", {
            message: "Accesso effettuato con successo",
            variant: "success"
          });
        })
        .catch(err => {
          console.log("Error >> ", err);
          store.dispatch("update_authtoken", null);
          this.pushcard("message", {
            message:
              "Le credenziali non sono riconoscibili. Controlla di aver scritto bene l'indirizzo mail e la password. Se non hai mai usato questa applicazione devi creare un profilo.",
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