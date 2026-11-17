/**
 * Author:      Samuel Theytaz
 * Created:     17.11.2026
 * Modified:    17.11.2026
 * Description: Router of the application, with the routes of the Ranking, Detail and Backtest pages
 */

import { createRouter, createWebHistory } from 'vue-router'
import RankingView from '@/views/RankingView.vue'
import DetailView from '@/views/DetailView.vue'
import BacktestView from '@/views/BacktestView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'ranking', component: RankingView },
    { path: '/detail', name: 'detail', component: DetailView },
    { path: '/backtest', name: 'backtest', component: BacktestView },
  ],
})

export default router
