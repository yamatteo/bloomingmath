<template>
  <div>
    <Navbar />
    <b-container>
      <b-row>
        <b-col></b-col>
        <b-col cols="12" sm="10" md="8">
          <h1>Admin Dashboard</h1>
          <Card title="Utenti">
            <div class="mb-2">
              <ul v-if="users.length" class="list-group list-group-flush">
                <ListGroupItem v-for="user in users" :key="user.id" :text="user.email"></ListGroupItem>
              </ul>
              <div v-else class="mb-2">
                <b>Nessun utente.</b>
              </div>
            </div>
          </Card>

          <Card title="Contenuti">
            <div class="mb-2">
              <ul v-if="contents.length" class="list-group list-group-flush">
                <ListGroupItem v-for="content in contents" :key="content.id" :text="content.short" :main="() => edit_content(content.id)"></ListGroupItem>
              </ul>
              <div v-else class="mb-2">
                <b>Nessun contenuto.</b>
              </div>

              <LittleForm icon="plus" path="/contents/add" :success="fetch_contents">
                <b-input name="short" placeholder="Short" />
                <b-input name="filetype" placeholder="Type" />
                <input type="submit" value="Aggiungi" />
              </LittleForm>
            </div>
          </Card>

          <Card title="Argomenti">
            <div class="mb-2">
              <ul v-if="nodes.length" class="list-group list-group-flush">
                <ListGroupItem v-for="node in nodes" :key="node.id" :text="node.short" 
                  :main="() => edit_node(node)"></ListGroupItem>
              </ul>
              <div v-else class="mb-2">
                <b>Nessun argomento.</b>
              </div>

              <LittleForm icon="plus" path="/nodes/add" :success="fetch_nodes">
                <b-input name="short" placeholder="Short" />
              </LittleForm>
            </div>
          </Card>

          <Card title="Gruppi">
            <div class="mb-2">
              <ul v-if="groups.length" class="list-group list-group-flush">
                <ListGroupItem
                  v-for="group in groups"
                  :key="group.id"
                  :text="group.short"
                  :main="() => edit_group(group)"
                ></ListGroupItem>
              </ul>
              <div v-else class="mb-2">
                <b>Nessun gruppo.</b>
              </div>

              <LittleForm icon="plus" path="/groups/add" :success="fetch_groups">
                <b-input name="short" placeholder="Short" />
              </LittleForm>
            </div>
          </Card>
        </b-col>
        <b-col></b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
export default {
  props: {},
  data: () => ({
    users: [],
    contents: [],
    nodes: [],
    groups: []
  }),
  computed: {
    need_update() {
      return this.$store.state.admin_update;
    }
  },
  components: {
    Navbar: () => import("@/components/Navbar"),
    Card: () => import("@/components/Card"),
    ListGroupItem: () => import("@/components/ListGroupItem"),
    LittleForm: () => import("@/components/LittleForm")
  },
  watch: {
    need_update(val) {
      if (val) {
        this.update();
        this.$store.commit("admin_update", false);
      }
    }
  },
  methods: {
    edit_content(content_id) {
      console.log("main with", content_id);
      
      this.axios
        .post("/contents/read", {
          find: { id: content_id },
          with_contents: true,
          with_other_contents: true
        })
        .then(response => {
          this.$store.commit("active_modal", {
            name: "ContentEditModal",
            props: { content: response.data }
          });
        })
        .catch(err => {
          console.log("Error (edit content) >>", err);
        });
    },
    edit_node(node) {
      this.axios
        .post("/nodes/read", {
          find: { id: node.id },
          with_contents: true,
          with_other_contents: true
        })
        .then(response => {
          this.$store.commit("active_modal", {
            name: "NodeEditModal",
            props: { node: response.data }
          });
        })
        .catch(err => {
          console.log("Error (edit node) >>", err);
        });
    },
    edit_group(group) {
      this.axios
        .post("/groups/read", {
          find: { id: group.id },
          with_nodes: true,
          with_other_nodes: true
        })
        .then(response => {
          this.$store.commit("active_modal", {
            name: "GroupEditModal",
            props: { group: response.data }
          });
        })
        .catch(err => {
          console.log("Error (edit group) >>", err);
        });
    },
    fetch_users() {
      this.axios
        .post("/users/browse")
        .then(response => {
          this.users = response.data;
        })
        .catch(err => {
          this.users = [];
          console.log(err);
        });
    },
    fetch_contents() {
      this.axios
        .post("/contents/browse")
        .then(response => {
          this.contents = response.data;
        })
        .catch(err => {
          this.contents = [];
          console.log(err);
        });
    },
    fetch_nodes() {
      this.axios
        .post("/nodes/browse")
        .then(response => {
          this.nodes = response.data;
        })
        .catch(err => {
          this.nodes = [];
          console.log(err);
        });
    },
    fetch_groups() {
      this.axios
        .post("/groups/browse")
        .then(response => {
          this.groups = response.data;
        })
        .catch(err => {
          this.groups = [];
          console.log(err);
        });
    },
    update() {
      this.fetch_users();
      this.fetch_contents();
      this.fetch_nodes();
      this.fetch_groups();
    }
  },
  mounted() {
    this.update();
  }
};
</script>

<style scoped>
.container {
  margin-top: 50px;
}
</style>