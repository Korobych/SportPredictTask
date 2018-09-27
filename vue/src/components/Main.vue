<template>
<div>
<nav class="navbar navbar-light bg-dark">
  <div class="head">
    <h2 class="name">{{msg}}</h2>
   <form class="form-inline">
    <input class="form-control mr-sm-2" type="search" placeholder="Команда" aria-label="Search">
    <input class="form-control mr-sm-2" type="search" placeholder="Команда" aria-label="Search">
    <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Найти</button>
  </form>
  </div>
</nav>
</div>
</template>

<script>
export default {
  name: 'Main',
  data () {
    return {
      msg: 'Elliott Fibonacci'
    }
  }
}
</script>
<style>
.head{
  margin-left: 35%;
}
.name{
  margin-left: 25%;
  color: azure;
}
</style>
