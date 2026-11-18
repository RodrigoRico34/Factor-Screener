<!--
  Author:      Samuel Theytaz
  Created:     18.11.2026
  Modified:    18.11.2026
  Description: Loading spinner shown while the application waits for an answer of the backend
-->

<template>
  <div class="loading" role="status">
    <span class="spinner"></span>
    <span>Chargement des données…</span>
  </div>
</template>

<style scoped>
.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 24px 32px;
  border: 1px solid var(--fs-bordure-defaut);
  border-radius: 12px;
  background-color: var(--fs-fond-surface);
  color: var(--fs-texte-secondaire);
}

.spinner {
  width: 32px;
  height: 32px;
  box-sizing: border-box;
  border: 3px solid var(--fs-decile-vide);
  border-top-color: var(--fs-bleu-accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
