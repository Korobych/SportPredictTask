<template>
<div>
<nav class="navbar navbar-light bg-dark">
  <div class="head">
    <h2 class="name">{{msg}}</h2>
   <form class="form-inline">
    <input v-model="fcommand" class="form-control mr-sm-2" type="search" placeholder="Команда" aria-label="Search">
    <input v-model="scommand" class="form-control mr-sm-2" type="search" placeholder="Команда" aria-label="Search"> 
    <select  v-model="change" class="form-control">
     <option  v-for="i in sport" :key="i" >{{ i }}</option>
    </select>
    <button @click="Parse()" class="btn btn-outline-success my-2 my-sm-0 find" type="submit">Найти</button>
  </form>

  </div>
</nav>
<center>{{info}}</center>
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
      info:"",
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
      axios.post('http://localhost:5000/today',{"sport":this.change})
      .then(res=>{
        this.info = res
      })
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
