/*
  Bookmark Web
  Modal Tags

*/

import { API_URL } from "/config.js";
import * as main from "/static/js/main.js";
import * as tags from "/static/js/entities/tags.js";


export function modal_tag_edit_prepare(tag){
  /* Takes a Tag object and prepares the Tag edit modal. */
  console.log("Setting up modal for Tag");
  console.log(tag);
  $("#modal-tag-edit-name").val(tag.name);
  $("#modal-tag-edit-delete-submit").attr("data-tag-id", tag.id);
  $("#modal-tag-edit-submit-save").attr("data-tag-id", tag.id);
  if( tag.hidden === false){
    $("#modal-tag-edit-hidden").prop('checked', false);
  } else {
    $("#modal-tag-edit-hidden").prop('checked', true);
  }
}

export function modal_tag_edit(tag_id){
  /* Setup the edit Tag modal values */
  var tag = tags.get_tag_by_id(tag_id);
  $("#modal-tag-edit-delete-submit").attr("data-tag-id", tag.id);
  $("#modal-tag-edit-submit-save").attr("data-tag-id", tag.id);
  $("#modal-tag-edit-name").val(tag.name);
  $("#modal-tag-edit-slug").val(tag.slug);
  if( tag.hidden === false){
    $("#modal-tag-edit-hidden").prop('checked', false);
  } else {
    $("#modal-tag-edit-hidden").prop('checked', true);
  }
}

export function modal_tag_edit_delete_submit(tag_id){
  /* Once the Delete Bookmark button is hit from the modal window, run the delete operation on the
  api. Then remove the link from the DOM.
  @todo: Setup an error handler
  */
  console.log("Were gonna delete Tag ID " + tag_id);
  $.ajax({
    type: "DELETE",
    url: API_URL + "/tag/" + tag_id,
    headers: {
        "Token": main.get_cookie("Token"),
        "Content-Type": "application/json"
    },
    success: function(){
        tag_delete_success(tag_id)
    },
    dataType: "json"
    });
}

/* Add Tag */
function modal_tag_add_submit(){
  /* Subit the content from the Tag */
  var tag_name = $("#modal_tag_add_name").val();
  var data = JSON.stringify({name: tag_name});
  $.ajax({
    type: "POST",
    url: API_URL + "/tag",
    headers: {
        "Token": main.get_cookie("Token"),
        "Content-Type": "application/json"
    },
    data: data,
    success: modal_tag_add_success,
    dataType: "json"
    });
}

/* Add Tag - Success */
function modal_tag_add_success(data){
  /* Response for a successful Tag creation. */
  $("#modal-tag-add").modal("hide");
  $("#modal_tag_add_name").val("");
  main.notify("Tag created successfully!", "success");
}

/* Delete Tag */
function tag_delete_success(tag_id){
  // $('#bookmarks_recent li').each(function() {
  //   var data_id = $(this)[0].dataset.bookmarkId
  //   if (data_id === bookmark_id) {
  //       $(this).hide();
  //   }
  // });
  $("#modal-tag-edit").modal("hide");
  main.notify("Deleted Tag successfully!", "success");
}

/* Edit Tag */
function modal_tag_edit_submit(tag_id){
  /* Method to send edited Tag to the api. Triggers when the Tag Edit modal save button
  is hit.
  */
  var payload = {
    name: $("#modal-tag-edit-name").val(),
    hidden: false
  }
  var tag_hidden = $("#modal-bookmark-edit-hidden").is(':checked');
  if(tag_hidden == true){
    tag_hidden = true;
  } else {
    tag_hidden = false;
  }
  payload["hidden"] = tag_hidden;
  
  payload = JSON.stringify(payload);
  $.ajax({
    type: "POST",
    url: API_URL + "/tag/" + tag_id,
    headers: {
        "Token": main.get_cookie("Token"),
        "Content-Type": "application/json"
    },
    data: payload,
    success: modal_tag_edit_success,
    dataType: "json"
  });
}

function modal_tag_edit_success(){
  $("#modal-tag-edit").modal("hide");
  main.notify("Edited tag successfully!", "success");
}


/* Move this to Modal Tag */
function modal_tag_delete_success(){
  $("#modal-tag-edit").modal("hide");
  main.notify("Deleted tag successfully!", "success");
}

function modal_tag_add_auto_feature_submit(){
  /* Submit the modal Tag Auto Feature Form */
  var tag_name = $("#modal_tag_add_name").val();
  var data = JSON.stringify(
    {
      entity_type: "tags",
      entity_id: $("#modal-tag-auto-feature-add-tag-id").val(),
      auto_feature_value: $("#modal-tag-auto-feature-add-value").val(),
      auto_feature_type: $("#modal-tag-auto-feature-add-select-type").val()
    }
  );
  $.ajax({
    type: "POST",
    url: API_URL + "/auto-feature",
    headers: {
        "Token": main.get_cookie("Token"),
        "Content-Type": "application/json"
    },
    data: data,
    success: function(data){
      main.notify("Tag auto feature created successfully!", "success");
      // @todo: Append the newly created Tag Auto Feature to the Auto Feature's table on the page
    },
    error: function(data){
      main.notify("Failed to add Tag Auto Feature", "error");
      // @todo: Append the newly created Tag Auto Feature to the Auto Feature's table on the page
    },
    dataType: "json"
    });
}


$(document).ready(function(){
    // Tag Create
    $("#modal_tag_add_submit").click( function(){
      modal_tag_add_submit();
    });

    $("#modal_tag_add_name").on( "keypress", function(event) {
      if(event.which == 13){
        modal_tag_add_submit();
      }
    });

    $(document).on("click", "#modal-tag-edit-submit-save", function(){
      var tag_id = $("#modal-tag-edit-submit-save").attr("data-tag-id");
      modal_tag_edit_submit(tag_id);
    });
    $(document).on("click", "#modal-tag-edit-delete-submit", function(){
      var tag_id = $("#modal-tag-edit-delete-submit").attr("data-tag-id");
      modal_tag_edit_delete_submit(tag_id);
    });

    $("#modal-tag-auto-feature-submit").click( function(){
      modal_tag_add_auto_feature_submit();
    });
    

});
