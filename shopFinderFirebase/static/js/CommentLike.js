function LikePost(post_id) {
  var xhttp = new XMLHttpRequest();
  // xhttp.onreadystatechange = function() {
  //   if (this.readyState == 4)
  //   {
  //
  //     str = document.getElementById(post_key).innerHTML
  //     str = str.substr(7, str.length - 1).trim()
  //     console.log(str)
  //     var integer = parseInt(str, 10);
  //     console.log(integer)
  //     integer += 1;
  //     document.getElementById(post_key).innerHTML = "Likes: " + String(integer);
  //   }
  // };
  xhttp.open("POST", "/Like", false);

  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.send("post=" + post_id );
}
function CommentPost(post_id) {
  var xhttp = new XMLHttpRequest();
  xhttp.open("POST", "/comment", false);
  var content=document.getElementById("Input"+post_id).value;
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.send("post=" + post_id +"&comment="+content);
}