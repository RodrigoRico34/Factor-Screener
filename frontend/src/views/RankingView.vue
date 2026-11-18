<!--
  Author:      Samuel Theytaz
  Created:     17.11.2026
  Modified:    18.11.2026 (Timmy Marendaz, US-204)
  Description: Ranking page, shows the title and the ranking table
               The stocks are loaded from the backend when the page opens
-->

<script setup>
import { ref, onMounted } from 'vue'
import RankingTable from '@/components/RankingTable.vue'
import { getStocks } from '@/services/api'

const stocks = ref([])
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    stocks.value = await getStocks()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <h1>Ranking momentum</h1>
  <p v-if="error" class="error">Impossible de charger les actions : {{ error }}</p>
  <RankingTable :stocks="stocks" :loading="loading" />
</template>

<style scoped>
.error {
  color: #ef5b5b;
  font-size: 14px;
}
</style>