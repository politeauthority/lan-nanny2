/*
  Lan Nanny Web
  Page
  Devices

*/

import * as generic from "/static/js/entities/generic.js";
import * as main from "/static/js/main.js";
import * as device_mac from "/static/js/entities/device_mac.js";
import * as vendors from "/static/js/entities/vendors.js";


function initial_devices(data){
  console.log("The Devices");
  console.log(data);
  var the_copy = null;
  data.objects.forEach(device => {
      the_copy = $('#devices_roster li:first').clone();
      the_copy.find('.device-url').attr("href", "/device/" + device.id);
      the_copy.find('.device-name').text(device.name);
      the_copy.find(".device-ip").text(device.ip);
      the_copy.find(".device-last-seen").text(main.time_since(device.last_seen));

      // the_copy.find('.device-device-mac-url').attr("href", "/device-mac/" + device_mac.id);
      // the_copy.find('.device-device-mac-last-ip').text(device_mac.last_ip);

      the_copy.removeClass("hide");
      $("#devices_roster").append(the_copy);
      // console.log(scan.created_ts);
  });
}


function initial_devices_macs(data){
    var the_copy = null;
    data.objects.forEach(device_mac => {
        the_copy = $('#devices_device_mac_roster li:first').clone();
        the_copy.find('.device-device-mac-address').text(device_mac.address);
        the_copy.find('.device-device-mac-url').attr("href", "/device-mac/" + device_mac.id);
        the_copy.find('.device-device-mac-last-ip').text(device_mac.last_ip);

        // Show the Vendor
        var show_vendor = false;
        if(device_mac.vendor_id){
          var vendor_name = vendors.get_vendor_name(device_mac.vendor_id)
          the_copy.find('.device-device-mac-vendor-name').text(vendor_name);
          show_vendor = true
        }
        if(show_vendor == false){
          the_copy.find('.device-device-mac-vendor').hide();
        }

        the_copy.removeClass("hide");
        $("#devices_device_mac_roster").append(the_copy);
        // console.log(scan.created_ts);
    });
}


$(document).ready(function(){
    // Handle Initial Page Load

    generic.get_data("devices")
      .then(data => {
        console.log('Data received:', data);
        initial_devices(data);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
    });



    generic.get_data("device-macs")
      .then(data => {
        console.log('Data received:', data);
        initial_devices_macs(data);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
    });

});
