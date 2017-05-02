
var btn_saveSetting;


// this container is passed to action db



$(document).ready(function(){
	bindElements();
	bindEvents();
	console.log("Loaded script.");
});


function bindElements(){

	btn_saveSetting = $("#btn_saveSetting");
}



function bindEvents(){
	
}






function confirmSettings(event){
	var setting_id = event.data.setting_id;

	btn_saveSetting.unbind();


	

}
