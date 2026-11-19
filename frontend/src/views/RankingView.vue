<template>
  <h1>Ranking momentum</h1>
  <p class="subtitle">
    Les actions du S&P 500 classées selon leur score momentum sur 12 mois
    (rendement cumulé). Décile 1 : losers, décile 10 : winners.
  </p>

  <div class="filters">
    <div class="search-box">
      <span class="search-icon">&#x1F50D;</span>
      <input
          type="text"
          placeholder="Rechercher un ticker ou un nom"
      />
    </div>

    <div class="sector-filter">
      <span class="sector-label">Secteur</span>
      <select>
        <option>Tous les secteurs</option>
      </select>
    </div>
  </div>

  <p v-if="loading" class="status">Chargement...</p>
  <p v-else-if="error" class="status error">Erreur : {{ error }}</p>

  <table v-else>
    <thead>
    <tr>
      <th @click="toggleSort('ticker')">Ticker {{ sortIcon('ticker') }}</th>
      <th @click="toggleSort('name')">Nom {{ sortIcon('name') }}</th>
      <th @click="toggleSort('sector')">Secteur {{ sortIcon('sector') }}</th>
      <th @click="toggleSort('score_12m')" class="col-right">Score 12m {{ sortIcon('score_12m') }}</th>
      <th @click="toggleSort('decile')">Décile {{ sortIcon('decile') }}</th>
    </tr>
    </thead>
    <tbody>
    <tr v-for="stock in sortedStocks" :key="stock.ticker">
      <td>
        <a class="number" href="#">{{ stock.ticker }}</a>
      </td>
      <td>{{ stock.name }}</td>
      <td>{{ stock.sector }}</td>
      <td class="col-right">
          <span
              class="number"
              :class="stock.score_12m >= 0 ? 'positive' : 'negative'"
          >
            {{ formatScore(stock.score_12m) }}
          </span>
      </td>
      <td>
        <div class="decile-cell">
          <span class="number">{{ stock.decile ?? '—' }}</span>
          <div class="decile-bar">
              <span
                  v-for="i in 10"
                  :key="i"
                  class="decile-block"
                  :class="{ filled: i <= (stock.decile ?? 0) }"
              ></span>
          </div>
        </div>
      </td>
    </tr>
    </tbody>
  </table>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getStocks } from '@/services/api'

const stocks = ref([])
const loading = ref(true)
const error = ref(null)

// Sort state: default is score 12m descending (best performers on top)
const sortKey = ref('score_12m')
const sortAsc = ref(false)

function toggleSort(key) {
  if (sortKey.value === key) {
    sortAsc.value = !sortAsc.value
  } else {
    sortKey.value = key
    sortAsc.value = true
  }
}

function sortIcon(key) {
  if (sortKey.value !== key) return '⇅'
  return sortAsc.value ? '↑' : '↓'
}

const sortedStocks = computed(() => {
  return [...stocks.value].sort((a, b) => {
    let valA = a[sortKey.value]
    let valB = b[sortKey.value]

    // Null values go to the end
    if (valA == null) return 1
    if (valB == null) return -1

    if (typeof valA === 'string') {
      valA = valA.toLowerCase()
      valB = valB.toLowerCase()
    }

    if (valA < valB) return sortAsc.value ? -1 : 1
    if (valA > valB) return sortAsc.value ? 1 : -1
    return 0
  })
})

function formatScore(value) {
  if (value == null) return '—'
  const sign = value >= 0 ? '+' : ''
  return sign + value.toFixed(3)
}

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

<!-- CSS Generate by Claude -->

<style scoped>
.subtitle {
  margin: 8px 0 32px;
  color: var(--fs-texte-secondaire);
  font-size: 14px;
}

.filters {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 300px;
  height: 40px;
  padding: 0 16px;
  border: 1px solid var(--fs-bordure-forte);
  border-radius: 8px;
  background-color: var(--fs-fond-surface);
}

.search-box input {
  flex: 1;
  border: none;
  background: none;
  color: var(--fs-texte-principal);
  font-family: inherit;
  font-size: 14px;
  outline: none;
}

.search-box input::placeholder {
  color: var(--fs-texte-discret);
}

.search-icon {
  color: var(--fs-texte-discret);
  font-size: 14px;
}

.sector-filter {
  display: flex;
  align-items: center;
  gap: 8px;
  height: 40px;
  padding: 0 16px;
  border: 1px solid var(--fs-bordure-forte);
  border-radius: 8px;
  background-color: var(--fs-fond-surface);
}

.sector-label {
  color: var(--fs-texte-secondaire);
  font-size: 14px;
}

.sector-filter select {
  border: none;
  background: none;
  color: var(--fs-texte-principal);
  font-family: inherit;
  font-size: 14px;
  font-weight: 600;
  outline: none;
  cursor: pointer;
}

.sector-filter select option {
  background-color: var(--fs-fond-surface);
}

.status {
  color: var(--fs-texte-secondaire);
}

.status.error {
  color: var(--fs-signal-negatif);
}

.col-right {
  text-align: right;
}

.positive {
  color: var(--fs-signal-positif);
}

.negative {
  color: var(--fs-signal-negatif);
}

.decile-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.decile-bar {
  display: flex;
  gap: 2px;
}

.decile-block {
  width: 6px;
  height: 16px;
  border-radius: 1px;
  background-color: var(--fs-decile-vide);
}

.decile-block.filled {
  background-color: var(--fs-bleu-accent);
}

th {
  cursor: pointer;
  user-select: none;
}
</style>

