function scaleElements() {
  var width = document.getElementById("story-main-img").width + "px";
  console.log(width);
  document.getElementById("story-content").style.width = width;
  document.getElementById("story-title").style.width = width;
  document.getElementById("story-info").style.width = width;
  document.getElementById("comments-wrapper").style.width = width;
}

scaleElements();
