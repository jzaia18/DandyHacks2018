//Copy a given message to the user's clipboard
function copyToClipboard(message) {
  if (!message)
    return;
  var textElement = document.createElement("textarea");
  textElement.value = message;
  document.body.appendChild(textElement);
  textElement.select();
  document.execCommand("copy");
  document.body.removeChild(textElement);
}
