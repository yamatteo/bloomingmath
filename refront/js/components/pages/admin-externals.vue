<template>
  <b-container class="mt-4">
    <b-row class="mb-3">
      <b-col>
        <h2 class="mb-3">Amministra contenuti esterni</h2>
        <b-form-select v-model="selected_node" :options="nodes_options"></b-form-select>
      </b-col>
    </b-row>
    <b-row v-if="node_details">
      <b-col>
        <base-card title="Externals">
          <base-list
            v-if="editing_external==null"
            :array="node_details.externals"
            :key-getter="item => 'external'"
            :pills="[{icon:'edit', callback: edit_external}]"
          ></base-list>
          <b-button block v-if="editing_external==null" @click="add_external">Add one</b-button>
          <div v-else>
            <base-input
              :value="node_details.externals[this.editing_external].short"
              @input="(event) => {node_details.externals[this.editing_external].short = event}"
            ></base-input>
            <base-input
              :value="node_details.externals[this.editing_external].url"
              @input="(event) => {node_details.externals[this.editing_external].url = event}"
            ></base-input>
            <base-textarea
              :value="node_details.externals[this.editing_external].long"
              @input="(event) => {node_details.externals[this.editing_external].long = event}"
            ></base-textarea>
            <base-button @click="save">Fatto</base-button>
          </div>
        </base-card>
      </b-col>
      <b-col>
        <base-card title="Content">
          <b-list-group flush>
            <b-list-group-item
              button
              v-for="(content, index) in node_details.contents"
              :key="'content'+index"
              class="d-flex justify-content-between align-items-center"
              @click="() => reader(content.id)"
            >
              <span>{{ content.short || content.id }}</span>
            </b-list-group-item>
          </b-list-group>
        </base-card>
        <base-card title="External Contents">
          <b-list-group flush>
            <b-list-group-item
              button
              v-for="(content, index) in node_details.external_contents"
              :key="'content'+index"
              class="d-flex justify-content-between align-items-center"
            >
              <p>
                {{ ec_dict[content.id].short }}
                <a :href="ec_dict[content.id].url">link</a>
              </p>
            </b-list-group-item>
          </b-list-group>
        </base-card>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
module.exports = {
  name: "admin-externals-page",
  components: {
    "base-badge": window.httpVueLoader("/js/components/bases/base-badge.vue"),
    "base-button": window.httpVueLoader("/js/components/bases/base-button.vue"),
    "base-card": window.httpVueLoader("/js/components/bases/base-card.vue"),
    "base-input": window.httpVueLoader("/js/components/bases/base-input.vue"),
    "base-list": window.httpVueLoader("/js/components/bases/base-list.vue"),
    "base-textarea": window.httpVueLoader(
      "/js/components/bases/base-textarea.vue"
    )
  },
  props: {},
  data() {
    return {
      nodes_array: [],
      selected_node: null,
      node_details: null,
      node_modified: false,
      editing_external: null,
      ec_dict: null
    };
  },
  computed: {
    nodes_options() {
      return [
        { value: null, text: "Scegli un argomento" },
        ...this.nodes_array.map((node, index) => ({
          value: index,
          text: node.short
        }))
      ];
    }
  },
  methods: {
    add_external() {
      this.node_details.externals.push({
        short: "new external",
        url: "",
        long: ""
      });
      this.save();
    },
    edit_external(item, index) {
      this.editing_external = index;
    },
    async fetch_ecdict() {
      const result = await post("/external_contents/browse");
      this.ec_dict = Object.fromEntries( result.data.map( ec => [ec.id, {short: ec.short, url: ec.url}]) );
    },
    save() {
      post("/nodes/edit", {
        find: { id: this.nodes_array[this.selected_node].id },
        data: this.node_details
      })
        .then(result => {
          console.log("/nodes/edit", result.data);
        })
        .catch(error => {
          console.log("/nodes/edit", error);
        })
        .then(() => {
          this.editing_external = null;
        });
    },
    reader(id) {
      window.open(
        `http://bloomingmath.herokuapp.com/contents/download/${id}`,
        "_blank"
      );
    }
  },
  watch: {
    selected_node: function(id) {
      post("/nodes/read", {
        find: { id: this.nodes_array[this.selected_node].id }
      })
        .then(result => {
          this.node_details = result.data;
          this.node_modified = false;
        })
        .catch(error => {
          console.log("/nodes/browse", error);
        });
    }
  },
  mounted() {
    this.fetch_ecdict();
    post("/nodes/browse")
      .then(result => {
        this.nodes_array = result.data;
      })
      .catch(error => {
        console.log("/nodes/browse", error);
      });
  }
};
</script>

<style scoped>
</style>