// global control panel functions



$(document).ready(function(){
	bindGlobalElements();
	bindMainMenuEvents();

});


function bindGlobalElements(){

}

function bindMainMenuEvents(){

	$(".sidebar-nav").hover(openFullMenu, closeFullMenu);
}


function openFullMenu(){
	//$(".sidebar-nav").css("width","200px");
}

function closeFullMenu(){
	//$(".sidebar-nav").css("width","100px");
}

