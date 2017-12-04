var checked;
var remember;
var label;

$(document).ready(function(){
  checked = false;
  remember = $("#remember");
  label = remember.prev();
  label.append(' <i id="remember-box" class="fa fa-square-o" aria-hidden="true"></i>');

  label.click(function() {
    remember.on();
    checked = !checked;
    var rememberBox = $("#remember-box");

    if (checked) {
      rememberBox.removeClass("fa-square-o");
      rememberBox.addClass("fa-check-square");
      rememberBox.css("color", "#329664");
    }

    else {
      rememberBox.removeClass("fa-check-square");
      rememberBox.addClass("fa-square-o");
      rememberBox.css("color", "");
    }
  });

  label.css("cursor", "pointer");
})