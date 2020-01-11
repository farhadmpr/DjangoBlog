$(function() {
  $("#btnFollow").click(function() {
    // Django Ajax CSRF ********************************************** */
    function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie !== "") {
        var cookies = document.cookie.split(";");
        for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === name + "=") {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
    var csrftoken = getCookie("csrftoken");

    function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
    }
    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      }
    });
    //*************************************************************** */

    let user_id = $(this).data("id");
    let action = $(this).attr("data-action");
    let url = "";
    let text = "";
    let cssClass = "";

    if (action == "follow") {
      url = "/accounts/follow/";
      text = "Unfollow";
      cssClass = "btn-secondary";
      action = "unfollow";
    } else {
      url = "/accounts/unfollow/";
      text = "Follow";
      cssClass = "btn-primary";
      action = "follow";
    }

    $.ajax({
      url: url,
      method: "POST",
      data: {
        user_id: user_id
      },
      success: function(data) {
        if (data["status"] == "true") {
          alert(data["status"]);
          $("#btnFollow").text(text);
          $("#btnFollow").attr("class", "btn " + cssClass);
          $("#btnFollow").attr("data-action", action);
        }
      }
    });
  });
});
