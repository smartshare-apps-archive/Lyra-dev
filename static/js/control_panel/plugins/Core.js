


$(document).ready(function(){
	bindMenuButtons();

});


function bindMenuButtons(){
	var subNavMenuButtons = $(".li_sub_nav_link");
	subNavMenuButtons.click(goToLink);

}



function goToLink(event){
	page = event.target.id;
	
	if (page == "li_link_plugins_main"){
		window.location.replace("/control/plugins/");
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
