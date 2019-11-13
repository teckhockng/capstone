// for plotting graph
google.charts.load('current', {'packages':['line']});
google.charts.setOnLoadCallback(drawChart);

var tableData = [[0, 50, 50]]
function drawChart() {
  var data = new google.visualization.DataTable();
  data.addColumn('number', 'Minutes Played');
  data.addColumn('number', '{{ home }} Win Probability');
  data.addColumn('number', '{{ visitor }} Win Probability');
  data.addRows(
    tableData
  );
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
  var url = '/get_predictions/{{game_id}}';
  var xhReq = new XMLHttpRequest();
  xhReq.open("GET", url, false);
  xhReq.send(null);
  var json_data = JSON.parse(xhReq.responseText);

  if(json_data[0][0].toString().includes("ET")){
    document.getElementById("game_status").innerHTML = "Game Time: " + json_data[0][0].toString();
    document.getElementById("home_win_percentage").innerHTML = "{{home}}" + " Win Percentage: 50%";
    document.getElementById("visitor_win_percentage").innerHTML = "{{visitor}}" + " Win Percentage: 50%";
  }else{
    document.getElementById("game_status").innerHTML = "Game Status: " + json_data[0][0].toString();
    document.getElementById("home_win_percentage").innerHTML = "{{home}}" + " Win Percentage: " + json_data[0][7].toString() + "%";
    document.getElementById("visitor_win_percentage").innerHTML = "{{visitor}}" + " Win Percentage: " + json_data[0][8].toString() +"%";
  };

  if(json_data[0][1] == null){
    document.getElementById("game_time").style.display = "none";
  }else{
    document.getElementById("game_time").innerHTML = "Time Remaining: " + json_data[0][1].toString();
  };

  document.getElementById("game_score").innerHTML = "Score: " + json_data[0][2].toString() + " - " + json_data[0][3].toString();
  if (json_data[0][1].toString().includes("out")){
    tableData.push([])
  }else{
    tableData.push([ json_data[0][6], json_data[0][7], json_data[0][8]])
  };
  setTimeout(drawChart, 10000);

};
