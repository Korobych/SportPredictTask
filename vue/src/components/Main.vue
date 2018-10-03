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
  </form>
  <div class="butt">
    <center><button @click="Parse()" class="btn btn-outline-success my-2 my-sm-0 find">Найти</button></center>
  </div>
  </div>
</nav>
<div v-bind:class="{ loader: isActive }">{{info}}</div>
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
      isActive:false,
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
      this.isActive = true;
      axios.post('http://localhost:5000/today',{"sport":this.change})
      .then(res=>{
        this.isActive = false
        this.info = res.data
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
.butt{
   margin-left: 600px;
   margin-top:-35px;
}
.loader,
.loader:before,
.loader:after {
  background: red;
  -webkit-animation: load1 1s infinite ease-in-out;
  animation: load1 1s infinite ease-in-out;
  width: 1em;
  height: 4em;
}
.loader {
  color: red;
  text-indent: -9999em;
  margin: 88px auto;
  position: relative;
  font-size: 11px;
  -webkit-transform: translateZ(0);
  -ms-transform: translateZ(0);
  transform: translateZ(0);
  -webkit-animation-delay: -0.16s;
  animation-delay: -0.16s;
}
.loader:before,
.loader:after {
  position: absolute;
  top: 0;
  content: '';
}
.loader:before {
  left: -1.5em;
  -webkit-animation-delay: -0.32s;
  animation-delay: -0.32s;
}
.loader:after {
  left: 1.5em;
}
@-webkit-keyframes load1 {
  0%,
  80%,
  100% {
    box-shadow: 0 0;
    height: 4em;
  }
  40% {
    box-shadow: 0 -2em;
    height: 5em;
  }
}
@keyframes load1 {
  0%,
  80%,
  100% {
    box-shadow: 0 0;
    height: 4em;
  }
  40% {
    box-shadow: 0 -2em;
    height: 5em;
  }
}


</style>
