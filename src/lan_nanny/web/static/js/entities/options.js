/*
  Lan Nanny Web
  Entities 
  Options

*/
import { API_URL } from "/config.js";
import * as main from "/static/js/main.js";



export function get_options(){
  /* Get recent bookmarks */
  $.ajax({
    type: "GET",
    url: API_URL + "/options",
    // url: API_URL + "/bookmarks?limit=1",
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
