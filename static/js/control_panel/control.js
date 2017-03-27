// global control panel functions


// global element handles
var li_products;
var li_orders;
var li_customers;
var li_settings;

$(document).ready(function(){
	bindGlobalElements();
	bindMainMenuEvents();

});


function bindGlobalElements(){
	li_products = $("#li_products");
	li_orders = $("#li_orders");
	li_customers = $("#li_customers")
	li_settings = $("#li_settings")
	li_store = $("#li_store")
	li_plugins = $("#li_plugins")
}

function bindMainMenuEvents(){
	li_products.click(productRedirect);
	li_orders.click(orderRedirect);
	li_customers.click(customerRedirect);
	li_settings.click(settingsRedirect);
	li_store.click(storeSettingsRedirect);
	li_plugins.click(pluginsRedirect);

	$(".sidebar-nav").hover(openFullMenu, closeFullMenu);
}


function openFullMenu(){
	//$(".sidebar-nav").css("width","200px");
}

function closeFullMenu(){
	//$(".sidebar-nav").css("width","100px");
}


function productRedirect(){
	window.location.href = "/control/products/";
}

function orderRedirect(){
	window.location.href = "/control/orders/";
}

function customerRedirect(){
	window.location.href = "/control/customers/";
}


function settingsRedirect(){
	window.location.href = "/control/settings/";
}

function storeSettingsRedirect(){
	window.location.href = "/control/store/";
}

function pluginsRedirect(){
	window.location.href = "/control/plugins/";
}



