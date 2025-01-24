/*
  Bookmarky Web Simple
  Bookmarks
  Opperations for handling Bookmark entities.

*/
import { API_URL } from "/config.js";
import * as main from "/static/js/main.js";


let BOOKMARKS = {}

export function get_bookmark_by_id(bookmark_id, from_api=false){
  /* Get a Bookmark by ID from memory or local storage, which ever method is working better at the
  time.
  */
  if(from_api === true){
    $.ajax({
      type: "GET",
      url: API_URL + "/bookmark/" + bookmark_id,
      headers: {
          "Token": main.get_cookie("Token"),
          "Content-Type": "application/json"
      },
      success: function(data){
      },
      dataType: "json"
      });
  } else {

    var the_bookmark = BOOKMARKS[bookmark_id];
    return the_bookmark;
  }

}

export function get_devices_dashboard(){
  /* Get recent bookmarks */
  $.ajax({
    type: "GET",
    url: API_URL + "/devices",
    // url: API_URL + "/bookmarks?limit=1",
    headers: {
        "Token": main.get_cookie("Token"),
        "Content-Type": "application/json"
    },
    success: function(data){
      console.log(data);
      show_devices(data, true, "#bookmarks_recent");
      // var next_page = Number(data.info["current_page"]) + 1;
      // $("#recent-load-more").attr("data-next-page", next_page);

    },
    dataType: "json"
    });
}

export function show_devices(data, append_top, the_list){
  /* Add bookmarks to the DOM, appending to the list provided. */
  /* Show recent Bookmarks on page load*/
  // console.log("Recent bookmarks show");
  // console.log(data.info.total_objects);
  data.objects.forEach( item => {
    var html = '<li class="list-group-item">'+ item.name  +'</li>'
    $("#device_roster").append(html);

    console.log(item);
  });
  

  // // If we have a bookmarks-total span lets update it with the info
  // $("#bookmarks-total").html(data.info.total_objects);
  // store_bookmarks(data); 
  // // console.log("Showing bookmarks, append: " + append_top);
  // const reversed_bookmarks = data.objects.reverse();
  // reversed_bookmarks.forEach( item => {
  //   add_bookmark_to_dom(item, append_top, the_list);
  // });
  // // recent_bookmarks_load_more(data.info);
  // $(".loading-spinner").hide();
}

export function add_bookmark_to_dom(bookmark_obj, append_top, the_list){
  /* Add a single Bookmark to the DOM. Appending it to the UL list given to us
  :param: bookmark_obj - The bookmark data that we're adding.
  :param: append_top (bool) - Append the bookmark data to the top of the list or bottom.
  :param: the_list (str) - Which list we're adding the Bookmark data to.
  */
  var $bookmark = $('.boiler_item').clone().removeClass('boiler_item').show();
  $bookmark.removeClass("boiler_item");
  $bookmark.find(".bookmark-title").text(main.truncate(bookmark_obj.title));
  $bookmark.find(".bookmark-url").text(main.truncate(bookmark_obj.url));
  $bookmark.find(".bookmark-url").attr("href", bookmark_obj.url);
  $bookmark.attr("data-bookmark-id", bookmark_obj.id);
  $bookmark.attr("data-bookmark-url", bookmark_obj.url);
  $bookmark.attr("data-bookmark-title", bookmark_obj.title);
  $bookmark.find(".bookmark-created-ts").text(main.human_time(bookmark_obj.created_ts));
  $bookmark.find("ul.dropdown-menu li:first a").attr("href", "/bookmark/" + bookmark_obj.id);
  add_bookmark_dir_to_dom($bookmark, bookmark_obj);
  $bookmark.find(".bookmark-notes").text(bookmark_obj.notes);
  // console.log("Showing bookmarks " + bookmark_obj.title + " bookmark.obj " + bookmark_obj.hidden)
  if( bookmark_obj.hidden == false){
    $bookmark.find(".bookmark-hidden").hide();
  }

  add_bookmark_tags_to_dom($bookmark, bookmark_obj);

  if(append_top){
    $(the_list).prepend( $bookmark );
  } else {
    $(the_list).append( $bookmark );
  }
}

