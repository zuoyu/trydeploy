(function (global) {

'use strict';


function setdynamic(img,tit,tex,date,author,type){
  if (type == "git"){
    var string = "<li id=\"view_list_style\" class=\"ui-btn ui-btn-b ui-li ui-li-has-thumb  ui-btn-up-c\"  ><div class=\"ui-btn-inner ui-li\"><div class=\"ui-btn-text\"><a class=\"ui-link-inherit\" href=\"#\"><img  style='height:2em;width:2em;' id=\"imagetag\"class=\"ui-li-thumb\" src=\""+img+"\"><p style='display:inline;float:left;position:relative;left:3em'> by "+author+"</p><h2 style='display:inline;' class=\"ui-li-heading\">\""+tit+"\"</a>&nbsp;&nbsp&nbsp;&nbsp&nbsp;&nbsp<span id=\"test\">["+date+"]</span></h2><p class=\"ui-li-desc\" style='white-space:normal;'>"+tex+"</p></a></div>&nbsp;</div></li>"
    return string;
  }
  if (type == "post"){
    var string = "<li id=\"view_list_style\" class=\"ui-btn ui-li ui-li-has-thumb  ui-btn-up-c\"  ><div class=\"ui-btn-inner ui-li\"><div class=\"ui-btn-text\"><a class=\"ui-link-inherit\" href=\"#\"><img  style='height:2em;width:2em;' id=\"imagetag\"class=\"ui-li-thumb\" src=\""+img+"\"><p style='display:inline;float:left;position:relative;left:3em'> by "+author+"</p><h2 style='display:inline;' class=\"ui-li-heading\">\""+tit+"\"</a>&nbsp;&nbsp&nbsp;&nbsp&nbsp;&nbsp<span id=\"test\">["+date+"]</span></h2><p class=\"ui-li-desc\" style='white-space:normal;'>"+tex+"</p></a></div>&nbsp;</div></li>"
    return string;
  }
  return string;
};

function getpost(data,page,cookie){
  var url = "api/posts/";
  var request = $.ajax({
          method: "GET",
          url: url,
  });
  request.done(function (callback) {
            var postobj = callback;
            var github = cookie.get("github");
            console.log(github);
            if(page == "home"){
                $.each(postobj.posts, function (i, value) {             
                        var st= setdynamic("/static/image/Yu.jpg",postobj.posts[i].title,postobj.posts[i].content,postobj.posts[i].date_created,postobj.posts[i].username,"post");
                        $("#list_post_view").append(st);
                });
            }
            if(page == "posted"){
                $.each(postobj.posts, function (i, value) {
                    if(data.username == postobj.posts[i].username){
                        var st= setdynamic("/static/image/Yu.jpg",postobj.posts[i].title,postobj.posts[i].content,postobj.posts[i].date_created,postobj.posts[i].username,"post");
                        console.log(postobj.posts[0].author.github);
                        $("#list_post_view").append(st);
                    }
                });
              var request = $.ajax({
                      method: "GET",
                      url: github,
              });
              request.done(function (callback) {
                        console.log(callback)
                        var githubobj = callback;
                        $.each(githubobj, function (i, value) {
                            var st= setdynamic("/static/image/git.png",githubobj[i].type,githubobj[i].repo.name,githubobj[i].created_at,"github user - "+githubobj[i].actor.login,"git");
                        
                            $("#list_post_view").append(st);
                        });
                     });
              request.fail(function (callback) {
                        console.log(callback);
                     });
            }

         });
  request.fail(function (callback) {
            console.log(callback);
         });
}


global.load_posts= {
    posts_load:getpost
    

}



})(this);