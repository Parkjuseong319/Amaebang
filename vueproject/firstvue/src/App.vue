<template>
  <v-app>
    <v-main>
      <router-view/>
    </v-main>
  </v-app>
  <div class="name">{{ name }}</div>
</template>

<script>
export default {
  setup(){
    const name = 'App';

    return {
      name
    }
  },
  
}
</script>
