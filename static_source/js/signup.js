(function () {

'use strict';

var url = 'api/authors/'

function postAuthor(author) {
    console.log(author)
    $.ajax({
      type: "POST",
      url: url,
      data: JSON.stringify(author),
      contentType:"application/json; charset=utf-8",
      success: function(msg){
        alert( "Data Saved: " + msg );
      },
      error: function(error) {
        console.log(error.responseText);
      }
    });
}

function getAuthor() {
    return {
        "username": value('#username-input') || 'user_99',
        "password": value('#password-input') || '0000',
        "email": value('#email-input') || "u1@email.com",
        "author": {
            "github": value('#github-input') || "user1"
        },
        "first_name": value('#first-name-input') || "Yushi",
        "last_name": value('#last-name-input') || "Wang"
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