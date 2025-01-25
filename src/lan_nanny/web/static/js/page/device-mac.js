/*
  Lan Nanny Web
  Page
  Device Mac

*/

import * as generic from "/static/js/entities/generic.js";
import * as main from "/static/js/main.js";
import * as device_mac from "/static/js/entities/device_mac.js";

function initial_device_mac(data){
    console.log("Hi");
    $(".device-mac-id").text(data.object.id);
    $(".device-mac-created-ts").text(main.human_time(data.object.created_ts));
    $(".device-mac-updated-ts").text(main.human_time(data.object.updated_ts));
    $(".device-mac-device-id").text(data.object.device_id);
    $(".device-mac-address").text(data.object.address);
    $(".device-mac-last-ip").text(data.object.last_ip);
    // handle_host_scan_stats(data);
    // handle_host_scans(data);
    if(data.object.device_id){
        console.log("We have a Device ID: " + data.object.device_id);
    }
}

function modal_device_mac_pair_submit(){
    const path = window.location.pathname;
    const segments = path.split('/');
    var device_mac_id = segments[segments.length - 1];
    console.log("Submitting the pair");
    var device_id = $("#modal_device_mac_device_pair_id").val()
    console.log("device id: " + device_id);
    device_mac.post_pair_device_mac_device(device_mac_id, device_mac_id)

}


$(document).ready(function(){
    const path = window.location.pathname;
    const segments = path.split('/');
    var device_mac_id = segments[segments.length - 1];

    // Handle Initial Page Load
    generic.get_data("device-mac/" + device_mac_id)
      .then(data => {
        console.log('Data received:', data);
        initial_device_mac(data);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
    });

    $( "#modal-device-mac-device-pair-submit" ).on( "click", function() {
        modal_device_mac_pair_submit();
      });

});
