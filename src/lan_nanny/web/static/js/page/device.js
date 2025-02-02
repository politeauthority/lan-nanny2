/*
  Lan Nanny Web
  Page
  Device

*/

import * as generic from "/static/js/entities/generic.js";
import * as main from "/static/js/main.js";
import * as device from "/static/js/entities/device.js";
import * as device_mac from "/static/js/entities/device_mac.js";


function initial_device(data){
  /* Initial load of Device page */
  console.log("DEVICE DATA");
  console.log(data);
  $(".device-id").text(data.object.id);
  $(".device-name").text(data.object.name);
  $(".device-ip").text(data.object.ip);
  $(".device-created-ts").text(main.human_time(data.object.created_ts));
  $(".device-created-ts").attr("href", "/device/" + data.object.id);
  $(".device-updated-ts").text(main.human_time(data.object.updated_ts));
  $(".device-first-seen").text(main.time_since(data.object.first_seen));
  $(".device-last-seen").text(main.time_since(data.object.last_seen));
  if(data.object.last_port_scan){
    $(".device-last-port-scan").text(main.time_since(data.object.last_port_scan));
  }
  if(data.object.device_macs.length > 0){
    initial_device_macs(data.object.device_macs);
  }
}


function initial_device_macs(device_macs){
    $("#device-macs").show();
    console.log("We got device macs");
    console.log(device_macs);
    var the_copy = null;
    device_macs.forEach(dm => {
      the_copy = $('#device-mac-list li:first').clone();
      the_copy.find(".device-mac-address").text(dm.address);
      the_copy.find(".device-mac-url").attr("href", "/device-mac/" + dm.id);
      the_copy.removeClass("hide");
      $("#device-mac-list").append(the_copy);
    });
}

function modal_device_delete(device_id){
    device.delete_device(device_id);

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

    $( "#modal-device-delete-submit" ).on( "click", function() {
        modal_device_delete(device_id);
    });

});
