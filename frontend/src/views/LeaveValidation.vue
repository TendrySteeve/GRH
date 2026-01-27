<script setup>
import { onMounted, ref } from 'vue';
import MainLayout from '../layouts/MainLayout.vue'
import { getAllLeaves } from '../api/leave';

const allLeaves = ref([])

const loadAllLeaves = async () => {
  try {
    const res = await getAllLeaves()
    if (res) {
      allLeaves.value = res
    }
  } catch (error) {
    
  }
}

onMounted(() => {
  loadAllLeaves()
})
</script>
<template>
  <MainLayout>
  </MainLayout>
</template>

<style scoped>

</style>