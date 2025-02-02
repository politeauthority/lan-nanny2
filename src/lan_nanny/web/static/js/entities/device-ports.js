/*
  Lan Nanny Web
  JS Entity
  Device Ports

*/
import { API_URL } from "/config.js";
import * as main from "/static/js/main.js";


export function get_device_ports(search_id, device_type){
    /* Get a collection of Device Ports for either a Device or a DeviceMac */
    console.log("Getting device ports")
    var payload = {}
    if(device_type == "device-mac"){
        payload["device_mac_id"] = search_id
    } else {
        payload["device_id"] = search_id
    }
    $.ajax({
        type: "GET",
        url: API_URL + "/device-ports",
        headers: {
            "Token": main.get_cookie("Token"),
            "Content-Type": "application/json"
        },
        dataType: "json",
        data: payload,
        success: function(data){
            console.log("Got Device Ports");
            console.log(data);
        },
        error: function(data){
            console.log("Failed to get Device Ports");
        }
      });
}
