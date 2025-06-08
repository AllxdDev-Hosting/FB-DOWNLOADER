<template>
  <div id="app">
    <Downloader />
  </div>
</template>

<script>
import Downloader from './components/Downloader.vue'

export default {
  name: 'App',
  components: {
    Downloader
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
