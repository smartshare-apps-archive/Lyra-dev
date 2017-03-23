// btn bindings
var btn_savePageData;

var pageData = {}

$(document).ready(function(){
	setupDescriptionEditor();

	bindElements();
	bindEvents();
	populatePageData();

	console.log(pageData);

});


function bindElements(){
	btn_savePageData = $("#btn_savePageData");
	btn_deletePage = $("#btn_deletePage");

}


function bindEvents(){
	$('#input_PageHTML').on('summernote.change', function(e) {
 		pageData["content"] = $('#input_PageHTML').summernote('code');
 		console.log(pageData);

	});	

	$(".editor_input").each(function(){
		var field_id = $(this).attr('data-fieldID');
		$(this).change({field_id: field_id}, updatePageData);

	});

	btn_savePageData.click(savePageData);
	btn_deletePage.click(deletePage);
	
}


function updatePageData(event){
	var field_id = event.data.field_id;
	var selectorString = '[data-fieldID="' + field_id + '"]'

	pageData[field_id] = $(".editor_input" + selectorString).val();

}

function populatePageData(){
	$(".editor_input").each(function(){
		var field_id = $(this).attr('data-fieldID');
		pageData[field_id] = $(this).val();
	})

}


// setups the page editor with summernote and populates it with current page content
function setupDescriptionEditor(){
	$('#input_PageHTML').summernote({
		  height: 500,                 // set editor height
		  minHeight: 200,             // set minimum height of editor
		  maxHeight: 800,             // set maximum height of editor
		  focus: false                  // set focus to editable area after initializing summernote
		});

	var PageHTML = $("#page_content").val();
	$('#input_PageHTML').summernote('code', PageHTML);

	pageData["content"] =  PageHTML;


	$(".note-editor .note-editable").css("text-align","left");
}

