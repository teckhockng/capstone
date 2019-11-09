var data = JSON.parse({{ game_data|safe }});
console.log(data)
//
// function jsonCallback(json){
//   console.log(json);
// }
//
// $.ajax({
//   url: "https://data.nba.com/data/5s/v2015/json/mobile_teams/nba/2019/scores/00_todays_scores.json",
//   dataType: "jsonp"
// });

function get_data(){
    var url = 'https://data.nba.com/data/5s/v2015/json/mobile_teams/nba/2019/scores/00_todays_scores.json';
    var xhReq = new XMLHttpRequest();
    xhReq.open("GET", url, false);
    xhReq.send(null);
    var data = JSON.parse(xhReq.responseText);
    console.log(data)

    // setTimeout(get_data, 5000)
    return data["gs"]["g"];
};

var test = get_data()
// for (i = 0; i < test.length; i++) {
//     document.getElementById("game_"+String(i)).innerHTML = test[i]["stt"];
//     console.log(test[i]["stt"]);
//     document.getElementById("game_score_"+String(i)).innerHTML = test[i]["v"]["s"] + " VS. " + test[i]["h"]["s"];
//     console.log(test[i]["v"]["s"] + " VS. " + test[i]["h"]["s"]);
// };
