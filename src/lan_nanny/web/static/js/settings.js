/*
  Bookmarky Web Simple
  Settings

*/
import { API_URL, VERSION_WEB } from "/config.js";
import * as main from "/static/js/main.js";


function get_whoami(){
    /* Get User and environment details */
    $.ajax({
        type: "GET",
        url: API_URL + "/who-am-i",
        headers: {
            "Token": main.get_cookie("Token"),
            "Content-Type": "application/json"
        },
        success: show_who_am_i,
        dataType: "json"
    });
}

function show_who_am_i(data){
    if(Object.hasOwn(data.user, 'metas') && Object.hasOwn(data.user.metas, 'display_hidden')){
        if(Object.hasOwn(data.user.metas, 'beta_features')){
            console.log("We have beta features");
            $("#setting-user-display-hidden").prop('checked', data.user.metas.beta_features.value);
        } else {
            console.log("No beta features");
            $("#setting-user-beta-features").prop("checked", false);
        }
        if(Object.hasOwn(data.user.metas, 'display_hidden')){
            console.log("Lets show the display details");
            $("#setting-user-display-hidden").prop('checked', data.user.metas.display_hidden.value);
        }
    }
    update_cell($("#settings-user-id"), data.user.id);
    update_cell($("#settings-server-version-api"), data.server.version);
    update_cell($("#info-token-expires-value"), data.token.expiration_date);
    update_cell($("#user-info-meta-display-hidden"), data.user.metas.display_hidden.value);
}


function get_database_stats(){
    /* Get Server database stats */
    $.ajax({
        type: "GET",
        url: API_URL + "/stats/entity-counts",
        headers: {
            "Token": main.get_cookie("Token"),
            "Content-Type": "application/json"
        },
        success: show_entity_counts,
        dataType: "json"
    });
}

function show_entity_counts(data){
    console.log(data);
    update_cell("#stats-database-bookmarks-total", data.entities.bookmarks);
    update_cell("#stats-database-bookmark-tags-total", data.entities.bookmark_tags);
    update_cell("#stats-database-tags-total", data.entities.tags);
    // update_cell($("#settings-user-id"), data.user.id);
    // update_cell($("#settings-server-version-api"), data.server.version);
    // update_cell($("#info-token-expires-value"), data.token.expiration_date);
}



function update_cell(cell, value){
    $(cell).html("<code>" + value + "</code>");
}

function update_user_settings(){
    var display_hidden = $("#setting-user-display-hidden").is(":checked");
    var beta_features = $("#setting-user-beta-features").is(":checked");
    var data = {
        "metas": {
            "display_hidden": display_hidden,
            "beta_features": beta_features,
        }
    }
    console.log("Gonna send payload");
    console.log(data);
    $.ajax({
        type: "POST",
        url: API_URL + "/user/meta",
        headers: {
            "Token": main.get_cookie("Token"),
            "Content-Type": "application/json"
        },
        data: JSON.stringify(data),
        success: saved_user_settings,
        dataType: "json"
    });
}

function saved_user_settings(){
    main.notify("Saved user settings", "success");
}


$(document).ready(function(){
    update_cell($("#settings-site-url"), API_URL);
    update_cell($("#settings-server-version-web"), VERSION_WEB);

    $("#setting-user-save-submit").click(function(){
        update_user_settings();

    });

    get_whoami();
    get_database_stats();
});
