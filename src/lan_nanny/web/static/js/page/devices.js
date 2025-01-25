/*
  Lan Nanny Web
  Page
  Devices

*/

import * as generic from "/static/js/entities/generic.js";
import * as main from "/static/js/main.js";
import * as device_mac from "/static/js/entities/device_mac.js";


function initial_devices_macs(data){
    var the_copy = null;   
    data.objects.forEach(device_mac => {
        the_copy = $('#devices_device_mac_roster li:first').clone();
        the_copy.find('.device-device-mac-address').text(device_mac.address);
        the_copy.find('.device-device-mac-url').attr("href", "/device-mac/" + device_mac.id);
        the_copy.find('.device-device-mac-last-ip').text(device_mac.last_ip);

        the_copy.removeClass("hide");
        $("#devices_device_mac_roster").append(the_copy);
        // console.log(scan.created_ts);
    });
}


$(document).ready(function(){
    // Handle Initial Page Load
    generic.get_data("device-macs")
      .then(data => {
        console.log('Data received:', data);
        initial_devices_macs(data);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
    });

});
