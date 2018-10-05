<template>
<div>
<nav class="navbar navbar-light bg-dark">
  <div class="head">
    <h2 class="name">{{msg}}</h2>
   <form class="form-inline">
    <input v-model="fcommand" class="form-control mr-sm-2" type="search" placeholder="Команда" aria-label="Search">
    <input v-model="scommand" class="form-control mr-sm-2" type="search" placeholder="Команда" aria-label="Search">
    <button class="btn btn-outline-success my-2 my-sm-0">Найти</button>  
     <select  v-model="change" class="form-control change">
     <option  v-for="i in sport" :key="i" >{{ i }}</option>
    </select>  
  </form>
    <div class="sbut">
      <button  @click="Parse()" class="btn btn-outline-success my-2 my-sm-0">Сегодня</button> 
  </div>
    
  </div>
</nav>
<div v-bind:class="{ loader: isActive }"></div>
  <table class="tab" cellspacing="5">
      <tr>
        <td><div v-for="i in time">{{ i }}</div></td>
        <td><div v-for="i in status">{{ i }}</div></td>
        <td><div v-for="i in home_team">{{ i }}</div></td>
        <td><div v-for="i in score">{{ i }}</div></td>
        <td><div v-for="i in away_team">{{ i }}</div></td>
        <td><div v-for="i in league">{{ i }}</div></td>
      </tr>
    </table>
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
      isActive:false,
      time:"",
      status:"",
      home_team:"",
      away_team:"",
      score:"",
      league:"",
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
      this.time="";
      this.status="";
      this.home_team="";
      this.away_team="";
      this.score="";
      this.league="";
      axios.post('http://localhost:5000/today',{"sport":this.change})
      .then(res=>{
        this.isActive = false
        this.Act = true
        this.time = res.data.start_time
        this.status = res.data.game_status
        this.home_team = res.data.home_team
        this.away_team = res.data.away_team
        this.score = res.data.score
        this.league = res.data.league
        console.log(typeof res.data)
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
  /* margin-left: 25%; */
  color: azure;
}
.butt{
  margin-left: -680px;
   margin-bot:20px;
}
.tab{
  margin:auto;
}
.change{
  margin-right:700px;
  margin-top:30px;
  
}
.today{
  margin-top:2000px;
}
.sbut{
  margin-left:150px;
  margin-top:-37px;
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
