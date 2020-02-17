<template>
  <div>
    <b-modal
      v-model="modalShow"
      id="signup-modal"
      @ok.prevent="attempt_signup"
      @cancel.prevent="goto_login"
      okTitle="Registrami"
      cancelTitle="Annulla"
      @hide.prevent=""
    >
      <template v-slot:modal-header="">
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
          @click.prevent="goto_login"
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
  </div>
</template>

<script>
export default {
  name: "SignupModal",
  data() {
    return {
      email: null,
      password: null,
      password_confirmation: null,
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
    attempt_signup() {
      console.log("Attempting signup...");
      this.dismiss_alert_message();
      this.axios
        .post("/users/signup", {
          email: this.$data.email,
          password: this.$data.password,
          password_confirmation: this.$data.password_confirmation
        })
        .then(result => {
          console.log("Backend >> ", result.data);
          this.$session.start();
          this.$session.set("authtoken", result.data.access_token);
          this.$store.dispatch("login_actualization", result.data.access_token);
          // store.commit("see_login_modal", false); TODO avvisa del successo
        })
        .catch(err => {
          console.log("Error >> ", err);
          this.$data.alert_message =
            "Qualcosa è andato storto. Potrebbe essere che la mail è già in uso.";
          this.$store.dispatch("login_actualization", null);
          // TODO avvisa dell'errore
        });
    },
    goto_login() {
      this.$store.commit("see_modal", "login");
    }
  }
};
</script>

<style scoped>
</style>