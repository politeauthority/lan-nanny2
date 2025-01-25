/*
  Lan Nanny Web
  Dashboard

*/

import { API_URL } from "/config.js";
import * as main from "/static/js/main.js";
import * as device from "/static/js/entities/device.js";
// import * as tags from "/static/js/entities/tags.js";

function get_dashboard_stats(){
  console.log("Getting dashboard stats")
  $.ajax({
    type: "GET",
    url: API_URL + "/stats/dashboard",
    headers: {
        "Token": main.get_cookie("Token"),
        "Content-Type": "application/json"
    },
    dataType: "json",
    success: function(data){
      draw_dashboard_stats(data);
      console.log(data);
      // var next_page = Number(data.info["current_page"]) + 1;
      // $("#recent-load-more").attr("data-next-page", next_page);
    }
  });
}

function draw_dashboard_stats(data){
  console.log("Drawing Stats")
  $("#dashboard-stats-devices-online").text(data.stats.online.devices_online);
  $("#dashboard-stats-device-macs-online").text(data.stats.online.device_macs_online);
}



$(document).ready(function(){
    console.log("hello world");
    device.get_devices_dashboard();
    get_dashboard_stats();
});
