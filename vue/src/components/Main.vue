<template>
<div>
<nav class="navbar navbar-light bg-dark">
  <div class="head">
    <h2 class="name">{{msg}}</h2>
   <form class="form-inline">
    <input v-model="firstTeam" class="form-control mr-sm-2" type="search" placeholder="Команда" aria-label="Search">
    <input v-model="secondTeam" class="form-control mr-sm-2" type="search" placeholder="Команда" aria-label="Search">
     <select  v-model="change" class="form-control change">
     <option  v-for="i in sport" :key="i" >{{ i }}</option>
    </select>  
    <p class="excp">{{excepInfo}}</p>
  </form>
<div class="secondButton">
      <button @click="TwoTeams()" class="btn btn-outline-success my-2 my-sm-0">Найти</button>
</div>
    
<!-- <div class="sbut ">
      <button  @click="Parse()" class="btn btn-outline-success my-2 my-sm-0">Сегодня</button> 
</div> -->

</div>
</nav>
<div v-bind:class="{ loader: isActive }"></div>


<div v-bind:class="{ excel: !excelReady }">
<center><p>Скачайте файл Excel - <a v-bind:href="filename" download><img src="static/excel.png" width="50" height="50" alt=""></a></p></center>
<center><p>Скачайте архив с графиками - <a href="/downloadfile/results.zip" download><img src="static/result.png" width="50" height="50" alt=""></a></p></center>
<!-- <center><a href="#" class="button2" tabindex="0">кнопка</a></center> -->
<div class="elfib">
<a class="btnflip" href="">
		<span class="btnflip-item btnflip__front">Elliot</span>
		<span class="btnflip-item btnflip__center"></span>
		<span class="btnflip-item btnflip__back">Fibonacci</span>
</a>
</div>
</div>
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
      msg: 'Elliot Fibonacci',
      change:"",
      isActive:false,
      excelReady:false,
      time:"",
      status:"",
      home_team:"",
      away_team:"",
      firstTeam:"",
      secondTeam:"",
      filename:"",
      score:"",
      league:"",
      excepInfo:"",
      sport:[
        "Футбол",
        "Хоккей",
        // "Теннис",
        // "Баскетбол",
        // "Волейбол",
        // "Гандбол",
        // "Футзал",
        // "Бейсбол"
      ]
    }
  },
  methods:{
    Parse(){
      this.isActive = true;
      this.excelReady = false;
      this.time="";
      this.status="";
      this.home_team="";
      this.away_team="";
      this.score="";
      this.league="";
      this.excepInfo = "";

      axios.post('http://185.179.188.146:5111/today',{"sport":this.change})
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
    },
    TwoTeams(){
      this.isActive = true;
      this.excelReady = false;
      this.filename = "";
      this.excepInfo = "";
      this.time="";
      this.status="";
      this.home_team="";
      this.away_team="";
      this.score="";
      this.league="";
      this.excepInfo = "Начался поиск команд";
      axios.post("http://185.179.188.146:5111/teams",{"sport":this.change,"first":this.firstTeam,"second":this.secondTeam})
      .then(res=>{
        // console.log(res.data)
        if(res.data.info=="nice"){
          this.excepInfo = "Команды найдены.Подготавливается excel для скачивания"
          axios.post("http://185.179.188.146:5111/efw",{"sport":this.change})
          .then(res=>{
            if(res.data.info=="ok"){
                console.log("OK")
                this.isActive = false;
                if(this.change=="Футбол"){
                  this.filename = "/downloadfile/Football.xlsx"
                  this.excelReady = true;
                  // console.log(this.filename)
                  this.excepInfo =""
                }else if(this.change=="Хоккей"){
                  this.filename = "/downloadfile/Hockey.xlsx"
                  this.excelReady = true;
                  // console.log(this.filename)
                  this.excepInfo = ""
                }
            }else{
                console.log("BAD")
                this.isActive = false;
                this.excepInfo = "К сожалению что-то пошло не так"
            }
          })
        }else{
          this.isActive = false;
          this.excepInfo = "К сожалению команды не удалось найти.\n Попробуйте проверить правильность написания команд, а также выбор спорта"
        }
      })
    }
  }
}
</script>
<style>

.elfib{
  margin-left: 800px;
  margin-top: 200px;
  /* margin: auto; */
  position: fixed;
}
.excp{
  color: #5FDB5C;
}
.excel{
  visibility: hidden;
}
.excCenter{
  margin-left:800px;
  margin-top: 200px;
}
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
  margin-top:-75px;
}

.secondButton{
  /* margin-left: 500px; */
  margin-bottom: 100px;
  margin-top:-104px;
  margin-right: 200px;
  margin-left: 500px;
  /* visibility: hidden; */
  /* background-color: aquamarine; */
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


/*Fibbonacci button*/
.btnflip {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 200px;
  height: 60px;
  text-align: center;
  transform-style: preserve-3d;
  perspective: 1000px;
  transform-origin: center center;
}
.btnflip-item {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  text-align: center;
  line-height: 60px;
  font-size: 24px;
  background-color: rgba(255,255,255, .05);
  transform-style: preserve-3d;
  backface-visibility: hidden;
  border-radius: 30px;
  text-transform: uppercase;
  color: #fff;
  transition: 1s;
}
.btnflip-item.btnflip__front {
  transform: rotateX(0deg) translateZ(20px);
}
.btnflip:hover .btnflip-item.btnflip__front {
  transform: rotateX(-180deg) translateZ(20px);
}
.btnflip-item.btnflip__back {
  transform: rotateX(180deg) translateZ(20px);
}
.btnflip:hover .btnflip-item.btnflip__back {
  transform: rotateX(0deg) translateZ(20px);
}
.btnflip-item.btnflip__center {
  background: linear-gradient(to left, #c31a5b, #7129bd);
}
.btnflip-item.btnflip__center::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to left, #ffdd1f, #c31a5b);
  border-radius: 30px;
  transform: translateZ(-1px);
}
.btnflip:hover .btnflip-item.btnflip__center {
  transform: rotateX(-180deg);
}

</style>
