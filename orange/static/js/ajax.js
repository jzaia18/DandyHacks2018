function vote(articleID, direction) {
  if ($.cookie(articleID) && $.cookie(articleID) == direction)
    return;

  $.ajax({
    url: "/vote/"+articleID+"/"+direction,
    context: document.body
  }).done(function() {
    $.cookie(articleID, direction, { expires : 10});
    if (direction == "left") {
      $("#votes-"+articleID)[0].innerText++;
    }
    else if (direction == "right") {
      $("#votes-"+articleID)[0].innerText--;
    }
  });
}
