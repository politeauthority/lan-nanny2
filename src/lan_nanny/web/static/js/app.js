/*
  Lan Nanny Web
  App

*/
import { API_URL } from "/config.js";
import * as main from "/static/js/main.js";
import * as device from "/static/js/entities/device.js";
import * as generic from "/static/js/entities/generic.js";
import * as vendors from "/static/js/entities/vendors.js";


export function initial_web_app_load(){
  /* Initial Web App Load
  */
  console.log("Running initiail web app load");
  vendors.get_vendors();
  return true;
}

function handle_logout(){
  /* Tasks to run when we've hit the logout button */
  console.log("we are logging out");
  delete_cookie("Token");
  location.href = '/';
}


function handle_session_messages(){
  /* Handle session messages. */
  if(sessionStorage.getItem("alert_displayed") === false){
    console.log("We have a session message to display");
  } else {
    // console.log("No session notifications to handle");
  }
}


function get_whoami(){
  /* Get User and environment details */
  const token = main.get_cookie("Token");
  $.ajax({
      type: "GET",
      url: API_URL + "/who-am-i",
      headers: {
          "Token": token,
          "Content-Type": "application/json"
      },
      success: success_who_am_i,
      // error: handle_logout,
      dataType: "json"
  });
}


function success_who_am_i(){
  // console.log("We're logged in");
}

function modal_device_add_submit(){
  var device_name = $("#modal_device_add_name").val();
  device.post_device(device_name);
  $("#modal-device-add").modal("hide");
}


$(document).ready(function(){
  console.log("HERES THE APP");
  $("#modal-device-add-submit").click(function(){
    modal_device_add_submit();
    console.log("clicked submit")
  });

});
