<template>
  <b-navbar toggleable="sm" type="dark" class="py-1">
    <b-navbar-brand href="#" @click.prevent="brandClick">
      <slot name="brand">
        {{ brand }}
      </slot>
    </b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav class="ml-auto">
        <slot></slot>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<script>
export default {
  name: "BaseNavbar",
  props: {
    brand: {
      type: String,
      default: "Navbar"
    },
    brandClick: {
      type: Function,
      default: () => {return false}
    }
  }
};
</script>

<style scoped>
nav {
  background-color: #334;
}
</style>