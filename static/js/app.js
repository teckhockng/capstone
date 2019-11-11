function update_data(){
 var url = '/get_data';
 var xhReq = new XMLHttpRequest();
 xhReq.open("GET", url, false);
 xhReq.send(null);
 var data = JSON.parse(xhReq.responseText);
 console.log(data);

 for (i = 0; i < data.length; i++){
   if(data[i][0].toString().includes("ET")){
     document.getElementById("game_status_"+i.toString()).innerHTML = "Game Time: " + data[i][0].toString();
   }else{
     document.getElementById("game_status_"+i.toString()).innerHTML = "Game Status: " + data[i][0].toString();
   };

   if(data[i][2] == null){
     document.getElementById("game_time_"+i.toString()).style.display = "none"
   }else{
     document.getElementById("game_time_"+i.toString()).innerHTML = "Time Remaining: " + data[i][2];
   };

   document.getElementById("game_score_"+i.toString()).innerHTML = "Score: " + data[i][3].toString() + " - " + data[i][4].toString();
 }
 setTimeout(update_data, 10000);
  };

 update_data();