export function click_track(bookmark_id){
  /* When a Bookmark link is clicked, open the Bookmark in a new tab, and send a request to the Api
  so that we can track the request.
  */
  console.log("Tracking Bookmark ID: " + bookmark_id);
  $.ajax({
    type: "POST",
    url: API_URL + "/bookmark/click-track/" + bookmark_id,
    headers: {
        "Token": main.get_cookie("Token"),
        "Content-Type": "application/json"
    },
    dataType: "json"
    });
}

function add_bookmark_tags_to_dom($bookmark, bookmark_obj){
  /* Handle adding a Bookmark's Tags to the DOM, associated with it's Bookmark */
  if(bookmark_obj.tags){
    bookmark_obj.tags.forEach( tag => {
      add_tag_to_do_shitty_way($bookmark, tag);
    });
  }
}

function add_tag_to_do_shitty_way($bookmark, tag){
  /* This way works, but I dont like it. It feels clumsy to write html this way, and harder to 
  update IMO.
  */
  var tag_html = '<li class="bookmark-tag list-group-item float-left">';
  tag_html += '<button type="button" class="btn btn-primary btn-sm">';
  tag_html += '<i class="bi bi-tag-fill btn-sm margin-5"></i>';
  tag_html += '<a class="bookmark-tag-text" href="/tag/' + tag.slug + '">' + tag.name + '</a>';
  tag_html += '</button>';
  tag_html += '</li>';
  $bookmark.find(".bookmark-tags").append(tag_html);
}

// function add_tag_to_do_better_way(){
//   /* This way doesnt work and adds extra tags to the dom, but it would be a better way to do it if
//   I can make it work.
//   */
//   var tag_boiler = $bookmark.find(".bookmark-tag-boiler").clone();
//   var tag_boiler = $bookmark.find(".bookmark-tag-boiler").clone().appendTo(".bookmark-tags");
//   $bookmark.find( ".bookmark-tags" ).prepend(tag_boiler);
//   var new_tag = $bookmark.find("ul.bookmark-tags li:first");
//   new_tag.removeClass(".bookmark-tag-boiler");
//   new_tag.css("display", "block");
//   new_tag.find(".bookmark-tag-text").text(tag.name);
//   new_tag.find(".bookmark-tag-text").attr("href", "/tag/" + tag.slug);
//   new_tag.find(".bookmark-tag-text").attr("href", "/tag/" + tag.slug);
// }

function add_bookmark_dir_to_dom($bookmark, bookmark_obj){
  var bookmark_dir = $bookmark.find(".bookmark_directory");
  if(bookmark_obj.directory_id){
    $bookmark.find(".bookmark_directory").show();
    var the_dir = directories.get_dir_from_storage(bookmark_obj.directory_id);
    console.log("We got a Dir baby!");
    console.log(the_dir);
    // @todo: Figure out why we dont have directories
    bookmark_dir.find(".bookmark-dir-text").attr("href", "/folder/" + the_dir.slug);
    bookmark_dir.find(".bookmark-dir-text").text(the_dir.name);
  } else {
    bookmark_dir.hide();
  }
}

function store_bookmarks(data){
  /* Store Bookmarks into local storage */
  let the_bookmarks = JSON.parse(localStorage.getItem("bookmarks"));
  if (! the_bookmarks){
    the_bookmarks = {};
  }
  if (data) {
    data.objects.forEach( bookmark => {
      the_bookmarks[bookmark.id] = {
        id: bookmark.id,
        title: bookmark.title,
        url: bookmark.url,
        created_ts: bookmark.created_ts,
        updated_ts: bookmark.updated_ts,
        tags: bookmark.tags,
        hidden: bookmark.hidden,
      }
    });
  }
  BOOKMARKS = the_bookmarks;
  localStorage.setItem("bookmarks", JSON.stringify(the_bookmarks));
}

