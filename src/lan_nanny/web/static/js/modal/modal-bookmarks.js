/*
  Bookmarky Web Simple
  Modal Bookmarks

*/
import { API_URL } from "/config.js";
// import * as bookmarks from "/static/js/entities/bookmarks.js";
import * as main from "/static/js/main.js";


function modal_bookmark_edit_prepare(bookmark_id){
  /* This populates the information for the edit Bookmark modal. To prep values for
  modal_bookmark_edit_submit
  */
  console.log("Prepping modal for Bookmark ID: " + bookmark_id);
  var bookmark = bookmarks.get_bookmark_by_id(bookmark_id);
  console.log(bookmark);
  console.log("BOOKMARK: " + bookmark.hidden);

  $("#modal_bookmark_edit_title").val(bookmark.title);
  $("#modal_bookmark_edit_url").val(bookmark.url);
  // $("#modal-bookmark-edit-notes").html("");
  $("#modal-bookmark-edit-notes").val(bookmark.notes);
  $("#modal-bookmark-edit-submit-save").attr("data-bookmark-id", bookmark_id);

  // Handle Directories
  // @todo: When we get to Nested directories this has to be done better!
  var the_dirs = JSON.parse(localStorage.getItem("directories"));
  // @todo - Dont include tags that have already been tagged
  the_dirs["objects"].forEach( dir => {
    $("#modal-bookmark-edit-dir-select").append('<option value="' + dir.id + '">' + dir.name + '</option>');
  });

  // Handle Tags
  var the_tags = JSON.parse(localStorage.getItem("tags"));
  // @todo - Dont include tags that have already been tagged
  the_tags["objects"].forEach( tag => {
    $("#modal-bookmark-edit-tag-add-select").append('<option value="' + tag.id + '">' + tag.name + '</option>');
  });
  if(bookmark.tags){
    bookmark.tags.forEach( tag => {
      $("#modal-bookmark-edit-tag-remove-select").append('<option value="' + tag.id + '">' + tag.name + '</option>');
    });
  } else {
    $("#modal-bookmark-edit-tag-remove-select-form-box").hide();
  }

  if( bookmark.hidden === false){
    console.log("Bookmark is hidden");
  } else {
    $("#modal-bookmark-edit-hidden").attr("checked", "checked");
  }
  console.log("BOOKMARK HIDE: "  + bookmark.hidden);
  

}


/* Bookmark Modal Edit */
function bookmark_favorite_click(){
  // Handle the favorited button on the modal being clicked
  if ($("#modal-bookmark-favorite").hasClass("bi-star")){
    $("#modal-bookmark-favorite").addClass("bookmark-fav");
    $("#modal-bookmark-favorite").addClass("bi-star-fill");
    $("#modal-bookmark-favorite").removeClass("bi-star");
  } else {
    $("#modal-bookmark-favorite").removeClass("bookmark-fav");
    $("#modal-bookmark-favorite").removeClass("bi-star-fill");
    $("#modal-bookmark-favorite").addClass("bi-star");
  }
  return true;
}


function modal_bookmark_edit_submit(bookmark_id){
  /* Method to send edited Bookmark to the api. Triggers when the Bookmark Edit modal save button
  is hit.
  */
  console.log("Saving Bookmark");
  var payload = {
    title: $("#modal_bookmark_edit_title").val(),
    url: $("#modal_bookmark_edit_url").val(),
    notes: $("#modal-bookmark-edit-notes").val(),
    hidden: false,
    metas: {},
  }

  if($("#modal-bookmark-favorite").hasClass("bi-star")){
    payload["metas"]["favorite"] = false;
  } else {
    payload["metas"]["favorite"] = true;
  }

  // Handle Directory
  var dir_id = $("#modal-bookmark-edit-dir-select option:selected").val();
  console.log("Adding bookmark to dir: " + dir_id);
  if(dir_id){
    payload.directory_id = dir_id;
  }

  // Handle Tag
  var tag_id = $("#modal-bookmark-edit-tag-add-select option:selected").val();
  var tag_add = false;
  if(tag_id){
    tag_add = true;
    payload.tag_id = tag_id;
  }
  var tag_id_remove = $("#modal-bookmark-edit-tag-remove-select").val();
  if(tag_id_remove){
    payload.tag_id_remove = tag_id_remove;
  }
  if($("#modal-bookmark-favorite").hasClass("bi-star-fill")){
    // console.log("It has a star yooo.");
    // console.log($("#modal-bookmark-favorite").hasClass("bi-star-fill"));
    payload.metas["favorite"] = true;

  }
  var bookmark_hidden = $("#modal-bookmark-edit-hidden").is(':checked');
  if(bookmark_hidden == true){
    bookmark_hidden = true;
  } else {
    bookmark_hidden = false;
  }
  payload["hidden"] = bookmark_hidden;
  
  console.log("SENDING PAYLOAD: ");
  console.log(payload);
  console.log("Tag Add: " + tag_add);
  payload = JSON.stringify(payload);
  $.ajax({
    type: "POST",
    url: API_URL + "/bookmark/" + bookmark_id,
    headers: {
        "Token": main.get_cookie("Token"),
        "Content-Type": "application/json"
    },
    data: payload,
    success: modal_bookmark_edit_success(tag_add),
    dataType: "json"
  });
}


