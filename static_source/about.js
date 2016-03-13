
var data= {"username":getCookie("username"),
       "userphoto":"../static/image/Yu.jpg",
       "followers":"50",
       "following":"77",
       "friends":"112"
       };
console.log(data);

if (data.username == "undefined" || data.username == "" ){
  
  document.getElementById("loginbutton").innerHTML ="<button id=\"signup\" onclick=\"signuppage()\"type=\"button\" class=\"btn btn-lg btn-primary\">Sign up</button> <a href=\"#myPopupDialog\" data-rel=\"popup\" data-position-to=\"window\" data-transition=\"fade\" ><button id=\"signin\"onclick=\"signinbox()\"type=\"button\" class=\"btn btn-lg btn-default\">Sign in</button></a>";
  $("#fot").hide();
  $("#div1").hide();
  $("#div2").hide();
}else{

  document.getElementById("loginbutton").innerHTML ="<a href=\"posted\" id=\"user_name_input\">[ "+data.username+" ]</a>&nbsp &nbsp &nbsp<a href=\"#myProfileDialog\" data-rel=\"popup\" data-position-to=\"window\" data-transition=\"fade\" ><button id=\"edit\"onclick=\"signinbox()\"type=\"button\" class=\"btn btn-lg btn-default\">Edit Profile</button></a><button id=\"logoutbutton\" type=\"button\" class=\"btn btn-lg btn-warning\">Logout</button>";
};

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
    return "";
}



function patchProfile(username,firstName, lastName, callback) {

  var token = JSON.parse(getCookie("token"));
  console.log(token.token);


  $.ajax({
    method: 'PATCH',
    url: getCookie("url"),
    contentType:"application/json; charset=utf-8",
    data: JSON.stringify({
      'username': username,
      'first_name': firstName,
      'last_name': lastName

    }),
    beforeSend: function (xhr) {
      xhr.setRequestHeader('Authorization', 'Token ' + token.token);
    },
    success: function (data) {
      //callback(data);
      setCookie("username",username);
      setTimeout(function(){
      window.location.href = "friends";
        },1000
      );


    },
    error: function (error) {
      console.log(error);
    }
  })
}






$("#update_submit").click(function(){

    var username_input = $("#user-name-input").val();
    var firstname_input = $('#first-name-input').val();
    var lastname_input = $('#last-name-input').val();

    patchProfile(username_input,firstname_input, lastname_input);
    //$("#response").html(token);  
    
});





function getlogin(url,data,callback){
  var val;
  var username = data.username;
  //console.log(username);
  var password = data.password;
  var request = $.ajax({
          method: "POST",
          url: url,
          data: data,

        });
  request.done(function (callback) {
            //console.log(callback);
            var token =JSON.stringify(callback);

            
            setCookie("username",username);
            setCookie("token",token);
            
         });
  request.fail(function () {
            //console.log(callback);
            clearCookie("username");
            clearCookie("token");
            clearCookie("url");
         });
  //return callback;

};

$("#login_submit").click(function(){
    var username = $("#username").val();
    var password = $("#password").val();

    var data = {"username": username, "password": password};
    //console.log(data);
    var url = "api-token/";
    var callback = "";
    getlogin(url,data,callback);
    var token=getCookie("token");
   
    //console.log(token);
    //$("#response").html(token);  
    setTimeout(function(){
      window.location.href = "friends";
    },1000
      );
});



$("#logoutbutton").click(function(){
  clearCookie("username");
    clearCookie("token");
    clearCookie("url");
    
    setTimeout(function(){
      window.location.href = "home";
    },1000
      );


});




$("#connect_friends").click(function(){
    
    setTimeout(function(){
      window.location.href = "friends";
    },1000
      );


});
$("#connect_home").click(function(){
    
    setTimeout(function(){
      window.location.href = "home";
    },1000
      );


});

$("#connect_prof").click(function(){
    
    setTimeout(function(){
      window.location.href = "posted";
    },1000
      );


});

$("#connect_net").click(function(){
    
    setTimeout(function(){
      window.location.href = "network";
    },1000
      );


});