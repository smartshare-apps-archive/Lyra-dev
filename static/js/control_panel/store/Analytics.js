
var btn_saveSetting;


// this container is passed to action db



$(document).ready(function(){
	bindElements();
	setupScriptEditor();

	bindEvents();


	console.log("Loaded script.");
});


function bindElements(){

	btn_saveSetting = $("#btn_saveSetting");
}



function bindEvents(){
	var initialAnalyticsScript = $("#initialAnalyticsScript").val();

	$('#analytics_script_input').on('summernote.change', function(e) {
		console.log("changed");
	});

	$("#analytics_script_input").summernote('code', initialAnalyticsScript);

}


function setupScriptEditor(){
	$('#analytics_script_input').summernote({
		  height: 175,                 // set editor height
		  minHeight: 175,             // set minimum height of editor
		  maxHeight: 500,             // set maximum height of editor
		  focus: false                  // set focus to editable area after initializing summernote
	});
	
	$("#analytics_script_input").summernote('codeview.toggle');
}







function confirmSettings(event){
	var setting_id = event.data.setting_id;

	btn_saveSetting.unbind();


	

}
