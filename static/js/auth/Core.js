

$(document).ready(function(){
	bindCoreEvents();
});


function bindCoreEvents(){
	$(".top-navbar li").each(function(){
		menuID = "#" + $(this).attr('id').split('_')[1] + "_menu";
		$(this).mouseenter({menuID: menuID}, popup_Menu);
	});

	$("#header_logo").click(function(){
		window.location.replace('/');
	});


	$("#cart_link").click(function(){
		window.location.replace('/cart');
	});

	$("#user_link").click(function(){
		window.location.replace('/login');
	});

	
	if($("#logout_link")){
		$("#logout_link").click(function(){
			window.location.replace('/auth/logout');
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



function close_Menu(event){
	var menuID = event.data.menuID
	$(menuID).css('display',"none");
}


