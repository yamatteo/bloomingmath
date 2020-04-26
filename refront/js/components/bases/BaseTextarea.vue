<template>
  <b-input-group>
    <template v-slot:prepend>
      <b-input-group-text v-if="field">{{ field }}</b-input-group-text>
    </template>
    <b-form-textarea
      :value="value"
      @input="updateValue()"
      :placeholder="placeholder"
      :rows="rows"
      :max-rows="maxRows"
      ref="internalTextarea"
    ></b-form-textarea>
  </b-input-group>
</template>

<script>
export default {
  name: "BaseTextarea",
  props: {
    field: {
      type: String,
      default: ""
    },
    maxRows: {
      type: Number,
      default: 6
    },
    placeholder: {
      type: String,
      default: "Enter text here..."
    },
    rows: {
      type: Number,
      default: 3
    },
    value: {
      type: String
    }
  },
  methods: {
    updateValue() {
      this.$emit("input", this.$refs.internalTextarea.localValue)
    }
  }
};
</script>

<style scoped>
.input-group-text {
  width: 3.6em;
  text-align: center;
}
</style>