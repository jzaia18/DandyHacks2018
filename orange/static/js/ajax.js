function vote(articleID, direction) {
  var updateCookie = true;
  if ($.cookie(articleID) && $.cookie(articleID) == direction) {
    direction *= -1;
    $.removeCookie(articleID);
    updateCookie = false;
  }
  else if ($.cookie(articleID) && $.cookie(articleID) == direction*-1) {
    direction *= 2;
  }

  $.ajax({
    url: "/vote/"+articleID+"/"+direction,
    context: document.body
  }).done(function() {
    $("#votes-"+articleID)[0].innerText-= -1*direction;
    if (updateCookie && direction != 0) {
      direction/=Math.abs(direction);
      $.cookie(articleID, direction, { expires : 10});
    }
  });
}
