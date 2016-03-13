(function (global) {

'use strict';

var tokenApi = 'api/authors/me/',
    token = '',
    user = {};

function requestToken(username, password, callback) {
  $.ajax({
    method: 'POST',
    url: tokenApi,
    contentType:"application/json; charset=utf-8",
    data: JSON.stringify({
      'username': username,
      'password': password
    }),
    success: function (data) {
      global.token = token = data['token'];
      global.user = user = data['user'];
      callback(user, token);
    },
    error: function (error) {
      console.log(error);
    }
  });
}

function patchProfile(username,firstName, lastName, callback) {
  $.ajax({
    method: 'PATCH',
    url: user.url,
    contentType:"application/json; charset=utf-8",
    data: JSON.stringify({
      'username': username,
      'first_name': firstName,
      'last_name': lastName

    }),
    beforeSend: function (xhr) {
      xhr.setRequestHeader('Authorization', 'Token ' + token);
    },
    success: function (data) {
      callback(data);
    },
    error: function (error) {
      console.log(error);
    }
  })
}

function setup() {
  $('#update-form').hide();
  $('#token-btn').click(function () {
    var username = $('#username-input').val(),
        password = $('#password-input').val();

    $('#token-display').html('');
    $('#user-display').html('');
    requestToken(username, password, function (user, token) {
      $('#token-display').html(token);
      $('#user-display').html(JSON.stringify(user));
      $('#update-form').show();
      $('#update-btn').click(function () {
        var firstName = $('#first-name-input').val(),
            lastName = $('#last-name-input').val();
        patchProfile(username,firstName, lastName, function (data) {
          $('#user-display').append('<br><br>');
          $('#user-display').append(JSON.stringify(data));
          console.log(data);
        });
      });
    });
  });
  
}

setup();


})(this);