/*
  Bookmarky Web Simple
  Main

*/

export function human_time(the_time){
  const utcDate = new Date(the_time);
  // Convert the UTC Date to the client's local time
  const localDate = new Date(utcDate.toLocaleString());
  // Get a friendly formatted timestamp in the client's local timezone
  const friendlyTimestamp = localDate.toLocaleString();
  return friendlyTimestamp;
}


export function notify(message, type){
  /* Create a notification message to the user. */
  $("#notify").text(message);
  $("#notify").slideDown(500, function(){
    $(this).delay(2000);
    $("#notify").slideUp(1000);
  });
}


export function truncate(text, max_size=100){
  /* Truncate a string if it's longer than we want it to be. */
  if (text == null){
    return "";
  }
  if(text.length >= max_size){
    return text.substring(0, max_size) + "...";
  } else {
    return text;
  }
}


export function set_cookie(cname, cvalue, exdays) {
  // Set a cookie by name, value and expiration date
  const d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  let expires = "expires="+ d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}


export function get_cookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');
  for(let i = 0; i <ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

export function delete_cookie(cname) {
  // Set the cookie's expiration date to a time in the past
  document.cookie = cname + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/";
}
