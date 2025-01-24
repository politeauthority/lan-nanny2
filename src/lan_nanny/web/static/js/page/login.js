/*
  Bookmarky Simple
  Login

*/
import { API_URL } from "/config.js";
import * as main from "/static/js/main.js";

function web_login(){
    console.log("Starting");
    client_id = $("#client_id").val();
    api_key = $("#api_key").val();
    fetch_new_token(client_id, api_key, API_URL);
}


function fetch_new_token(client_id, api_key){
    window.localStorage.setItem('API_URL', API_URL);
    $.ajax({
      type: "POST",
      url: API_URL + "/auth",
      headers: {
          "X-Api-Key": api_key,
          "Client-Id": client_id,
          "Content-Type": "application/json"
      },
      success: succes_login,
      error: error_login,
      dataType: "json"
    });
}


function succes_login(data){
    console.log("successful login");
    main.set_cookie("Token", String(data.token), 10);
    // localStorage.setItem('jwt', String(data.token));
    console.log("setting API_URL");
    console.log(data.token);
    location.href = '/dashboard';
}

function error_login(){
  console.log("Error logging in");
  $("#login-form").show();
  $("#login-loading").hide();
  notify("Invalid login", "error")
}

function check_if_were_loggied_in(){
  console.log("checking if we're logged in");
  // let token = window.localStorage.getItem('token')
  // if (token){
  //     see_if_token_still_good(token);
  // } else {
  //     console.log("token expired don't continue");
  // }
  // console.log(token);
}
  


function token_still_valid(){
    console.log("token is still good!");
    // location.href = "/bookmarks";
}

function notify(message, type="success"){
    /* Create a notification message to the user.
    */
    if(type == "success"){
        $("#notify").addClass("alert-success");
    } else if(type == "error"){
        $("#notify").addClass("alert-danger");
    }
    $("#notify").text(message);
    $("#notify").slideDown(500, function(){
      $(this).delay(2000);
      $("#notify").slideUp(1000);
    });
}

function check_if_logged_in(){
  /*If we have a Token cookie, lets see if we're logged in. */
  console.log("Checking if we're logged in")
  $.ajax({
    url:  API_URL + "/who-am-i",
    method: 'GET',
    headers: {
      "Token": main.get_cookie("Token"),
      "Content-Type": "application/json"
    },
    success: function(data, textStatus, jqXHR) {
      if (jqXHR.status === 200) {
        location.href = '/bookmarks';
      }
    },
    error: function(jqXHR, textStatus, errorThrown) {
      console.log("Token is no longer valid for login: " + jqXHR.status);
    }
  });
}


$(document).ready(function(){
  if(main.get_cookie("Token")){
    check_if_logged_in();
  }
  $("#login_submit").off("click").on("click", function(event) {
    event.preventDefault();
    $("#login-form").hide();
    $("#login-loading").fadeIn();
    web_login();
  });
});
