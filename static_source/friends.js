(function (global) {

'use strict';


var cookie = global.cookie_setting;
var clicks = global.button_click;
var infor_nav = global.nav_inf;
var login_infor_set = global.login_setting;
var update_and_post = global.update_and_post;
var frineds_find =global.findfriends;


var data= {"username":cookie.get("username"),
       "url":cookie.get("url"),
       "token":cookie.get("token"),
       "userphoto":"../static/image/Yu.jpg",
       "followers":"50",
       "following":"77",
       "friends":"112"
       };

function setup(cookie,login_infor_set,infor_nav,clicks,data){
  var page="friends";
  

  $("#searchbutton").click(function(){
      console.log($('#myFilter').val());
      searchfriend($('#myFilter').val());
  });

  $("#update_submit").click(function(){
      var username_input = $("#user-name-input").val();
      var firstname_input = $('#first-name-input').val();
      var lastname_input = $('#last-name-input').val();
      update_and_post.update_profile(cookie,data,username_input,firstname_input, lastname_input); 
  });

  $('#post_post').click(function(){
      update_and_post.post_posts(data.url);
  });


  infor_nav.nav_inf_setting(data,page);
  clicks.clickbtn(cookie);
  frineds_find.friends(cookie,data,"friends");
};



setup(cookie,login_infor_set,infor_nav,clicks,data);

})(this);