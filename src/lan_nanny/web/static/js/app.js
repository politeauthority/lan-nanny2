/*
  Lan Nanny Web
  App

*/
import { API_URL } from "/config.js";
import * as main from "/static/js/main.js";

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


$(document).ready(function(){
  get_whoami()

  $("#nav-logout").click( function(){
    handle_logout()
  });

});
