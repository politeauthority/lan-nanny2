/*
  Lan Nanny Web
  Page
  Settings

*/

import * as generic from "/static/js/entities/generic.js";
import * as options from "/static/js/entities/options.js";

function initial_load_options(data){
  data.objects.forEach(option => {
    // console.log(option);
    if(option.name == "scan-hosts-enabled"){
      if(option.value != true){
        set_btn_disabled("scan-hosts-enabled");
      } else {
        set_btn_enabled("scan-hosts-enabled");
      }
    } else if (option.name == "scan-ports-enabled"){
      console.log("WE got scan ports");
      if(option.value != true){
        set_btn_disabled("scan-ports-enabled");
      } else {
        set_btn_enabled("scan-ports-enabled");
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

function set_btn_enabled(button_name){
  var the_btn = $("#" + button_name);
  the_btn.removeClass("btn-danger");
  the_btn.addClass("btn-success");
  the_btn.text("Enabled");
}

function update_option(the_btn){
  console.log("button clicked");
  var option_name = the_btn.attr("id");
  var the_value = "";
  if(the_btn.hasClass("btn-danger")){
    console.log("Turn it True");
    the_value = true;
    set_btn_enabled(option_name);
  } else {
    console.log("Turn it false");
    the_value = false;
    set_btn_disabled(option_name);
  }
  options.save_option(option_name, the_value);
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
      update_option($(this));
    });

});
