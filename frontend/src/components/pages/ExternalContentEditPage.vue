<template>
  <BasePage title="Contenuto esterno">
    <BaseCard title="Modifica il contenuto">
      <template v-slot:pills>
        <BasePill v-if="is_modified" icon="save" :onClick="save"></BasePill>
      </template>

      <b-input-group prepend="short">
        <b-form-input v-model="external_content.short" placeholder="Short" @change="has_changed"></b-form-input>
      </b-input-group>

      <b-input-group prepend="url">
        <b-form-input v-model="external_content.url" placeholder="Short" @change="has_changed"></b-form-input>
      </b-input-group>

      <b-input-group prepend="long">
        <b-form-textarea
          id="textarea"
          v-model="external_content.long"
          placeholder="Enter something..."
          rows="3"
          max-rows="6"
          @change="has_changed"
        ></b-form-textarea>
      </b-input-group>
    </BaseCard>

    
  </BasePage>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "ExternalContentEditPage",
  data: () => ({
    external_content: {},
    is_modified: false,
  }),
  computed: {
    ...mapState(["current_user"])
  },
  methods: {
    pull_yourself_from(group_id) {
      console.log("pull yourself from", group_id, "...");
      this.axios
        .post("/groups/pull_self", {
          group_id: group_id
        })
        .then(response => {
          console.log("Backend (pull yourself from) >>", response.data);
          this.$store.dispatch("fetch_cu");
        })
        .catch(err => {
          console.log("Error (pull yourself from) >>", err);
        });
    },
    push_yourself_from(group_id) {
      console.log("push yourself from", group_id, "...");
      this.axios
        .post("/groups/push_self", {
          group_id: group_id
        })
        .then(response => {
          console.log("Backend (push yourself from) >>", response.data);
          this.$store.dispatch("fetch_cu");
        })
        .catch(err => {
          console.log("Error (push yourself from) >>", err);
        });
    },
    fetch_content() {
      this.axios
        .post("/external_contents/read", {
          id: this.$store.state.page.external_content_id
        })
        .then(result => {
          this.external_content = result.data;
        })
        .catch(err => {
          console.log(err);
        });
    },
    save() {
      this.axios.post("/external_contents/edit", {
        find: {id: this.external_content.id},
        data: this.external_content
      }).then(result => {
        console.log(result.data);
        this.is_modified = false
      }).catch(err => {
        console.log("Error (saving) >>> ", err);
        
      })
    },
    has_changed() {
      this.is_modified = true
    }
  },
  mounted() {
    this.fetch_content();
  }
};
</script>

<style scoped>
</style>