<template>
  <b-list-group flush>
    <b-list-group-item
      button
      v-for="(item, index) in array"
      :key="keyGetter(item) + index"
      class="d-flex justify-content-between align-items-center"
      @click="event => callback(item, index)"
    >
      <span>{{ nameGetter(item) }}</span>
      <span>
        <base-badge
          v-for="(info, pindex) in pills"
          :key="keyGetter(item) + index + 'pill' + pindex"
          pill
          :icon="info.icon"
          @click="event => info.callback(item, index)"
        ></base-badge>
      </span>
    </b-list-group-item>
  </b-list-group>
</template>

<script>
module.exports = {
  name: "base-list",
  components: {
    "base-badge": window.httpVueLoader("/js/components/bases/base-badge.vue")
  },
  props: {
    array: Array,
    keyGetter: {
      type: Function,
      default: item => item.id
    },
    nameGetter: {
      type: Function,
      default: item => item.short || "undefined naming"
    },
    pills: {
      type: Array,
      default: () => {
        return new Array();
      }
    },
    callback: {
      type: Function,
      default: () => {}
    }
  }
};
</script>

<style scoped>
</style>