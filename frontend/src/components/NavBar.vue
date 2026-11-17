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
  background-color: #0f1a2d;
  border-bottom: 1px solid #1f2e48;
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
  color: #97a5bd;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
}

.links a:hover {
  color: #e6ecf5;
}

/* RouterLink adds this class to the link of the current page */
.links a.router-link-active {
  color: #e6ecf5;
  border-bottom-color: #5b9be0;
}
</style>
