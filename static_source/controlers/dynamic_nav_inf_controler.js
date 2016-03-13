(function (global) {

'use strict';

function setifor(img,username,followers, following, friends){
  var string = "<table><tr><td id = \"holder\"><center><img id = \"user_file_image\"src=\""+img+"\"height=\"150\" width=\"150\">  </center>  </td><td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td><td id=\"userintroduction\"><div class=\"page-header\"><h1>"+username+"</h1></div><div class=\"well\"><p>Following: "+following+"   Followers: "+followers+"    Friends: "+friends+"</p></div></td></tr></table>";
  return string;
};

function nav_inf_set(data,page){
    var cookie = global.cookie_setting;
    var url = "api/author/me";
    var request = $.ajax({
            method: "GET",
            url: url,
          });
    request.done(function (callback) {
              var userobj = callback;
              var head = setifor(data.userphoto,userobj.username,data.following, data.followers, data.friends);
              cookie.set("username",userobj.username);
              cookie.set("github", userobj.github);
              cookie.set("userid",userobj.id);
              //console.log(userobj.id);
              $("#loginbutton").html("<a href=\"posted\" id=\"user_name_input\">[ "+userobj.username+" ]</a>&nbsp &nbsp &nbsp<a href=\"#myProfileDialog\" data-rel=\"popup\" data-position-to=\"window\" data-transition=\"fade\" ><button id=\"edit\"onclick=\"signinbox()\"type=\"button\" class=\"btn btn-lg btn-default\">Edit Profile</button></a><a href=\"/logout/\">&nbsp;&nbsp;&nbsp;<button id=\"logoutbutton\" type=\"button\" class=\"btn btn-lg btn-warning\">Logout</button></a>");
              $("#info").html(head);
              $("#connect-infor").html("<div id=\"connect-infor\" class=\"alert alert-success\" ><center><strong>Successfully loaded!</strong> You can view your friends' posts below.<br>if you want to see the most recent posts please click the refresh button or the load more button at the bottom<center></div>");
           });
    request.fail(function (callback) {
              console.log(callback);
           });

}



global.nav_inf= {
  nav_inf_setting:nav_inf_set
	
}



})(this);
