<template>
  <b-modal
    v-model="visible"
    :ok-only="okOnly"
    :okTitle="okTitle"
    cancelTitle="Annulla"
    @ok.prevent="eventOk"
    @cancel.prevent="() => wear('login')"
    @hide.prevent
  >
    <template v-slot:modal-header>
      <h5 class="modal-title">{{ modalTitle }}</h5>
    </template>

    <div v-if="mask == 'login'">
      <p>
        Per usare questa applicazione è necessario avere un
        <b>profilo</b>. È possibile aggiungere l'applicazione alla propria schermata del cellulare per rendere l'accesso più comodo.
      </p>
      <p>
        Per favore, inserisci i tuoi dati. Se non hai un profilo, vai alla pagina di
        <a
          href="#"
          @click.prevent="() => wear('signup')"
        >registrazione</a>.
      </p>
    </div>
    <div v-else-if="mask == 'signup'">
      <p>
        Se non hai ancora un profilo, inserisci qui i tuoi dati e potrai accedere. Se hai già un profilo, torna alla pagina di
        <a
          href="#"
          @click.prevent="() => wear('login')"
        >accesso</a>.
      </p>
    </div>
    <div v-else-if="mask == 'reset'">
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
    </div>

    <b-input-group size="lg">
      <b-input-group-prepend is-text>
        <font-awesome-icon icon="envelope"></font-awesome-icon>
      </b-input-group-prepend>
      <b-form-input
        v-model="email"
        placeholder="Email address"
        autofocus
        @keyup.ctrl.insert="() => { email = 'user@example.com'; password = 'pass' ; attempt_login() ;}"
        @keyup.ctrl.alt.insert="() => { email = 'admin@example.com'; password = 'pass' ; attempt_login() ;}"
      ></b-form-input>
    </b-input-group>

    <b-button
      v-if="mask == 'reset'"
      block
      :disabled="code_sent"
      class="my-2"
      @click="send_code"
    >{{ code_sent ? 'Codice inviato (controlla la posta)' : 'Invia il codice' }}</b-button>

    <b-input-group v-if="mask == 'reset'" size="lg">
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
        <font-awesome-icon icon="lock"></font-awesome-icon>
      </b-input-group-prepend>
      <b-form-input
        v-model="password"
        placeholder="Password"
        type="password"
        @keyup.enter="attempt_login"
      ></b-form-input>
    </b-input-group>

    <b-input-group v-if="mask == 'signup' || mask == 'reset'" size="lg">
      <b-input-group-prepend is-text>
        <font-awesome-icon icon="check"></font-awesome-icon>
      </b-input-group-prepend>
      <b-form-input
        v-model="password_confirmation"
        placeholder="Conferma password"
        type="password"
        @keyup.enter="attempt_signup"
      ></b-form-input>
    </b-input-group>

    <b-alert v-if="wrong_credentials" variant="warning" class="mt-2" show dismissible>
      <b>Le credenziali inserite non sono riconosciute.</b>
      <br />Hai scritto bene l'indirizzo mail?
      <br />
      <a href="#" @click.prevent="() => wear('reset')">Hai dimenticato la password?</a>
    </b-alert>
  </b-modal>
</template>

<script>
export default {
  props: {},
  data: () => ({
    visible: true,
    mask: "login",
    email: null,
    password: null,
    password_confirmation: null,
    reset_code: null,
    wrong_credentials: false,
    code_sent: false
  }),
  computed: {
    eventOk() {
      if (this.mask == "login") return this.attempt_login;
      else if (this.mask == "signup") return this.attempt_signup;
      else if (this.mask == "reset") return this.attempt_reset;
      else return null;
    },
    modalTitle() {
      if (this.mask == "login") return "Accedi all'applicazione";
      else if (this.mask == "signup") return "Crea un profilo";
      else if (this.mask == "reset") return "Richiedi nuova password";
      else return null;
    },
    okOnly() {
      if (this.mask == "login") return true;
      else return false;
    },
    okTitle() {
      if (this.mask == "login") return "Accedi";
      else if (this.mask == "signup") return "Registrami";
      else if (this.mask == "reset") return "Reset password";
      else return null;
    }
  },
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
          this.$store.dispatch("auth_refresh");
          this.$store.commit("page", "main");
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
          this.$store.commit("success_alert", "Utente creato con successo.");
          this.$session.set("authtoken", result.data.access_token);
          this.$store.dispatch("auth_refresh");
          this.$store.commit("page", "main");
        })
        .catch(err => {
          console.log("Error >> ", err);
          this.$store.commit(
            "warning_alert",
            "Qualcosa è andato storto. Potrebbe essere che la mail è già in uso."
          );
        });
    },
    send_code() {
      this.code_sent = true;
      this.axios
        .post("/users/password_reset_request", { email: this.$data.email })
        .then(result => {
          console.log("Backend (code request) >>", result.data);
        })
        .catch(err => {
          console.log("Error (code request)", err);
        });
    },
    attempt_reset() {
      this.axios
        .post("/users/password_reset", {
          email: this.$data.email,
          token: this.$data.reset_code,
          password: this.$data.password,
          password_confirmation: this.$data.password_confirmation
        })
        .then(result => {
          console.log("Backend (reset request) >>", result.data);
          this.$store.commit(
            "success_alert",
            "La password è stata reimpostata."
          );
        })
        .catch(err => {
          console.log("Error (reset request)", err);
        this.$store.commit("warning_alert", "Qualcosa è andato storto.")
        });
    }
  }
};
</script>

<style scoped>
</style>