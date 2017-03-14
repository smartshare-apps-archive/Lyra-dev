$(document).ready(function(){
	bindCoreEvents();
});


function bindCoreEvents(){
	$(".top-navbar li").each(function(){
		menuID = "#" + $(this).attr('id').split('_')[1] + "_menu";
		$(this).mouseenter({menuID: menuID}, popup_Menu);
	});

	$("#header_logo").click(function(){
		window.location.href = '/';
	});


	$("#cart_link").click(function(){
		window.location.href = '/cart';
	});

	$("#user_link").click(function(){
		window.location.href = '/login';
	});

	if($("#admin_link")){
		$("#admin_link").click(function(){
			window.location.href = '/control/products';
		});
	}


	if($("#logout_link")){
		$("#logout_link").click(function(){
			window.location.href = '/auth/logout';
		});
	}

	if($("#btn_returnToStore")){
		$("#btn_returnToStore").click(function(){
			window.location.href = '/products';
		});
	}

}



function popup_Menu(event){
	var nav_link = $(event.target);
	var offset = nav_link.offset();
	
	var menuID = event.data.menuID;
	
	var top = offset.top;
	var left = offset.left;


	$(menuID).css('display',"inline");
	$(menuID).css('top',top + "px");
	$(menuID).css('left',left + "px");

	$(menuID).mouseleave({menuID: menuID}, close_Menu);
}



function popup_Message(messageHTML){
	var toggleHeight = 100;
	var bottomPos = $(window).scrollTop() + $(window).height()

	$("#message_container").css("top", (bottomPos - toggleHeight) + "px");
	

	$("#message_container").html(messageHTML);
	$("#message_container").slideToggle("fast");
	
	setTimeout(close_Message, 5000);
}


function close_Message(){
	$("#message_container").slideUp("fast");
}


function close_Menu(event){
	var menuID = event.data.menuID
	$(menuID).css('display',"none");
}


function replaceAll(str, find, replace) {
  return str.replace(new RegExp(find, 'g'), replace);
}


