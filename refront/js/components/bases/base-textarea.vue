<template>
  <b-input-group>
    <b-input-group-prepend is-text>
      <i :class="`fas fa-${icon} mx-auto`"></i>
    </b-input-group-prepend>
    <b-form-textarea
      :value="value"
      @input="$emit('input', $event)"
      :placeholder="placeholder"
      rows="2"
      max-rows="6"
      @keyup="$emit('keyup', $event)"
    ></b-form-textarea>
  </b-input-group>
</template>

<script>
module.exports = {
  name: "base-input",
  props: {
    value: {
      type: String,
      default: ""
    },
    icon: {
      type: String,
      default: "keyboard"
    },
    placeholder: {
      type: String,
      default: "Write here..."
    },
  },
};
</script>

<style scoped>
.input-group-text {
  width: 3em;
  text-align: center;
}
</style>