var btn_closeThemeEditor;
var btn_savePageThemes;
var btn_addSection;

var label_page_type;
var page_sections_container;
var page_preview_container;
var section_editor;

var pageData = {};
var pageIDList = [];

$(document).ready(function(){
	bindElements();
	bindEvents();
	getPageData();
	populatePageData();
});


function bindElements(){
	btn_closeThemeEditor = $("#btn_closeThemeEditor");
	btn_saveSection = $("#btn_saveSection");
	btn_savePageThemes = $("#btn_savePageThemes");
	btn_addSection = $("#btn_addSection");
	btn_addNewSection = $("#btn_addNewSection");

	label_page_type = $("#label_page_type");
	page_sections_container = $("#page_sections_container");

	page_preview_container = $("#page_preview_container");
	section_editor = $("#section_editor");

}


function bindEvents(){
	btn_closeThemeEditor.click(closeEditor);
	
	$("#select_page_id").change(populatePageData);
	btn_savePageThemes.click(savePageThemes);
}


function getPageData(){
	pageIDList = [];

	$(".page_data.page_id").each(function(){
		var page_id = $(this).attr('data-pageID');

		pageIDList.push(page_id);
		pageData[page_id] = {};

		var selectorString = '[data-pageID="' + page_id + '"]';

		var page_sections = $(".page_data.page_sections"+selectorString).val();
		var page_type = $(".page_data.page_type"+selectorString).val();
		var page_section_data = $(".page_data.page_section_data"+selectorString).val();

	
		// splits up the section data into data stored for each page section
		page_section_data = page_section_data.split('<section_split>');
		pageData[page_id]["section_data"] = {};	

		page_section_data = page_section_data.filter(removeEmpty);		// removes empty elements from the section list

		for (var i=0;i<page_section_data.length;i++){
			var section_data_split = page_section_data[i].split('<id_split>');	// splits each element in the list into section data and section id
			var section_id_data = section_data_split[0].split(':');
			
			var sectionID = section_id_data[0];
			var sectionTemplate = section_id_data[1];
			
			var sectionAnchorData = section_data_split[1].split('<split>');		// splits all the various anchors stored within that section

			pageData[page_id]["section_data"][sectionID] = {};
			pageData[page_id]["section_data"][sectionID]["section_template"] = sectionTemplate

			for(var j=0;j<sectionAnchorData.length;j++){
				var currentAnchor = sectionAnchorData[j].split('<anchor_id_split>');	// gets the current anchor ID
				var anchor_id = currentAnchor[0];
				var anchorTags = currentAnchor[1].split('<>');
				
				pageData[page_id]["section_data"][sectionID][anchor_id] = {};
				
				for(var k=0;k<anchorTags.length;k++){
						var anchor_tag = anchorTags[k].split('=');
						anchor_tag = [anchor_tag.shift(), anchor_tag.join('=')];	

						var tag_id = anchor_tag[0];
						var tag_value = anchor_tag[1];
						pageData[page_id]["section_data"][sectionID][anchor_id][tag_id] = tag_value;
					}
				}
			}
		
		pageData[page_id]["page_id"] = page_id;
		pageData[page_id]["type"] = page_type;
		pageData[page_id]["sections"] = page_sections.split(',');
	});

}



