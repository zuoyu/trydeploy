(function (global) {

'use strict';




function findfriends(cookie,data,page){
  var load_post = global.load_posts; 
  console.log("yoyo");
  console.log(cookie.get("userid"));
  var url = "api/friends/"+cookie.get("userid");
  var request = $.ajax({
          method: "GET",
          url: url,
        });
  request.done(function (callback) {
            console.log(callback);
            var friendsobj = callback;

            $.each(friendsobj.authors,function (i,value){
              //console.log("sm++++");
              //console.log(i);
              var auturl = "api/author/"+friendsobj.authors[i];
              $.getJSON(auturl,function(data){
                    
                    //console.log(data);
                    if(page == "network"){
                      $("#f2").append("<li class=\"ui-last-child\" ><a id =\"click_target\" value=\""+data.id+"\" class=\"ui-btn ui-btn-icon-right ui-icon-user\">"+data.username+"</a></li>");
                    }
                    if(page =="friends" ){
                      $("#friends_list_view").append("<li class=\"ui-last-child\" ><a id =\"click_target\" value=\""+data.id+"\" class=\"ui-btn ui-btn-icon-right ui-icon-user\">"+data.username+"</a></li>");
                    }           
                });
            }); 

         });
  request.fail(function (callback) {
            console.log(callback);
         });
};

global.findfriends= {
  friends:findfriends
	
}



})(this);