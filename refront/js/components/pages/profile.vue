<template>
  <b-container class="mt-3">
    <b-row>
      <b-col>
        <base-card title="Profilo utente">
          <p>
            <b>La tua email:</b>
            {{ user.email }}
          </p>
          <base-card title="Gruppi" class="mt-3">
            <b-list-group flush :key="'belongarray' + refresh">
              <b-list-group-item
                button
                v-for="(belong_info, index) in belong_array"
                :key="belong_info.id"
                class="d-flex justify-content-between align-items-center"
              >
                {{ belong_info.short }}
                <b-overlay :show="belong_info.disabled" rounded="sm">
                  <span>
                    <b-form-checkbox
                      :checked="belong_info.belong"
                      name="check-button"
                      switch
                      @input="switched(index)"
                    ></b-form-checkbox>
                  </span>
                </b-overlay>
              </b-list-group-item>
            </b-list-group>
          </base-card>
        </base-card>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
module.exports = {
  name: "profile-page",
  components: {
    "base-card": window.httpVueLoader("/js/components/bases/base-card.vue")
  },
  data() {
    return {
      refresh: 1
    };
  },
  computed: {
    user() {
      return store.state.current_user;
    },
    belong_array() {
      let l_belong_array = new Array();
      for (group of this.user.groups) {
        l_belong_array.push({
          id: group.id,
          short: group.short,
          belong: true,
          disabled: false
        });
      }
      for (group of this.user.available_groups) {
        l_belong_array.push({
          id: group.id,
          short: group.short,
          belong: false,
          disabled: false
        });
      }
      return l_belong_array;
    }
  },
  methods: {
    switched(index) {
      let bi = this.belong_array[index];
      let id = bi.id;
      let belong = bi.belong;
      let action = belong ? "/groups/pull_self" : "/groups/push_self";
      console.log("switched", id, belong);
      bi.disabled = true;
      this.refresh += 1;
      post(action, { group_id: id })
        .then(result => {
          console.log(result.data);
          bi.belong = !belong
        })
        .catch(error => {
          console.log(action, error);
        })
        .then(() => {
          bi.disabled = false;
          this.refresh += 1;
        });
    }
  }
};
</script>

<style scoped>
</style>