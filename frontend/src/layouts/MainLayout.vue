<script setup>
import Navbar from '../components/Navbar.vue';


</script>
<template>
  <div class="h-full w-full relative">
    <Navbar />

    <div class="flex-1 bg-gray-50">
      <slot></slot>
    </div>
  </div>
</template>