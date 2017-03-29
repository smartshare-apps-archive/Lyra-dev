$(document).ready(function(){

bindElements();
bindEvents();

});


function bindElements(){
	$(".btn-run-plugin").each(function(){
		var plugin_id = $(this).attr('data-pluginID');
		var plugin_name = $(this).attr('data-pluginName');

		$(this).click({plugin_id: plugin_id}, run_PyUtil);
	});


}

function run_PyUtil(event){
	var plugin_id = event.data.plugin_id;

	window.location.href = "/control/plugins/pyutil/" + plugin_id
}


function bindEvents(){

}