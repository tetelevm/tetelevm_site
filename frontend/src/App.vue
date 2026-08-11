<script setup>
const graphqlUrl = import.meta.env.VITE_GRAPHQL_URL
</script>

<template>
  <main>
    <h1>tetelevm</h1>
    <p>Личный сайт в разработке.</p>
    <a :href="graphqlUrl">GraphQL API</a>
  </main>
</template>
