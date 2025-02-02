/*
  Lan Nanny Web
  Page
  Scans

*/

import * as generic from "/static/js/entities/generic.js";
import * as main from "/static/js/main.js";

function initial_scan_hosts(data){
    handle_host_scan_stats(data);
    handle_host_scans(data);
}


function initial_scan_ports(data){
    handle_port_scan_stats(data);
    handle_port_scans(data);
}


function handle_port_scan_stats(data){
    /* Draw all the Scan Ports*/
    $("#total-scan-ports").text(data.info.total_objects);
}


function handle_host_scan_stats(data){
    /* Draw all the Scan Hosts */
    $("#total-scan-hosts").text(data.info.total_objects);
    console.log(data.info);
}


function handle_host_scans(data){
    /* Draw all the Scan Hosts
    */
    var the_copy = null;   
    data.objects.forEach(scan => {
        // console.log(scan.created_ts);
        the_copy = $('#scan_host_roster_boiler').clone();
        the_copy.find('.scan-host-id').text(scan.id);
        the_copy.find('.scan-host-time').text(main.time_since(scan.created_ts));
        the_copy.find('.scan-hosts-found').text(scan.hosts_found);

        // console.log(the_copy.clone());
        the_copy.removeClass("hide");
        the_copy.removeAttr("id");
        $("#scan_host_roster").append(the_copy);
        // console.log(scan.created_ts);
    });
}


function handle_port_scans(data){
    /* Draw all the Scan Ports*/
    var the_copy = null;   
    data.objects.forEach(scan => {
        // console.log(scan.created_ts);
        the_copy = $("#scan_port_roster_boiler").clone();

        var port_scan_id = '<a href="/scan-port/' + scan.id + '">' + scan.id + '</a>';
        the_copy.find('.scan-port-id').html(port_scan_id);
        the_copy.find('.scan-port-time').text(main.time_since(scan.created_ts));

        if(scan.device_id){
            console.log("Device Mac ID: " + scan.device_id);
        } else {
            console.log("Device MAC ID: " + scan.device_mac_id);
            var device_mac_link = '<a href="/device-mac/' + scan.device_mac_id + '">Device Mac: ' + scan.device_mac_id + '</a>';
            the_copy.find(".scan-port-device").html(device_mac_link);
        }
        the_copy.removeClass("hide");
        the_copy.removeAttr("id");
        $("#scan_port_roster").append(the_copy);
        // console.log(scan.created_ts);
    });
}


$(document).ready(function(){
    // console.log("Starting Settings")

    // Handle Initial Page Load
    generic.get_data("scan-hosts")
      .then(data => {
        console.log('Data received:', data);
        initial_scan_hosts(data);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
    });

    generic.get_data("scan-ports")
    .then(data => {
      console.log('Data received:', data);
      initial_scan_ports(data);
      // 
    })
    .catch(error => {
      console.error('Error fetching data:', error);
  });
 	
    // $( ".option-btn" ).on( "click", function() {
    //   update_option($(this));
    // });

});