function populatePageData(){
	var page_id = $("#select_page_id").val();
	var selectorString = '[data-pageID="' + page_id + '"]'
	
	var page_sections = pageData[page_id]["sections"];
	var page_type = pageData[page_id]["type"];

	label_page_type.val(page_type);
	page_sections_container.html("");

	var sortableHTML = "<ul id=\"sortable_sections\"></ul>";

	page_sections_container.append(sortableHTML);

	var sortableContainer = $("#sortable_sections");

	for (var i=0;i<page_sections.length;i++){
		var section_id = page_sections[i];
		
		var currentHTML = "<li class=\"ui-state-default section-controls-container\" data-sectionID=\"" + section_id + "\">";
		currentHTML += "<div class=\"section-controls\" data-sectionID=\"" + section_id + "\">";
		
		currentHTML += "<button type=\"button\" class=\"btn btn-primary change-section-order\" data-sectionID=\"" + section_id + "\">" + "<span class=\"glyphicon glyphicon-th-large\"></span>" + "</button>";

		if(section_id != "content"){
			currentHTML += "<button type=\"button\" class=\"btn btn-primary section-edit\" data-sectionID=\"" + section_id + "\" data-toggle=\"modal\" data-target=\"#modal_editSection\">" + "<span class=\"glyphicon glyphicon-pencil\"></span>" + "</button>";
		}

		currentHTML += "<button type=\"button\" class=\"btn btn-default section-btn\">" + section_id + "</button>";

		if(section_id != "content"){
			currentHTML += "<button type=\"button\" data-toggle=\"modal\" data-target=\"#modal_deleteSection\" class=\"btn btn-danger section-delete\" data-sectionID=\"" + section_id + "\">" + "<span class=\"glyphicon glyphicon-minus-sign\"></span>" + "</button>";
		}

		currentHTML += "</div>";
		currentHTML += "</li>";

		sortableContainer.append(currentHTML);
	}

 
    $( "#sortable_sections" ).sortable({
    	handle: '.change-section-order',
    	cancel: ''
    });
    $( "#sortable_sections" ).disableSelection();

    $( "#sortable_sections" ).on( "sortupdate", function( event, ui ) {
    	updateSectionOrder(page_id);

    } );


	var page_url = "/page/" + page_id;

	$(".section-edit").each(function(){
		var sectionID = $(this).attr('data-sectionID');
		var sectionTemplate = pageData[page_id]["section_data"][sectionID]["section_template"];

		$(this).click({pageID: page_id, sectionID: sectionID, sectionTemplate:sectionTemplate}, populateSectionFields);
	});

	$(".section-delete").each(function(){
		var sectionID = $(this).attr('data-sectionID');

		$(this).click(function(){
			var btn_deleteSection = $("#btn_deleteSection");
			btn_deleteSection.unbind();

			btn_deleteSection.click({pageID: page_id, sectionID:sectionID}, deleteSection);
		});

	});


	page_preview_container.attr('src', page_url);
	btn_addNewSection.unbind();
	btn_addNewSection.click({page_id:page_id}, addSection);
}



//moves a sections rendering either up or down on the page
function updateSectionOrder(page_id){
	pageData[page_id]["sections"] = [];

	$("#sortable_sections").find(".section-controls").each(function(){
		var sectionID = $(this).attr('data-sectionID');
		pageData[page_id]["sections"].push(sectionID);
	});	
}


function setupDescriptionEditor(pageID, sectionID, anchorID){
	var selectorString = '[data-anchorID="' + anchorID + '"]';

	$('.text_editor'+selectorString).summernote({
		  height: 200,                 // set editor height
		  minHeight: 200,             // set minimum height of editor
		  maxHeight: 500,             // set maximum height of editor
		  focus: false                  // set focus to editable area after initializing summernote
		});


	$('.text_editor'+selectorString).on('summernote.change', function(e) {
 		var currentText = $('.text_editor'+selectorString).summernote('code');
 		pageData[pageID]["section_data"][sectionID][anchorID]["anchor_value"] = currentText;

	});	

	var anchorHTML = pageData[pageID]["section_data"][sectionID][anchorID]["anchor_value"];
	$('.text_editor'+selectorString).summernote('code', anchorHTML);

	//pageData["section_data"] =  PageHTML;
}


function setupResourceEditor(pageID, sectionID, anchorID){
	var selectorString = '[data-anchorID="' + anchorID + '"]';
	var currentResourceID = pageData[pageID]["section_data"][sectionID][anchorID]["anchor_value"];

	var resource_editor = $(".resource-editor" + selectorString);
	var selectResource = resource_editor.find(".select-image-resource");
	var imagePreview = resource_editor.find(".image-preview");

	$(".image_resource_uri").each(function(){
		var filename = $(this).attr('data-filename');
		var resource_id = $(this).attr('data-resourceID');
		var resource_uri = $(this).attr('data-resourceURI');

			selectResource.append($('<option>', {
			    value: resource_id,
			    text: filename + ":   " + resource_id
			}));

		if(resource_id == currentResourceID){
			imagePreview.css('background-image',"url('" + resource_uri + "')");
		}
	});

	selectResource.val(currentResourceID);

	selectResource.change(function(){
		var resource_id = $(this).val();
		var selectorString = '[data-resourceID="' + resource_id + '"]';
		var resource_uri = $(".image_resource_uri" + selectorString).attr('data-resourceURI');

		pageData[pageID]["section_data"][sectionID][anchorID]["anchor_value"] = resource_id;

		imagePreview.css('background-image',"url('" + resource_uri + "')");
	})

}



