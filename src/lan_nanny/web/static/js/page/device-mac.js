/*
  Lan Nanny Web
  Page
  Device Mac

*/

import * as generic from "/static/js/entities/generic.js";
import * as main from "/static/js/main.js";
import * as device_mac from "/static/js/entities/device_mac.js";

function initial_device_mac(data){
    $(".device-mac-id").text(data.object.id);
    $(".device-mac-created-ts").text(main.human_time(data.object.created_ts));
    $(".device-mac-updated-ts").text(main.human_time(data.object.updated_ts));
    $(".device-mac-device-id").text(data.object.device_id);
    $(".device-mac-address").text(data.object.address);
    $(".device-mac-last-ip").text(data.object.last_ip);
    $(".device-mac-first-seen").text(main.time_since(data.object.first_seen));
    $(".device-mac-last-seen").text(main.time_since(data.object.last_seen));
    $(".device-mac-last-port-scan").text(main.time_since(data.object.last_port_scan));
    // handle_host_scan_stats(data);
    // handle_host_scans(data);
    if(data.object.device_id){
        console.log("We have a Device ID: " + data.object.device_id);
        get_device(data.object.device_id);
    }
}

function get_device(device_id){
  /* Get a Device by it's ID and put it on the page. */
  console.log("getting device id: " + device_id)
  generic.get_data("device/" + device_id)
  .then(data => {
    console.log('Data received:', data);
    initial_device(data);
  })
  .catch(error => {
    console.error('Error fetching data:', error);
});

$( "#modal-device-mac-device-pair-submit" ).on( "click", function() {
    modal_device_mac_pair_submit();
  });

}

function initial_device(data){
  console.log("DEVICE DATA");
  console.log(data);
  $("#device-mac-device").removeClass("hide");
  $(".device-mac-device-name").text(data.object.name);
  $(".device-mac-device-page").attr("href", "/device/" + data.object.id);
}

function modal_device_mac_pair_submit(){
    const path = window.location.pathname;
    const segments = path.split('/');
    var device_mac_id = segments[segments.length - 1];
    console.log("Submitting the pair");
    var device_id = $("#modal_device_mac_device_pair_id").val()
    console.log("device id: " + device_id);
    device_mac.post_pair_device_mac_device(device_mac_id, device_id);

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
