$(function () {
  var chatDisplayWindow = $('#chat-display-window');
  var userInput = $('#user-input');

  function scrollToBottom() {
    chatDisplayWindow.scrollTop(chatDisplayWindow[0].scrollHeight);
  }

  function sendMessage() {
    var message = userInput.val().trim();
    if (message) {
      $.ajax({
        type: 'POST',
        url: '/Flexirobo/chat',
        data: JSON.stringify({ message: message }),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function (data) {
          var reply = data['message'];
          chatDisplayWindow.append('<p><span class="user-message">' + message + '</span></p>');
          chatDisplayWindow.append('<p><span class="bot-message">' + reply + '</span></p>');
          userInput.val('');
          scrollToBottom();
        }
      });
    }
  }

  $('#submit-button').click(sendMessage);

  userInput.keydown(function (e) {
    if (e.keyCode == 13 && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    } else {
      setTimeout(scrollToBottom, 0);
    }
  });

  $(window).resize(scrollToBottom);

  scrollToBottom();
});