<template>
  <b-modal
    v-if="want_login"
    id="login_modal"
    v-model="visible"
    okTitle="Accedi"
    ok-only
    @ok.prevent="attempt_login"
    @hide.prevent
  >
    <template v-slot:modal-header>
      <h5 class="modal-title">Accedi all'applicazione</h5>
    </template>
    <p>Per usare questa applicazione è necessario avere un <b>profilo</b>. È possibile aggiungere l'applicazione alla propria schermata del cellulare per rendere l'accesso più comodo.</p>

    <p>
      Per favore, inserisci i tuoi dati. Se non hai un profilo, vai alla pagina di
      <a
        href="#"
        @click.prevent="toggleForm"
      >registrazione</a>.
    </p>

    <b-input-group size="lg">
      <b-input-group-prepend is-text>
        <b-icon-envelope />
      </b-input-group-prepend>
      <b-form-input
        v-model="email"
        placeholder="Email address"
        autofocus
        @keyup.ctrl.insert="() => { email = 'user@example.com'; password = 'pass' ; attempt_login() ;}"
        @keyup.ctrl.alt.insert="() => { email = 'admin@example.com'; password = 'pass' ; attempt_login() ;}"
      ></b-form-input>
    </b-input-group>

    <b-input-group size="lg">
      <b-input-group-prepend is-text>
        <b-icon-lock />
      </b-input-group-prepend>
      <b-form-input
        v-model="password"
        placeholder="Password"
        type="password"
        @keyup.enter="attempt_login"
      ></b-form-input>
    </b-input-group>
  </b-modal>
  <b-modal
    v-else
    v-model="modalShow"
    id="signup_modal"
    @ok.prevent="attempt_signup"
    @cancel.prevent="toggleForm"
    okTitle="Registrami"
    cancelTitle="Annulla"
    @hide.prevent
  >
    <template v-slot:modal-header>
      <h5 class="modal-title">Crea un profilo</h5>
    </template>

    <b-alert
      v-if="alert_message"
      show
      dismissible
      variant="warning"
      @dismissed="dismiss_alert_message"
    >{{ alert_message }}</b-alert>

    <p>
      Se non hai ancora un profilo, inserisci qui i tuoi dati e potrai accedere. Se hai già un profilo, torna alla pagina di
      <a
        href="#"
        @click.prevent="toggleForm"
      >accesso</a>.
    </p>

    <b-input-group size="lg">
      <b-input-group-prepend is-text>
        <b-icon-envelope />
      </b-input-group-prepend>
      <b-form-input v-model="email" placeholder="Email address" autofocus></b-form-input>
    </b-input-group>

    <b-input-group size="lg">
      <b-input-group-prepend is-text>
        <b-icon-lock />
      </b-input-group-prepend>
      <b-form-input
        v-model="password"
        placeholder="Password"
        type="password"
        @keyup.enter="attempt_signup"
      ></b-form-input>
    </b-input-group>

    <b-input-group size="lg">
      <b-input-group-prepend is-text>
        <b-icon-shield-lock />
      </b-input-group-prepend>
      <b-form-input
        v-model="password_confirmation"
        placeholder="Conferma password"
        type="password"
        @keyup.enter="attempt_signup"
      ></b-form-input>
    </b-input-group>
  </b-modal>
</template>

<script>
export default {
  props: {},
  data: () => ({
    visible: true,
    want_login: true,
    email: null,
    password: null,
    password_confirmation: null
  }),
  computed: {},
  methods: {
    toggleForm() {
      this.want_login = !this.want_login;
    },
    attempt_login() {
      this.axios
        .post("/users/login", {
          email: this.$data.email,
          password: this.$data.password
        })
        .then(result => {
          console.log("Backend >> ", result.data);
          this.$session.set("authtoken", result.data.access_token);
          this.$store.dispatch("auth_refresh")
          this.$store.commit("page", "main")
        })
        .catch(err => {
          console.log("Error >> ", err);
          this.$store.commit("warning_alert", "Qualcosa è andato storto. Riprova ad accedere.")
        });
    },
    attempt_signup() {
      this.axios
        .post("/users/signup", {
          email: this.$data.email,
          password: this.$data.password,
          password_confirmation: this.$data.password_confirmation
        })
        .then(result => {
          console.log("Backend >> ", result.data);
          this.$store.commit("success_alert", "Utente creato con successo.")
          this.$session.set("authtoken", result.data.access_token);
          this.$store.dispatch("auth_refresh")
          this.$store.commit("page", "main")
        })
        .catch(err => {
          console.log("Error >> ", err);
          this.$store.commit("warning_alert", "Qualcosa è andato storto. Potrebbe essere che la mail è già in uso.")
        });
    },
  }
};
</script>

<style scoped>
</style>