// populate the section editor modal with currently applicable fields
function populateSectionFields(event){
	var pageID = event.data.pageID;
	var sectionID = event.data.sectionID;
	var sectionTemplate = event.data.sectionTemplate;

	var selectorString = '[data-sectionID="' + sectionTemplate + '"]';
	var section_container = $(".rendered_section_body"+selectorString);	// finds the rendered template containing the html of a section
	// reset the contents of the section editor modal
	section_editor.html("");

	//go through the section template, looking for data insertion points
	section_container.find('.anchor').each(function(){

		var anchorID = $(this).attr('data-anchorID');
		
		//check what type of resource they are to allow for proper editor elements
		if($(this).hasClass('text-resource')){
			var currentHTML = "<h4> " + anchorID + ":</h4>";
			currentHTML += "<div class=\"text_editor\" data-anchorID=\"" +  anchorID + "\" contenteditable=\"true\" ></div><hr>";
			section_editor.append(currentHTML);
			setupDescriptionEditor(pageID, sectionID, anchorID);
		}
		else if($(this).hasClass('image-resource')){
			var currentHTML = "<h4> " + anchorID + ":</h4>";
			currentHTML += "<div class=\"resource-editor\" data-anchorID=\"" +  anchorID + "\">";
			currentHTML += "<div class=\"image-preview\"></div>";
			currentHTML += "<select class=\"form-control select-image-resource\">";
			currentHTML += "</select></div><hr>";

			section_editor.append(currentHTML);
			setupResourceEditor(pageID, sectionID, anchorID);

		}


	});
	btn_saveSection.unbind();

	btn_saveSection.click({page_id: pageID}, savePageSectionData);

}

function addSection(event){
	var page_id = event.data.page_id;
	var section_template = $("#select_section_snippet").val();
	var section_id = $("#new_section_id").val();

	// remove this fucking dumb shit soon
	if(section_id == "" || section_id in pageData[page_id]["sections"]){
		console.log("exists");
	}

	pageData[page_id]["section_data"][section_id] = {};
	pageData[page_id]["section_data"][section_id]["section_template"] = section_template;

	var selectorString = '[data-sectionID="' + section_template + '"]';
	var section_container = $(".rendered_section_body"+selectorString);	// finds the rendered template containing the html of a section

	section_container.find('.anchor').each(function(){
		var anchorID = $(this).attr('data-anchorID');
		//check what type of resource they are to allow for proper editor elements
		pageData[page_id]["section_data"][section_id][anchorID] = {};

		if($(this).hasClass('text-resource')){
			pageData[page_id]["section_data"][section_id][anchorID]["anchor_type"] = "text-resource";
		}
		else if($(this).hasClass('image-resource')){
			pageData[page_id]["section_data"][section_id][anchorID]["anchor_type"] = "image-resource";
		}

		pageData[page_id]["section_data"][section_id][anchorID]["anchor_value"] = "";
	});

	pageData[page_id]["sections"].push(section_id);


	populatePageData(); //re-renders the page as well as populates the section control dialogs


	savePageThemes(event);
}


function deleteSection(event){
	var page_id = event.data.pageID;
	var section_id = event.data.sectionID;
	var selectorString = '[data-sectionID="' + section_id + '"]';

	delete pageData[page_id]["section_data"][section_id];

	var currentIndex = pageData[page_id]["sections"].indexOf(section_id);

	pageData[page_id]["sections"].splice(currentIndex, 1);

	var containerToDelete = $(".section-controls-container" + selectorString);

	containerToDelete.remove();
	savePageThemes(event);
}



function closeEditor(){
	window.location.href = '/control/store/'	
}


function removeEmpty(value){
	return value != "";
}