<template>
  <div>
    <b-modal
      v-model="modalShow"
      id="login-modal"
      @ok.prevent="attempt_login"
      ok-only
      okTitle="Login"
      @hide.prevent
    >
      <template v-slot:modal-header="">
        <h5 class="modal-title">Benvenut@ Eternauta</h5>
      </template>
      <b-alert
        v-if="alert_message"
        show
        dismissible
        variant="warning"
        @dismissed="dismiss_alert_message"
      >{{ alert_message }}</b-alert>

      <p>Per usare questa applicazione è necessario avere un profilo e accedere con i propri dati. È possibile aggiungere l'applicazione alla propria schermata del cellulare per rendere l'accesso più comodo.</p>

      <p>
        Per favore, inserisci i tuoi dati. Se non hai un profilo, vai alla pagina di
        <a href="#" @click.prevent="goto_signup">registrazione</a>.
      </p>

      <p>
        <!-- TODO: only for development -->
        <a
          href="#"
          class="my-1"
          @click="() => { email = 'user@example.com'; password = 'pass' ; attempt_login() ;}"
        >user@example.com login</a>
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
          @keyup.enter="attempt_login"
        ></b-form-input>
      </b-input-group>
    </b-modal>
  </div>
</template>

<script>
export default {
  name: "LoginModal",
  data() {
    return {
      email: null,
      password: null,
      alert_message: null
    };
  },
  computed: {
    modalShow: function() {
      return true;
    }
  },
  methods: {
    dismiss_alert_message() {
      this.$data.alert_message = null;
    },
    attempt_login() {
      console.log("Attempting login...");
      this.dismiss_alert_message();
      let store = this.$store;
      this.axios
        .post("/users/login", {
          email: this.$data.email,
          password: this.$data.password
        })
        .then(result => {
          console.log("Backend >> ", result.data);
          this.$session.set("authtoken", result.data.access_token);
          this.$store.dispatch("login_actualization", result.data.access_token);
          store.commit("see_modal", null);
        })
        .catch(err => {
          console.log("Error >> ", err);
          this.$data.alert_message = "Qualcosa è andato storto. Riprova...";
          this.$store.dispatch("login_actualization", null);
          store.commit("see_flash_modal", {
            text: "Accesso non riuscito!",
            variant: "warning"
          });
        });
    },
    goto_signup() {
      this.$store.commit("see_modal", "signup");
    }
  }
};
</script>

<style scoped>
</style>