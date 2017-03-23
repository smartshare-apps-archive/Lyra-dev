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
	
	if (page == "li_link_store_settings_main"){
		window.location.href = "/control/store/";
	}
	else if(page == "li_link_store_settings_navigation"){
		window.location.href = "/control/store/navigation";
	}
	else if(page == "li_link_store_settings_footer"){
		window.location.href = "/control/store/footer";
	}
	else if(page == "li_link_store_settings_pages"){
		window.location.href = "/control/store/pages";
	}

	else if(page == "li_link_store_settings_file_manager"){
		window.location.href = "/control/store/file_manager";
	}

	else if(page == "li_link_store_settings_theme_manager"){
		window.location.href = "/control/store/theme_manager";
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
