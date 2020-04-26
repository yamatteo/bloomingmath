<template>
  <b-input-group>
    <b-input-group-prepend is-text>
      <i :class="`fas fa-${icon} mx-auto`"></i>
    </b-input-group-prepend>
    <b-form-input
      :value="value"
      @input="$emit('input', $event)"
      :placeholder="placeholder"
      :type="type"
      @keyup="$emit('keyup', $event)"
    ></b-form-input>
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
    type: {
      type: String,
      default: "text"
    }
  },
};
</script>

<style scoped>
.input-group-text {
  width: 3em;
  text-align: center;
}
</style>