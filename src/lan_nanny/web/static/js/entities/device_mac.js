/*
  Lan Nanny Web
  JS Entity
  Device Mac
*/
import { API_URL } from "/config.js";
import * as main from "/static/js/main.js";


export function post_pair_device_mac_device(device_mac_id, device_id){
    var payload = {
        "device_id": device_id,
        "identified": true
      }
      payload = JSON.stringify(payload);
      $.ajax({
        type: "POST",
        url: API_URL + "/device-mac/" + device_mac_id,
        headers: {
            "Token": main.get_cookie("Token"),
            "Content-Type": "application/json"
        },
        dataType: "json",
        data: payload,
        success: function(data){
          console.log("Paired Device Mac to Device Successfully");
        },
        error: function(data){
          console.log("Failed to pair Device Mac to Device");
        }
      });
}
