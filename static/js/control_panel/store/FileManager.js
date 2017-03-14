var minimumScroll = 0;
var isPositionFixed = false;
var actionBar;
var selectAll = true;
var selectedFiles = {};

$(document).ready(function(){
	bindElements();
	bindEvents();
	loadFileThumbnails();

});


function bindElements(){


}

function bindEvents(){

	$(".row_resource").each(function(){
		var resource_id = $(this).attr('data-resourceID');
		$(this).find(".selectTableItem").change({resource_id: resource_id}, selectFile);
	});

	$("#select_all_files").change(toggleAllFiles);

	$("#select_filename").change(function(){
		var filename = $(this).val().split('\\');
		var pathLength = filename.length;
		filename = filename[pathLength-1];

		$("#input_filename").val(filename);
		
	});


	$(".btn_bulk_delete_files").click(bulkDeleteFiles);

}


function setupActionBar(){
	actionBar = $("#file_action_bar");

	$(window).scroll(function(){
		var top = $(this).scrollTop();

		if(top > minimumScroll && isPositionFixed == false){
		isPositionFixed = true;
		actionBar.css("position","fixed");
		actionBar.css("top","0px");
		}
		else if(top < minimumScroll && isPositionFixed == true){
		isPositionFixed = false;
		actionBar.css("position","absolute");
		actionBar.css("top",minimumScroll+"px");
		}

	});

}



function selectFile(event){
	var resource_id = event.data.resource_id;

	var deleteKey = false;		// holds delete/add state
	var selectorString = '[data-resourceID="' + resource_id + '"]';

	event.stopPropagation();

	selectedFileCheckbox = $("input:checkbox" + selectorString);

	if (resource_id in selectedFiles){
		deleteKey = true;
		delete selectedFiles[resource_id]
	}
	else{
		selectedFiles[resource_id] = resource_id;
	}

	// this ensures that checkboxes in every customer table are updated to reflect the current selection state
	selectedFileCheckbox.each(function(){
		if (deleteKey){
			$(this).prop("checked",false);
		}
		else{
			$(this).prop("checked",true);
		}

	});

	var nOrders = Object.keys(selectedFiles).length;

	if (nOrders > 0){
		$("#file_action_bar").css("display","inline");
		
		if(nOrders == 1){
			$("#n_files_selected").html("<b>" + nOrders + "</b> file selected ");
		}
		else{
			$("#n_files_selected").html("<b>" + nOrders + "</b> files selected ");

		}
	}
	else if (nOrders == 0){
		$("#file_action_bar").css("display","none");
	}
}



// toggles all files either selected or deselected
function toggleAllFiles(){
	var resourceIDList = $("#resourceIDList").val().split(',');
	resourceIDList.pop();
	

	for(var i=0;i<resourceIDList.length;i++){
		var resource_id = resourceIDList[i];

		if(selectAll == true){
			selectedFiles[resource_id] = resource_id;
		}
		else{
			if (resource_id in selectedFiles){
				delete selectedFiles[resource_id];
			}
		}
	}

	if(selectAll){
		$(".selectTableItem").each(function(){
			$(this).prop('checked',true);
		});
	}
	else{
		$(".selectTableItem").each(function(){
			$(this).prop('checked',false);
		});
	}

	var nFiles = Object.keys(selectedFiles).length;

	if (nFiles > 0){
		$("#file_action_bar").css("display","inline");
		
		if(nFiles == 1){
			$("#n_files_selected").html("<b>" + nFiles + "</b> file selected ");
		}
		else{
			$("#n_files_selected").html("<b>" + nFiles + "</b> files selected ");

		}

	}
	else if (nFiles == 0){
		$("#file_action_bar").css("display","none");
	}

	selectAll = !selectAll;
}

function loadFileThumbnails(){
	$(".row_resource").each(function(){
		var resource_id = $(this).attr('data-resourceID');
		var resource_uri = $(this).find('.resource_uri').html();
		//var thumbnail_cont = $(this).find('.thumbnail');

		/*
		if (thumbnail_cont.hasClass("image_40")){
			var bg_url = "url('" + resource_uri + "')";
			thumbnail_cont.css('background-image', bg_url);
		}
		else if(thumbnail_cont.hasClass("generic_40")){

		}
		*/
	});
}