// contains core functionality for product section
// this file specifically manages submenu navigation event binding 

var selectedProducts = {};
var selectedOrders = {};


$(document).ready(function(){
	bindMenuButtons();


});


function bindMenuButtons(){
	var subNavMenuButtons = $(".li_sub_nav_link");
	subNavMenuButtons.click(goToLink);

}


function goToLink(event){
	page = event.target.id;
	
	if (page == "li_link_products_main"){
		window.location.replace("/control/products/");
	}
	else if(page == "li_link_products_inventory"){
		window.location.replace("/control/products/inventory/");
	}
	else if(page == "li_link_products_collections"){
		window.location.replace("/control/products/collections/");
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
