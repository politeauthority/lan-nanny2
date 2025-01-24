/*
  Lan Nanny Web
  Page
  Settings

*/

// import { API_URL } from "/config.js";
// import * as main from "/static/js/main.js";
import * as generic from "/static/js/entities/generic.js";
// import * as tags from "/static/js/entities/tags.js";

function initial_load_options(data){
  data.objects.forEach(option => {
    // console.log(option);
    if(option.name == "scan-hosts-enabled"){
      if(option.value != true){
        set_btn_disabled("scan-hosts-enabled");

      }
    }
  });
}

function set_btn_disabled(button_name){
  var the_btn = $("#" + button_name);
  the_btn.removeClass("btn-success");
  the_btn.addClass("btn-danger");
  the_btn.text("Disabled");
}


$(document).ready(function(){
    console.log("Starting Settings")

    // Handle Initial Page Load
    generic.get_data("options")
      .then(data => {
        console.log('Data received:', data);
        initial_load_options(data)
      })
      .catch(error => {
        console.error('Error fetching data:', error);
    });

 	
    $( ".option-btn" ).on( "click", function() {
      console.log("button clicked");

    } );

});
