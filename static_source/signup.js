
(function () {

'use strict';

var url = 'api/author/'

function postAuthor(author) {
    console.log(author)
    $.ajax({
      type: "POST",
      url: url,
      data: JSON.stringify(author),
      contentType:"application/json; charset=utf-8",
      success: function(msg){
        alert( "successfull sign up your account please wait admin to prove" );
        setTimeout(function(){
          window.location.href = "home";
          },1000
        );     
      },
      error: function(error) {
        alert( "Sorry the accout already exit. try another account" );
      }
    });
}

function getAuthor() {
    return {
        "username": value('#username-input') ,
        "email": value('#email-input'),
        "password": value('#password-input') ,
        "first_name": value('#first-name-input'),
        "last_name": value('#last-name-input'),
        "github": value('#github-input')
    };
}

function value(field) {
    return $(field).val();
}

function setup() {
    $('#create-btn').click(function () {
        var author = getAuthor();
        postAuthor(author);   
    });
}

setup();




})();






