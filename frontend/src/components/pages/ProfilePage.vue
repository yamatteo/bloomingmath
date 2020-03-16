<template>
  <BasePage title="Il tuo profilo">
    <BaseCard title="Informazioni sull'utente">
      <p>
        <b>La tua mail:</b>
        {{ current_user.email }}
      </p>
    </BaseCard>

    <BaseCard title="Gruppi di appartenenza" scroll>
      <BaseListGroup>
        <template v-slot:header>I gruppi di cui fai parte</template>
        <BaseListGroupItem v-for="group in current_user.groups" :key="group.id">
          {{ group.short }}
          <template v-slot:pills>
            <BasePill icon="times-circle" :onClick="() => pull_yourself_from(group.id)"></BasePill>
          </template>
        </BaseListGroupItem>
        <template v-slot:empty>
          <BaseListGroupItem disabled>nessuno</BaseListGroupItem>
        </template>
      </BaseListGroup>

      <BaseListGroup class="mt-2">
        <template v-slot:header>I gruppi in cui puoi entrare</template>
        <BaseListGroupItem v-for="group in current_user.available_groups" :key="group.id">
          {{ group.short }}
          <template v-slot:pills>
            <BasePill icon="thumbs-up" :onClick="() => push_yourself_from(group.id)"></BasePill>
          </template>
        </BaseListGroupItem>

        <template v-slot:empty>
          <BaseListGroupItem disabled>nessuno</BaseListGroupItem>
        </template>
      </BaseListGroup>
    </BaseCard>
  </BasePage>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "ProfilePage",
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
    }
  }
};
</script>

<style scoped>
</style>