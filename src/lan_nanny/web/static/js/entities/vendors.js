/*
  Lan Nanny Web
  Entities 
  Vendors

*/
import { API_URL } from "/config.js";
import * as main from "/static/js/main.js";


export function get_vendors(){
    /* Get Vendors and store them in local storage */
    $.ajax({
        type: "GET",
        url: API_URL + "/vendors",
        headers: {
            "Token": main.get_cookie("Token"),
            "Content-Type": "application/json"
        },
        dataType: "json",
        success: function(data){
            console.log("Successfully got vendors");

            // Convert array to dictionary keyed by the `id` field
            const vendor_dict = data.objects.reduce((acc, obj) => {
                acc[parseInt(obj.id)] = obj; // Set the object in dictionary with id as key
                return acc; // Return the accumulator for the next iteration
            }, {});
            console.log(vendor_dict);
            localStorage.setItem('vendors', JSON.stringify(vendor_dict));


        },
    });
    return
}

