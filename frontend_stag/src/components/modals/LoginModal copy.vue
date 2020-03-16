<template>
  <b-modal
    v-if="mask == 'login'"
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
        @click.prevent="() => wear('signup')"
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

    <b-alert v-if="wrong_credentials" variant="warning" class="mt-2" show dismissible>
      <b>Le credenziali inserite non sono riconosciute.</b><br />
      Hai scritto bene l'indirizzo mail?<br />
      <a href="#" @click.prevent="() => wear('reset')">Hai dimenticato la password?</a>
    </b-alert>
  </b-modal>



  <b-modal
    v-else-if="mask == 'signup'"
    v-model="visible"
    id="signup_modal"
    @ok.prevent="attempt_signup"
    @cancel.prevent="() => wear('login')"
    okTitle="Registrami"
    cancelTitle="Annulla"
    @hide.prevent
  >
    <template v-slot:modal-header>
      <h5 class="modal-title">Crea un profilo</h5>
    </template>

    <p>
      Se non hai ancora un profilo, inserisci qui i tuoi dati e potrai accedere. Se hai già un profilo, torna alla pagina di
      <a
        href="#"
        @click.prevent="() => wear('login')"
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



  <b-modal
    v-else-if="mask == 'reset'"
    v-model="visible"
    id="reset_modal"
    @ok.prevent="attempt_reset"
    @cancel.prevent="() => wear('login')"
    okTitle="Reset"
    cancelTitle="Annulla"
    @hide.prevent
  >
    <template v-slot:modal-header>
      <h5 class="modal-title">Richiedi nuova password</h5>
    </template>

    <p>
      Se vuoi reimpostare la password devi inserire anche il codice che di verrà inviato per mail.
      Questo codice serve ad essere sicuri che è proprio il proprietario della mail a richiedere la nuova password.
      Se non vuoi cambiare password, torna alla pagina di 
      <a
        href="#"
        @click.prevent="() => wear('login')"
      >accesso</a>.
    </p>

    <p>
      Per cambiare password, inserisci la tua mail e poi premi su "Invia codice".
      Dopo qualche minuto arriverà una mail al tuo indirizzo. Copia il codice e inseriscilo qui sotto assieme alla nuova password.
    </p>

    <b-input-group size="lg">
      <b-input-group-prepend is-text>
        <b-icon-envelope />
      </b-input-group-prepend>
      <b-form-input v-model="email" placeholder="Email address" autofocus></b-form-input>
    </b-input-group>

    <b-button>Invia cofice</b-button>

    <b-input-group size="lg">
      <b-input-group-prepend is-text>
        <font-awesome-icon icon="key"></font-awesome-icon>
      </b-input-group-prepend>
      <b-form-input
        v-model="reset_code"
        placeholder="Codice reimpostazione"
        type="text"
        @keyup.enter="attempt_reset"
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
        @keyup.enter="attempt_reset"
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
        @keyup.enter="attempt_reset"
      ></b-form-input>
    </b-input-group>
  </b-modal>
</template>

<script>
export default {
  props: {},
  data: () => ({
    visible: true,
    mask: 'login',
    email: null,
    password: null,
    password_confirmation: null,
    reset_code: null,
    wrong_credentials: false
  }),
  computed: {},
  methods: {
    wear(mask) {
      this.mask = mask;
      this.password = null;
      this.password_confirmation = null;
      this.reset_code = null;
      this.wrong_credentials = null;
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
          this.wrong_credentials = true;
          // this.$store.commit("warning_alert", "Qualcosa è andato storto. Riprova ad accedere.")
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
    attempt_reset() {
    },
  }
};
</script>

<style scoped>
</style>