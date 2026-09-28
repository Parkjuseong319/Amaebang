<template>
  <div>좀 되라 이젠</div>
  <div class="name">{{ name }}</div>
</template>

<script>
export default {
  setup(){
    const name = 'vue 거지같애'

    return {
      name
    }
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
