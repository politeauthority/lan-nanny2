/*
  Lan Nanny Web
  Entities 
  Scans

*/
import { API_URL } from "/config.js";
import * as main from "/static/js/main.js";



export function get_devices_dashboard(){
  /* Get recent bookmarks */
  $.ajax({
    type: "GET",
    url: API_URL + "/scans",
    // url: API_URL + "/bookmarks?limit=1",
    headers: {
        "Token": main.get_cookie("Token"),
        "Content-Type": "application/json"
    },
    success: function(data){
      console.log(data);
      show_devices(data, true, "#bookmarks_recent");
      // var next_page = Number(data.info["current_page"]) + 1;
      // $("#recent-load-more").attr("data-next-page", next_page);

    },
    dataType: "json"
    });
}
