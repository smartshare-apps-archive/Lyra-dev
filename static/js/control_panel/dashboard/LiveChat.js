

var live_chat_guests;
var btn_sendLiveMessage;

var chatLog = {};
var intervalID;

$(document).ready(function(){
	bindChatElements();
	getUserList();



});


function bindChatElements(){
	live_chat_guests = $("#live_chat_guests");
	live_chat_window = $("#live_chat_window");

	input_liveChatMessage = $("#input_liveChatMessage");
	btn_sendLiveMessage = $("#btn_sendLiveMessage");
}


function bindChatEvents(){
	var session_id;

	$(".btn-chat-user").each(function(){

		$(this).unbind();
		session_id = $(this).attr('data-sessionID');

		$(this).click({user_sessionID: session_id}, loadChatWindow);


	});

}



function getUserList(){

	$.ajax({

	  method: "GET",
	  url: "/actions/get_message",

	  data: { 
	  	type: "live_chat_init",
	  	body: "null"
	  },

	})
	  .done(function(response) {
	  	if (response != "\"invalid\""){
	  		var users = JSON.parse(response);

	  		populateUserList(users);
	  		bindChatEvents();
	  	} 
	  
	  });



}




function populateUserList(users){
	live_chat_guests.html("");
	
	for(var i=0;i<users.length;i++){
		var currentHTML = "";

		var session_id = users[i][0];
		var timestamp = users[i][1];
		var ttl = users[i][2];

		currentHTML += "<button type=\"button\" class=\"btn btn-primary btn-chat-user\" data-sessionID=\"" + session_id + "\">" + session_id + "</button> <hr class=\"hr-sm-margin\">";

		live_chat_guests.append(currentHTML);
	}

	
}




function loadChatWindow(event){
	user_sessionID = event.data.user_sessionID;
	


	$('#input_liveChatMessage').keypress(function (e) {
		 var key = e.which;
		 if(key == 13)  // the enter key code
		  {
		    btn_sendLiveMessage.trigger("click");
		    return false;  
		  }
	});   

	btn_sendLiveMessage.unbind();
	btn_sendLiveMessage.click({session_id: user_sessionID}, sendMessage);

	retrieveChatLog(user_sessionID);

	clearInterval(intervalID);

	intervalID = window.setInterval(function(){
	 	retrieveChatLog(user_sessionID);
	}, 2000);

}




function sendMessage(event){

	var session_id = event.data.session_id;
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
	  	type: "live_chat_toUser"
	  },

	})
	  .done(function(response) {
	  	if (response != "\"invalid\""){
	  		

	  	} 
	 
	  });

	 input_liveChatMessage.val("");
}


function createChatLog(session_id){

	var message_index = 0;
	var messages = 1;
	var combinedList = [];

	while(messages >= 1){
		messages = 0;

		if("toUser" in chatLog[session_id]){
			if(message_index < chatLog[session_id]["toUser"].length){

				var parsed_timestamp = Date.parse(chatLog[session_id]["toUser"][message_index]["timestamp"]);

				//live_chat_window.append("<div class=\"toUser-message\">" + chatLog[session_id]["toUser"][message_index]["body"] + "</div>");

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

				//live_chat_window.append("<div class=\"fromUser-message\">" + chatLog[session_id]["fromUser"][message_index]["body"] + "</div>");
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



function retrieveChatLog(session_id){
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


function populateChatLog(messages){
	live_chat_window.html("");
	live_chat_window.append("Chatting with: " + user_sessionID + "<hr>");

	messages = JSON.parse(messages);

	// loop through messages in chat log
	for(var i=0;i<messages.length;i++){
		var message_type = messages[i][0];
		var message_body = messages[i][1];
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
			console.log("created");
			
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