<template>
  <b-form
    inline
    class="my-2"
    @submit.prevent="submitted"
    @keyup.enter="emit_submit"
  >
    <b-input-group size="sm" class="mb-2 mr-sm-2 mb-sm-0 w-100">
      <template v-slot:prepend v-if="icon!=null | text!= null">
        <b-input-group-text>
          {{ text }}
          <b-icon :icon="icon" />
        </b-input-group-text>
      </template>
      <slot></slot>
    </b-input-group>
  </b-form>
</template>

<script>
import lodash from "lodash";
export default {
  props: {
    text: {
      type: String,
      default: null
    },
    icon: {
      type: String,
      default: null
    },
    path: {
      type: String,
      required: true
    },
    success: {
      type: Function,
      default: data => {
        console.log(data);
      }
    },
    error: {
      type: Function,
      default: data => {
        console.log(data);
      }
    },
    confirmation: {
      type: Boolean,
      default: false
    },
    hidden_data: {
      type: Object,
      default: () => ({})
    }
  },
  methods: {
    emit_submit() {
      this.$emit("submit");
    },
    submitted() {
      let proceed
      if (this.confirmation) {
        proceed = confirm("Do you want to submit?");
      } else {
        proceed = true;
      }
      if (proceed) {
        let body = {};
        for (const child of this.$children) {
          if (child.selectedFile) lodash.set(body, child.name, child.selectedFile);
          else lodash.set(body, child.name, child.localValue);
        }
        Object.assign(body, this.hidden_data)
        console.log(body)
        this.axios
          .post(this.path, body)
          .then(response => {
            this.success(response.data);
          })
          .catch(err => {
            this.error(err);
          });
      }
    }
  }
};
</script>

<style scoped>
</style>