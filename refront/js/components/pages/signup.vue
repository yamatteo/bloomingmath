<template>
  <b-container class="mt-3">
    <b-row>
      <b-col>
        <base-card title="Crea un profilo" forced :over_body="attempting">
          <div>
            <p>
              Se vuoi puoi creare un
              <b>profilo</b> inserendo la tua mail e una password. Questi dati non verranno condivisi con nessuno. Se hai già un profilo (se hai già usato questa applicazione altre volte), devi solo effettuare
              <a
                href="#"
                @click.prevent="() => goto('login')"
              >l'accesso</a>.
            </p>
          </div>

          <base-input v-model="email" icon="envelope" placeholder="Email"></base-input>
          <base-input v-model="password" icon="lock" placeholder="Password" type="password"></base-input>
          <base-input
            v-model="password_confirmation"
            icon="check"
            placeholder="Password (conferma)"
            type="password"
            @keyup.enter="attempt_signup"
          ></base-input>
          <base-button @click="attempt_signup">Crea un nuovo profilo</base-button>
        </base-card>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
module.exports = {
  name: "signup-page",
  components: {
    "base-button": window.httpVueLoader("/js/components/bases/base-button.vue"),
    "base-card": window.httpVueLoader("/js/components/bases/base-card.vue"),
    "base-input": window.httpVueLoader("/js/components/bases/base-input.vue")
  },
  data: () => ({
    email: null,
    password: null,
    password_confirmation: null,
    attempting: false
  }),
  methods: {
    attempt_signup() {
      this.attempting = true;
      post("/users/signup", {
        email: this.$data.email,
        password: this.$data.password,
        password_confirmation: this.$data.password_confirmation
      })
        .then(result => {
          console.log("POST /user/signup", result.data);
          store.dispatch("update_authtoken", result.data.access_token);
          this.goto("home");
          this.pushcard("message", {
            message:
              "Il nuovo profilo è stato registrato. Non dimenticare la password.",
            variant: "success"
          });
        })
        .catch(err => {
          console.log("POST /user/signup", err);
          this.pushcard("message", {
            message:
              "Qualcosa ha impedito la registrazione del nuovo profilo. Controlla di aver scritto bene l'indirizzo mail e la password. Se hai già usato questa applicazione il profilo esiste già, non devi crearlo.",
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