<!--
  Author:      Samuel Theytaz
  Created:     17.11.2026
  Modified:    18.11.2026 (Timmy Marendaz, US-204)
  Description: Ranking page, shows the title and the ranking table
               The table is empty for now, the real data comes with US-205
-->

<script setup>
import RankingTable from '@/components/RankingTable.vue'

const stocks = []
</script>

<template>
  <h1>Ranking momentum</h1>
  <RankingTable :stocks="stocks" />
</template>