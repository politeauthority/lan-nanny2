/*
  Bookmarky Web Simple
  Modal Directory

*/
import { API_URL } from "/config.js";
import * as main from "/static/js/main.js";

/* Directory Add */
function modal_directory_add(){
    /* Setup the add Directory modal form */
    console.log("Adding a Direcotry");
    var the_dirs = JSON.parse(localStorage.getItem("directories"));
    console.log(the_dirs);
}

function add_directory(){
  var payload = {
    name: $("#modal-dir-add-name").val(),
  }
  var data = JSON.stringify(payload);
  $.ajax({
    type: "POST",
    url: API_URL + "/directory",
    headers: {
        "Token":main.get_cookie("Token"),
        "Content-Type": "application/json"
    },
    data: data,
    success: add_directory_success,
    dataType: "json"
    });

}

function add_directory_success(){
  $('#modal-directory-add').modal("hide");
  $("#bookmark_title").val("");
  $("#bookmark_url").val("");
  main.notify("Folder added successfully");
}


$(document).ready(function(){
  // Moodal Directory Add
  $("#modal-directory-add-submit").click(function(){
    add_directory();
  });

//   $("#modal-directory-add").click(function(){
//     modal_directory_add();
//   })

});

