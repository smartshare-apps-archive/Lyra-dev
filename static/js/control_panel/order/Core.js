// contains core functionality for order section
// this file specifically manages submenu navigation event binding 
var selectedOrders = {};
var selectedProducts = {};
var selectedCustomers = {};


$(document).ready(function(){
	bindMenuButtons();

});


function bindMenuButtons(){
	var subNavMenuButtons = $(".li_sub_nav_link");
	subNavMenuButtons.click(goToLink);

}



function goToLink(event){
	page = event.target.id;
	
	if (page == "li_link_orders_main"){
		window.location.replace("/control/orders/");
	}
	else if(page == "li_link_orders_drafts"){
		window.location.replace("/control/orders/drafts");
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
