function update_data(){
     var url = '/get_predictions/{{game_id}}';
     var xhReq = new XMLHttpRequest();
     xhReq.open("GET", url, false);
     xhReq.send(null);
     var data = JSON.parse(xhReq.responseText);
     console.log(url);
     console.log(data);

    if(data[0][0].toString().includes("ET")){
      document.getElementById("game_status").innerHTML = "Game Time: " + data[0][0].toString();
      document.getElementById("home_win_percentage").innerHTML = "{{home}}" + " Win Percetage: 50%";
      document.getElementById("visitor_win_percentage").innerHTML = "{{visitor}}" + " Win Percetage: 50%";
    }else{
      document.getElementById("game_status").innerHTML = "Game Status: " + data[0][0].toString();
      document.getElementById("home_win_percentage").innerHTML = "{{home}}" + "Win Percetage: " + data[0][7].toString();
      document.getElementById("visitor_win_percentage").innerHTML = "{{visitor}}" + "Win Percetage: 50%" + data[0][8].toString();
    };

    if(data[0][1] == null){
      document.getElementById("game_time").style.display = "none";
    }else{
      document.getElementById("game_time").innerHTML = "Time Remaining: " + data[1].toString();
    };


    document.getElementById("game_score").innerHTML = "Score: " + data[0][2].toString() + " - " + data[0][3].toString();
     // setTimeout(update_data, 10000);
};

update_data();

// for plotting graph
google.charts.load('current', {'packages':['line']});
google.charts.setOnLoadCallback(drawChart);
function drawChart() {
  var data = new google.visualization.DataTable();
  data.addColumn('string', 'Minutes Played');
  data.addColumn('number', '{{ home }} Win Probability');
  data.addColumn('number', '{{ visitor }} Win Probability');
  data.addRows([
    //in this format ["string", num, num]
    ["00:00", 0, 0]
  ]);
  var options = {
    chart: {
      title: '{{ home }} vs {{ visitor }}',
      subtitle: 'Win Probability'
    },
    width: 900,
    height: 500,
    hAxis: {
      title: 'Minutes Played',
      ticks: [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75]
    },
    vAxis: {
      title: 'Win Probability',
      ticks: [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    },
    colors: ['#a52714', '#097138']
  };
  var chart = new google.charts.Line(document.getElementById('chart_div'));
  chart.draw(data, options);
  data.addRows([["80:00", 90, 85]]);
}
