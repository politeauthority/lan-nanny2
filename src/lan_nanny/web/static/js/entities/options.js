/*
  Lan Nanny Web
  Entities 
  Options

*/
import { API_URL } from "/config.js";
import * as main from "/static/js/main.js";


export function save_option(option_name, option_value){
  var payload = {
    "value": option_value
  }
  payload = JSON.stringify(payload);
  $.ajax({
    type: "POST",
    url: API_URL + "/option/" + option_name,
    headers: {
        "Token": main.get_cookie("Token"),
        "Content-Type": "application/json"
    },
    dataType: "json",
    data: payload,
    success: function(){
      console.log("saved Option succesffully");
    },
  });
}


export function get_options(){
  /* Get recent bookmarks */
  $.ajax({
    type: "GET",
    url: API_URL + "/options",
    headers: {
        "Token": main.get_cookie("Token"),
        "Content-Type": "application/json"
    },
    success: function(){
      console.log("Successfully got options")
      // var next_page = Number(data.info["current_page"]) + 1;
      // $("#recent-load-more").attr("data-next-page", next_page);

    },
    dataType: "json"
    });
    return data
}
