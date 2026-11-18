<script setup>
import { computed } from 'vue'
import { RouterView } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import { pendingRequests } from '@/services/api'

const isLoading = computed(() => pendingRequests.value > 0)
</script>

<template>
  <NavBar />

  <main class="page" :class="{ 'is-loading': isLoading }">
    <RouterView />
  </main>

  <LoadingSpinner v-if="isLoading" class="overlay" />
</template>

<style scoped>
.page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 24px;
}

/* The page stays visible but greyed out and can't be clicked */
.page.is-loading {
  opacity: 0.4;
  pointer-events: none;
}

.overlay {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
</style>
