(function (global) {

'use strict';


var cookie = global.cookie_setting;



function getuserlogin(cookie,username,callback){
    var url = "api/author/me";
    var request = $.ajax({
            method: "GET",
            url: url,
          });
    request.done(function (callback) {
              var userobj = callback;
              cookie.set("username",userobj.username);
           });
    request.fail(function (callback) {
              console.log(callback);
           });

}









global.login_setting = {
	url_setting:getuserlogin,

}



})(this);