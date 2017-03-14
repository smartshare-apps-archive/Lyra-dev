// contains core functionality for settings section
// this file specifically manages submenu navigation event binding 



$(document).ready(function(){
	bindMenuButtons();

});


function bindMenuButtons(){
	var subNavMenuButtons = $(".li_sub_nav_link");
	subNavMenuButtons.click(goToLink);

}


function goToLink(event){
	page = event.target.id;
	
	if (page == "li_link_settings_main"){
		window.location.replace("/control/settings/");
	}
	else if (page == "li_link_settings_payment"){
		window.location.replace("/control/settings/payment");
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
