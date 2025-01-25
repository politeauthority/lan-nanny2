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
        the_copy = $('#scan_host_roster li:first').clone();
        the_copy.find('.scan-time').text(main.time_since(scan.created_ts));
        the_copy.find('.scan-hosts-found').text(scan.hosts_found);
        // var html = '<li class="list-group-item">'+scan.created_ts+'</li>';
        // console.log(the_copy.clone());
        the_copy.removeClass("hide");
        $("#scan_host_roster").append(the_copy);
        // console.log(scan.created_ts);
    });
}


function initial_scan_ports(data){
    handle_port_scan_stats(data);
    handle_port_scans(data);
}


function handle_port_scan_stats(data){
    /* Draw all the Scan Ports*/
    $("#total-scan-ports").text(data.info.total_objects);
}


function handle_port_scans(data){
    /* Draw all the Scan Ports*/
    var the_copy = null;   
    data.objects.forEach(scan => {
        // console.log(scan.created_ts);
        the_copy = $('#scan_ports_roster li:first').clone();
        the_copy.find('.scan-time').text(main.time_since(scan.created_ts));
        the_copy.find('.scan-ports-device-mac-id').text(scan.device_mac_id);
        the_copy.find(".scan-ports-device-mac-link").attr("href", "/device-mac/" + scan.device_mac_id);
        if(scan.device_id){
            the_copy.find('.scan-ports-device-id-value').text(scan.device_id);
        } else {
            the_copy.find('.scan-ports-device-id').hide();
        }

        the_copy.find('.scan-ports-scan-type').text(scan.scan_type);
        // var html = '<li class="list-group-item">'+scan.created_ts+'</li>';
        // console.log(the_copy.clone());
        the_copy.removeClass("hide");
        $("#scan_ports_roster").append(the_copy);
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
