(function (global) {

'use strict';

function setCookie(key,value){
  document.cookie = key+"="+value;
};

function clearCookie(token){
  setCookie(token,"undefined",-1);
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1);
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return " ";
}


global.cookie_setting = {
	set:setCookie,
	get:getCookie,
	clear:clearCookie,
}


})(this);
