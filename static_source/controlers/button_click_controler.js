(function (global) {
'use strict';
var cookie = global.cookie_setting;
function button_click(cookie){

    
    

    $("#connect_friends").click(function(){
        setTimeout(function(){
          window.location.href = "friends";
        },0
          );
    });

    $("#connect_home").click(function(){
        setTimeout(function(){
          window.location.href = "home";
        },0
          );
    });

    $("#connect_net").click(function(){
        setTimeout(function(){
          window.location.href = "network";
        },0
          );
    });

    $("#connect_prof").click(function(){
        setTimeout(function(){
          window.location.href = "posted";
        },0
          );
    });

}



global.button_click = {
	clickbtn:button_click

}

})(this);
