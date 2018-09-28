<template>
<div>
<nav class="navbar navbar-light bg-dark">
  <div class="head">
    <h2 class="name">{{msg}}</h2>
   <form class="form-inline">
    <input v-model="fcommand" class="form-control mr-sm-2" type="search" placeholder="Команда" aria-label="Search">
    <input v-model="scommand" class="form-control mr-sm-2" type="search" placeholder="Команда" aria-label="Search"> 
    <select class="form-control">
     <option v-for="i in sport" :key="i" >{{ i }}</option>
    </select>

    <button @click="Parse()" class="btn btn-outline-success my-2 my-sm-0 find" type="submit">Найти</button>
  </form>
  </div>
</nav>
</div>
</template>

<script>
import axios from "axios"

export default {
  name: 'Main',
  data () {
    return {
      msg: 'Elliott Fibonacci',
      change:"",
      fcommand:"",
      scommand:"",
      sport:[
        "Футбол",
        "Хоккей",
        "Теннис",
        "Баскетбол",
        "Волейбол",
        "Гандбол",
        "Футзал",
        "Бейсбол"
      ]
    }
  },
  methods:{
    Parse(){
      console.log(this.i)
      console.log(this.fcommand)
      console.log(this.scommand)
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
.find{
  margin-left: 15px;
}
</style>
