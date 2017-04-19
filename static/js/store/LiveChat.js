

var live_chat_guests;
var btn_sendLiveMessage;
var session_id;
var chatLog = {};


$(document).ready(function(){
	bindChatElements();
	initLiveChat();
	
	bindChatEvents();

});




function bindChatElements(){
	live_chat_guests = $("#live_chat_guests");
	live_chat_window = $("#live_chat_window");

	input_liveChatMessage = $("#input_liveChatMessage");
	btn_sendLiveMessage = $("#btn_sendLiveMessage");

	session_id = $("#current_sessionID").val();
}


function bindChatEvents(){

	$('#input_liveChatMessage').keypress(function (e) {
		 var key = e.which;
		 if(key == 13)  // the enter key code
		  {
		    btn_sendLiveMessage.trigger("click");
		    return false;  
		  }
		});   

	btn_sendLiveMessage.unbind();
	btn_sendLiveMessage.click({session_id: session_id}, sendMessage);

	
	window.setInterval(function(){
	 	retrieveChatLog(session_id);
	}, 2000);
	
}




function initLiveChat(){
	var message = input_liveChatMessage.val();

	$.ajax({
	  method: "GET",
	  url: "/actions/store_message",

	  data: { 
	  	session_id: session_id,
	  	body: "null",
	  	type: "live_chat_init"
	  },

	})
	  .done(function(response) {
	  	if (response != "\"invalid\""){
	  		retrieveChatLog(session_id);
	  	} 
	 
	  });

	 input_liveChatMessage.val("");
}








function sendMessage(){
	var message = input_liveChatMessage.val();

	if(message == ""){
		return;
	}


	$.ajax({
	  method: "GET",
	  url: "/actions/store_message",

	  data: { 
	  	session_id: session_id,
	  	body: message,
	  	type: "live_chat_fromUser"
	  },

	})
	  .done(function(response) {
	  	if (response != "\"invalid\""){
	  		//retrieveChatLog(session_id);

	  	} 
	 
	  });

	 input_liveChatMessage.val("");
}




function createChatLog(){
	var message_index = 0;
	var messages = 1;
	var combinedList = [];

	while(messages >= 1){
		messages = 0;

		if("toUser" in chatLog[session_id]){
			if(message_index < chatLog[session_id]["toUser"].length){

				var parsed_timestamp = Date.parse(chatLog[session_id]["toUser"][message_index]["timestamp"]);

				chatLog[session_id]["toUser"][message_index]["type"] = "toUser";
				chatLog[session_id]["toUser"][message_index]["unix_timestamp"] = parsed_timestamp;

				combinedList.push(chatLog[session_id]["toUser"][message_index]);
				messages += 1;
			}
		}


		if("fromUser" in chatLog[session_id]){
			if(message_index < chatLog[session_id]["fromUser"].length){

				var parsed_timestamp = Date.parse(chatLog[session_id]["fromUser"][message_index]["timestamp"]);
				
				chatLog[session_id]["fromUser"][message_index]["type"] = "fromUser";
				chatLog[session_id]["fromUser"][message_index]["unix_timestamp"] = parsed_timestamp;

				combinedList.push(chatLog[session_id]["fromUser"][message_index]);

				messages += 1;
			}
		}

		message_index++;
	}


	combinedList = combinedList.sort(function(x, y){
	    return x.unix_timestamp - y.unix_timestamp;
	})


	for(var i=0;i<combinedList.length;i++){

		if(combinedList[i]["type"] == "toUser"){
			live_chat_window.append("<div class=\"toUser-message\">" + combinedList[i]["body"] + "</div>");

		}
		else if(combinedList[i]["type"] == "fromUser"){
			live_chat_window.append("<div class=\"fromUser-message\">" + combinedList[i]["body"] + "</div>");
		}

	}

	var trueDivHeight = live_chat_window[0].scrollHeight;
	var divHeight = live_chat_window.height();
	var trueBottom = trueDivHeight - divHeight;


	live_chat_window.stop().animate({ scrollTop: trueBottom }, "slow");

		
}



function retrieveChatLog(){
	chatLog[session_id] = {};

	$.ajax({
	  method: "GET",
	  url: "/actions/get_live_chat_messages",

	  data: { 
	  	session_id: session_id,
	  },

	})
	  .done(function(response) {
	  	if (response != "\"invalid\""){
	  		//console.log(response);
	  		populateChatLog(response);
	  	} 
	  	else{
	  		return null;
	  	}
	  
	  });
}



var entityMap = {
  '&': '&amp;',
  '<': '&lt;',
  '>': '&gt;',
  '"': '&quot;',
  "'": '&#39;',
  '/': '&#x2F;',
  '`': '&#x60;',
  '=': '&#x3D;'
};


function escapeHtml (string) {
  return String(string).replace(/[&<>"'`=\/]/g, function (s) {
    return entityMap[s];
  });
}


function populateChatLog(messages){
	live_chat_window.html("");
	//live_chat_window.append("Chatting with: " + session + "<hr>");

	messages = JSON.parse(messages);

	// loop through messages in chat log
	for(var i=0;i<messages.length;i++){
		var message_type = messages[i][0];
		var message_body = escapeHtml(messages[i][1]);
		var message_timestamp = messages[i][2];
		var message_sessionID = messages[i][3];
		var message_ttl = messages[i][4];

		var messageData = {
			body: message_body,
			timestamp: message_timestamp,
			ttl: message_ttl,
			type: message_type
		};


		// create a new dictionary to represent messages 
		if (!(message_sessionID in chatLog)){		
			chatLog[message_sessionID] = {};
			
			
		}

		if(message_type == "live_chat_init"){
				continue;
			}

		// append a message from the admin -> user
		else if(message_type == "live_chat_toUser"){
			if("toUser" in chatLog[message_sessionID]){
				chatLog[message_sessionID]["toUser"].push(messageData);

			}
			else{
				chatLog[message_sessionID]["toUser"] = [];
				chatLog[message_sessionID]["toUser"].push(messageData);
			}
			
		}

		// append a message from user -> admin
		else if(message_type == "live_chat_fromUser"){
			if("fromUser" in chatLog[message_sessionID]){
				chatLog[message_sessionID]["fromUser"].push(messageData);

			}
			else{
				chatLog[message_sessionID]["fromUser"] = [];
				chatLog[message_sessionID]["fromUser"].push(messageData);
			}

			
		}

	
	}	// end loop through messages

	createChatLog(message_sessionID);
}