$(document).ready(function(){
	bindMenuButtons();

});


function bindMenuButtons(){
	var subNavMenuButtons = $(".li_sub_nav_link");
	subNavMenuButtons.click(goToLink);

}



function goToLink(event){
	page = event.target.id;
	
	if (page == "li_link_dashboard_main"){
		window.location.replace("/control/");
	}
	
	else if (page == "li_link_dashboard_live_chat"){
		window.location.replace("/control/live_chat");
	}

	else{
		alert('not ready yet');
	}
}


function replaceAll(str, find, replace) {
  return str.replace(new RegExp(find, 'g'), replace);
}


function doNothing(event){
	event.stopPropagation();
}
