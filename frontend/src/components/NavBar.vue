<!--
  Author:      Samuel Theytaz
  Created:     17.11.2026
  Modified:    17.11.2026
  Description: Navigation bar shown on every page, with the links to Ranking, Detail and Backtest
               The link of the current page is highlighted
-->

<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <header class="navbar">
    <div class="navbar-content">
      <div class="brand">
        <img src="@/assets/logo.svg" alt="" width="28" height="28" />
        <span>Factor Screener</span>
      </div>

      <nav class="links">
        <RouterLink to="/">Ranking</RouterLink>
        <RouterLink to="/detail">Détail action</RouterLink>
        <RouterLink to="/backtest">Backtester</RouterLink>
      </nav>
    </div>
  </header>
</template>

<style scoped>
.navbar {
  background-color: var(--fs-fond-surface);
  border-bottom: 1px solid var(--fs-bordure-defaut);
}

.navbar-content {
  display: flex;
  align-items: center;
  gap: 48px;
  max-width: 1200px;
  height: 64px;
  margin: 0 auto;
  padding: 0 24px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 15px;
  font-weight: 600;
}

.links {
  display: flex;
  align-self: stretch;
  gap: 4px;
}

.links a {
  display: flex;
  align-items: center;
  padding: 0 16px;
  border-bottom: 2px solid transparent;
  color: var(--fs-texte-secondaire);
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
}

.links a:hover {
  color: var(--fs-texte-principal);
}

/* RouterLink adds this class to the link of the current page */
.links a.router-link-active {
  color: var(--fs-texte-principal);
  border-bottom-color: var(--fs-bleu-accent);
}
</style>
