/*
  Lan Nanny Web
  Page
  Device

*/

import * as generic from "/static/js/entities/generic.js";
import * as main from "/static/js/main.js";
import * as device_mac from "/static/js/entities/device_mac.js";


function initial_device(data){
  console.log("DEVICE DATA");
  console.log(data);
  $(".device-id").text(data.object.id);
  $(".device-name").text(data.object.name);
  $(".device-ip").text(data.object.ip);
  $(".device-created-ts").text(data.object.created_ts);
  $(".device-created-ts").attr("href", "/device/" + data.object.id);
  $(".device-first-seen").text(main.time_since(data.object.first_seen));
  $(".device-last-seen").text(main.time_since(data.object.last_seen));
  if(data.object.last_port_scan){
    $(".device-last-port-scan").text(main.time_since(data.object.last_port_scan));
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
    var device_id = segments[segments.length - 1];
    console.log(device_id);

    // Handle Initial Page Load
    generic.get_data("device/" + device_id)
      .then(data => {
        console.log('Data received:', data);
        initial_device(data);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
    });

    // $( "#modal-device-mac-device-pair-submit" ).on( "click", function() {
    //     modal_device_mac_pair_submit();
    //   });

});
