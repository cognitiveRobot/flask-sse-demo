function listen() {
    var source = new EventSource("/stream/");
    var target = document.getElementById("messageDiv");
    source.onmessage = function(msg) {
      console.log(msg.data);
	     target.innerHTML = msg.data + '<br>';
    }
}

listen();
