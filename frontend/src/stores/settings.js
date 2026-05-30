import { defineStore } from 'pinia'

export const useSettingsStore = defineStore('settings', {
  state: () => ({
    enableFx: localStorage.getItem('enableFnaFx') !== 'false',
  }),
  actions: {
    toggleFx() {
      this.enableFx = !this.enableFx
      localStorage.setItem('enableFnaFx', this.enableFx)
    },
    resetFx() {
      this.enableFx = true
      localStorage.removeItem('enableFnaFx')
    }
  }
})