function modal_bookmark_edit_success(data, tag_add){
  /* Handle a successful edit.*/
  $("#modal-bookmark-edit").modal("hide");
  main.notify("Edited bookmark successfully.");
  console.log(data);
  console.log(tag_add);
  // console.log("Editing Bookmark: " + data.)
}


function modal_bookmark_edit_delete_submit(bookmark_id){
  /* Once the Delete Bookmark button is hit from the modal window, run the delete operation on the
  api. Then remove the link from the DOM.
  @todo: Setup an error handler
  */
  $.ajax({
    type: "DELETE",
    url: API_URL + "/bookmark/" + bookmark_id,
    headers: {
        "Token": main.get_cookie("Token"),
        "Content-Type": "application/json"
    },
    success: function(){
        console.log("Here we go");
        bookmark_delete_success(bookmark_id)

    },
    dataType: "json"
    });
}


function bookmark_delete_success(bookmark_id){
  $('#bookmarks_recent li').each(function() {
    var data_id = $(this)[0].dataset.bookmarkId
    if (data_id === bookmark_id) {
        $(this).hide();
    }
  });
  $("#modal-bookmark-edit").modal("hide");
  main.notify("Deleted bookmark successfully!", "success");
}


/* Bookmarks Add */
function add_bookmark(){
  // Add a Bookmark via a modal.
  var title = $("#bookmark_title").val();
  var url = $("#bookmark_url").val();
  var data = JSON.stringify({title: title, url: url});
  $.ajax({
    type: "POST",
    url: API_URL + "/bookmark",
    headers: {
        "Token": main.get_cookie("Token"),
        "Content-Type": "application/json"
    },
    data: data,
    success: add_bookmark_success,
    dataType: "json"
    });

  $('#add_bookmark_modal').modal('hide')
}

function add_bookmark_success(){
  $("#bookmark_title").val("");
  $("#bookmark_url").val("");
  bookmarks.get_boomarks_recent();
}


$(document).ready(function(){
  $("#modal-bookmark-add-submit-save").click(function(){});

  // Moodal Bookmark Add
  $("#modal-bookmark-add-submit").click(function(){
    add_bookmark();
  });

  // Modal Bookmark Edit - Drop down menu button
  $(document).on("click", ".bookmark-edit-btn", function(){
    var bookmark_id = $(this).closest(".a-bookmark")[0].dataset.bookmarkId;
    modal_bookmark_edit_prepare(bookmark_id);
  });

  $("#modal-bookmark-favorite").click(function(){
    bookmark_favorite_click();
  });

  $("#modal-bookmark-edit-submit-save").click(function(){
    var bookmark_id = $(this).attr("data-bookmark-id");
    console.log("Edit Modal button clicked" + bookmark_id);
    modal_bookmark_edit_submit(bookmark_id);
  })

  $("#modal-bookmark-edit-submit-delete").click(function(){
    var bookmark_id = $("#modal-bookmark-edit-submit-save").attr("data-bookmark-id");
    modal_bookmark_edit_delete_submit(bookmark_id);
  });

});

