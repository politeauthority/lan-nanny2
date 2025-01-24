/*
  Lan Nanny Web
  Entities 
  Options

*/
import { API_URL } from "/config.js";
import * as main from "/static/js/main.js";



export function get_collection(collection_name){
  /* Get a collection of entities */
  console.log("fetching: " + collection_name);
  var return_first = function () {
    var response = null;
    $.ajax({
      type: "GET",
      url: API_URL + "/" + collection_name,
      headers: {
          "Token": main.get_cookie("Token"),
          "Content-Type": "application/json"
      },
      dataType: "json",
      success: function(data){
        response = data;
        // var next_page = Number(data.info["current_page"]) + 1;
        // $("#recent-load-more").attr("data-next-page", next_page);
      }
    });
    return response
  }();
  return return_first;
}


export function get_data(collection_name) {
  return new Promise((resolve, reject) => {
      $.ajax({
          url: API_URL + "/" + collection_name,
          method: 'GET',
          dataType: 'json',
          headers: {
            "Token": main.get_cookie("Token"),
            "Content-Type": "application/json"
        },
        dataType: "json",
          success: function(data) {
              resolve(data);  // Resolve the promise with the received data
          },
          error: function(xhr, status, error) {
              reject(error);  // Reject the promise with the error
          }
      });
  });
}