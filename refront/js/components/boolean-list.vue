<template>
  <b-list-group flush>
    <b-list-group-item
      button
      v-for="(item, index) in array"
      :key="keyGetter(item, index)"
      class="d-flex justify-content-between align-items-center"
      @click="event => callback(item, index)"
    >
      <span>{{ nameGetter(item, index) }}</span>
      <b-overlay :show="waiting_array[index]" rounded="sm">
        <span>
          <b-form-checkbox
            :checked="booleanGetter(item, index)"
            name="check-button"
            switch
            @input="toggle(item, index)"
          ></b-form-checkbox>
        </span>
      </b-overlay>
    </b-list-group-item>
  </b-list-group>
</template>

<script>
module.exports = {
  name: "boolean-list",
  components: {},
  props: {
    array: Array,
    keyGetter: {
      type: Function,
      default: (item, index) => "boolean-list-item" + item.id + index
    },
    nameGetter: {
      type: Function,
      default: (item, index) => item.short || "undefined naming"
    },
    booleanGetter: {
      type: Function,
      default: item => item.boolean_value
    },
    booleanToggler: {
      type: Function,
      default: (item, index) =>
        (this.array[index].boolean_value = !this.array[index].boolean_value)
    },
    callback: {
      type: Function,
      default: () => {}
    }
  },
  data() {
    return {
    waiting_array: this.array.map(item => false)
    }
  },
  methods: {
    async toggle(item, index) {
      this.waiting_array[index] = true;
      await this.booleanToggler(item, index);
      temp = [ ...this.waiting_array]
      temp[index] = false;
      this.waiting_array = [...temp]
    }
  }
};
</script>

<style scoped>
</style>