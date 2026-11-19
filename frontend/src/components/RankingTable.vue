<!--
  Author:      Timmy Marendaz
  Created:     17.11.2026
  Modified:    18.11.2026
  Description: Ranking table (US-204) with the columns ticker, name, sector, 12m score and decile
               It only displays the stocks it receives, it doesn't load them itself
               While "loading" is true, a loading row is shown instead of the stocks
-->

<script setup>
defineProps({
  stocks: {
    type: Array,
    required: true,
  },
  loading: {
    type: Boolean,
    default: false,
  },
})

const columns = [
  { key: 'ticker', label: 'Ticker' },
  { key: 'name', label: 'Nom' },
  { key: 'sector', label: 'Secteur' },
  { key: 'momentum_12m', label: 'Score 12m', align: 'right' },
  { key: 'decile', label: 'Décile' },
]

// 0.947 -> "+0.947" and -0.45 -> "−0.450"
function formatScore(score) {
  const sign = score >= 0 ? '+' : '−'
  return sign + Math.abs(score).toFixed(3)
}
</script>

<template>
  <div class="table-card">
    <table class="ranking-table">
      <thead>
      <tr>
        <th
            v-for="col in columns"
            :key="col.key"
            :class="[`col-${col.key}`, { right: col.align === 'right' }]"
        >
          {{ col.label }}
        </th>
      </tr>
      </thead>

      <tbody>
      <tr v-if="loading">
        <td :colspan="columns.length" class="state">
          <span class="loader" aria-hidden="true"></span>
          Chargement des actions…
        </td>
      </tr>

      <tr v-for="stock in loading ? [] : stocks" :key="stock.ticker">
        <td class="col-ticker">
          <span class="ticker">{{ stock.ticker }}</span>
        </td>
        <td class="col-name">{{ stock.name }}</td>
        <td class="col-sector">{{ stock.sector }}</td>
        <td
            class="col-momentum_12m right"
            :class="stock.momentum_12m >= 0 ? 'positive' : 'negative'"
        >
          {{ formatScore(stock.momentum_12m) }}
        </td>
        <td class="col-decile">
            <span class="decile">
              <span class="decile-number">{{ stock.decile }}</span>
              <span class="decile-bars" :aria-label="`Décile ${stock.decile} sur 10`">
                <span
                    v-for="n in 10"
                    :key="n"
                    class="bar"
                    :class="{ filled: n <= stock.decile }"
                ></span>
              </span>
            </span>
        </td>
      </tr>

      <tr v-if="!loading && stocks.length === 0">
        <td :colspan="columns.length" class="state">Aucune action à afficher</td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
/* Colors, same palette as the NavBar */
.table-card {
  --card-bg: #0f1a2d;
  --header-bg: #13203a;
  --border: #1f2e48;
  --text: #e6ecf5;
  --text-muted: #97a5bd;
  --accent: #5b9be0;
  --bar-empty: #1d3352;
  --positive: #34c38f;
  --negative: #ef5b5b;
  --mono: 'JetBrains Mono', 'SF Mono', 'Cascadia Mono', Consolas, monospace;

  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 10px;
  overflow: hidden;
}

.ranking-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
  color: var(--text);
}

th,
td {
  padding: 0 24px;
  text-align: left;
  white-space: nowrap;
}

.right {
  text-align: right;
}

/* Header */
thead tr {
  height: 48px;
  background: var(--header-bg);
  border-bottom: 1px solid var(--border);
}

th {
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-muted);
}

/* Rows */
tbody tr {
  height: 56px;
  border-bottom: 1px solid var(--border);
}

tbody tr:last-child {
  border-bottom: none;
}

/* Columns */
.col-ticker {
  width: 14%;
}

.ticker {
  font-family: var(--mono);
  font-size: 13px;
  color: var(--accent);
}

.col-name {
  width: 32%;
}

td.col-sector {
  width: 28%;
  font-size: 13px;
  color: var(--text-muted);
}

td.col-momentum_12m {
  width: 10%;
  font-family: var(--mono);
  font-size: 13px;
}

.positive {
  color: var(--positive);
}

.negative {
  color: var(--negative);
}

/* Decile: number + 10 bars */
.decile {
  display: inline-flex;
  align-items: center;
  gap: 16px;
}

.decile-number {
  font-family: var(--mono);
  font-size: 13px;
  min-width: 16px;
}

.decile-bars {
  display: inline-flex;
  gap: 2px;
}

.bar {
  width: 5px;
  height: 14px;
  border-radius: 1px;
  background: var(--bar-empty);
}

.bar.filled {
  background: var(--accent);
}

/* Loading and empty rows */
.state {
  height: 80px;
  text-align: center;
  color: var(--text-muted);
}

.loader {
  display: inline-block;
  width: 14px;
  height: 14px;
  margin-right: 10px;
  vertical-align: -2px;
  border: 2px solid var(--bar-empty);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>