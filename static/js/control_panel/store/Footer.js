var btn_viewStore;
var btn_saveFooterSettings;
var btn_addFooterCategory;

var footerData = {};
var formattedFooterData = {};
var selectedFooterCategory = null;


$(document).ready(function(){
	bindElements();
	bindEvents();

	getFooterData();

	var default_selection = $("#table_footerCategories").find(".row_footer_category");
	selectedFooterCategory = default_selection.attr('data-footerCategory');
	
	setupHeaderEditor();
	selectFooterCategory(selectedFooterCategory);


});



function bindElements(){
	btn_viewStore = $("#btn_viewStore");
	btn_saveFooterSettings = $("#btn_saveFooterSettings");
	btn_addFooterCategory = $("#btn_addFooterCategory");
}



function bindEvents(){
	btn_viewStore.unbind();
	btn_viewStore.click(redirect_Store);
	

	$(".selectTableItem").each(function(){
		$(this).unbind();

		var footer_category = $(this).attr('data-footerCategory');
		//console.log(footer_category);

		$(this).change({footer_category: footer_category}, passFooterCategory);
	});

	btn_saveFooterSettings.unbind();
	btn_saveFooterSettings.click(saveFooterSettings);

	$(".btn_delete_footer_category").each(function(){
		$(this).unbind();

		var footer_category = $(this).attr('data-footerCategory');
		$(this).click({footer_category:footer_category}, deleteFooterCategory);
		
	});

	btn_addFooterCategory.unbind();
	btn_addFooterCategory.click(createFooterCategory);

	$(".rename_category").each(function(){
		$(this).unbind();
		var footer_category = $(this).attr('data-footerCategory');
		$(this).change({footer_category: footer_category}, renameFooterCategory);
	});

}


function setupHeaderEditor(){
	$('#dropdown_title_input').summernote({
		  height: 175,                 // set editor height
		  minHeight: 175,             // set minimum height of editor
		  maxHeight: 500,             // set maximum height of editor
		  focus: false                  // set focus to editable area after initializing summernote
	});
}



function createFooterCategory(event){
	var new_footer_category = $("#input_footerCategory").val();

	if (new_footer_category == ""){
		return false;
	}

	var templateHTML = "<tr class=\"row_footer_category\" data-footerCategory=\"" + new_footer_category + "\">" +
		"<td class=\"td_select\">" + 
		"<label class=\"btn btn-default select_container\">" + 
		"<input type=\"checkbox\" class=\"selectTableItem\" data-footerCategory=\"" + new_footer_category + "\">" + 
		"</label>" + 
		"</td>" + 
		"<td class=\"text-center\">" + 
		"<input type=\"text\" class=\"form-control rename_category\" value=\"" + new_footer_category + "\" data-footerCategory=\"" + new_footer_category + "\">" + 
		"</td>";


		templateHTML += "<input type=\"hidden\" class=\"footer_data dropdown\" data-footerCategory=\"" + new_footer_category + "\" value=\"title:default<split>default:/\">";

		

	templateHTML += "<input type=\"hidden\" class=\"initial_category\" data-footerCategory=\"" + new_footer_category + "\" value=\"" + new_footer_category + "\">" + 
	"<td>" +  
	"<button type=\"button\" class=\"btn btn-danger btn_delete_footer_category\" data-footerCategory=\""+ new_footer_category + "\"> &nbsp; <span class=\"glyphicon glyphicon-minus-sign\"></span> &nbsp;" 
	"</td>" + 
	"</tr>";

	$("#footer_categories_body").append(templateHTML);

	createFooterData(new_footer_category);
	bindEvents();
}


function deleteFooterCategory(event){
	var footer_category = event.data.footer_category;

	var selectorString = '[data-footerCategory="' + footer_category + '"]';
	var footer_row = $("tr"+selectorString);
	footer_row.remove();
	footerData[footer_category]["action"] = "delete";
}


function passFooterCategory(event){
	var footer_category = event.data.footer_category;
	selectFooterCategory(footer_category);

}


function selectFooterCategory(footer_category){
	console.log("Selecting: " + footer_category);

	var selectorString = 'input:checkbox[data-footerCategory="' + footer_category + '"]';
	var chk_box = $(selectorString);
	
	selectedNavCategory = footer_category;

	$(".selectTableItem").each(function(){
		if($(this).attr('data-footerCategory') != chk_box.attr('data-footerCategory')){
			$(this).prop("checked",false);
		}
	});


	$("#span_footer_category").html(footer_category);
	

	var parsed_dropdown_data = parseDropdownData(footerData[footer_category]["data"]);
	console.log("New parsed dropdown data: " + parsed_dropdown_data);

	$("#dropdown_list_input").html("");
	
	dropDownMenuData = {};


	var dropDownTitle = parsed_dropdown_data["title"];
	

	$("#dropdown_link_container").html("");

	for(var link in parsed_dropdown_data){
		if (link == "title") { continue; }
		var uri = parsed_dropdown_data[link];	

		var currentHTML = "";

		currentHTML += "<div class=\"dropdown_link_cont\" data-footerCategory=\"" + footer_category + "\" data-dropdownLink=\"" + link + "\">";
		currentHTML += "<input type=\"text\" class=\"form-control footer_edit input_link_label\" value=\"" + link + "\">";
		

		currentHTML += "<input type=\"text\" class=\"form-control footer_edit input_link_href\" value=\"" + uri + "\">";
		currentHTML += "<button type=\"button\" class=\"btn btn-danger btn_delete_footer_link\" data-dropdownLink=\"" + link + "\"> <span class=\"glyphicon glyphicon-minus-sign\"> </span> </button>";
		currentHTML += "</div>";


		$("#dropdown_link_container").append(currentHTML);
	}


	$("#btn_addFooterLink").unbind();
	$("#btn_addFooterLink").click({footer_category: footer_category}, addCategoryLink);

	$(".input_link_label").each(function(){
		var footer_category = $("#span_footer_category").html();
		$(this).unbind();
		$(this).change({footer_category: footer_category}, updateFooterData);
	});

	$(".input_link_href").each(function(){
		var footer_category = $("#span_footer_category").html();
		$(this).unbind();
		$(this).change({footer_category: footer_category}, updateFooterData);
	});

	$(".btn_delete_footer_link").each(function(){
		var footer_link = $(this).attr('data-dropdownLink');
		$(this).click({footer_link:footer_link}, deleteFooterLink);
	})

	$("#dropdown_title_input").unbind();

	$('#dropdown_title_input').on('summernote.change', {footer_category: footer_category}, function(e) {
		updateFooterData(e);
	});

	$("#dropdown_title_input").summernote('code', dropDownTitle);

	if (!chk_box.is(":checked")){
		chk_box.prop("checked",true);
	}

}


function renameFooterCategory(event){

	if (footer_category in footerData){
		return false;
	} 

	var footer_category = event.data.footer_category;
	var selectorString = '[data-footerCategory="' + footer_category + '"]';


	var target_input = $("input:text"+ selectorString);
	var new_name = target_input.val();

	var footer_data_cont = $("input:hidden"+selectorString);
	var chk_cont = $("input:checkbox" + selectorString);
	var row_cont = $('tr' + selectorString);

	footerData[new_name] = footerData[footer_category];
	delete footerData[footer_category];

	chk_cont.attr('data-footerCategory',new_name);
	footer_data_cont.attr('data-footerCategory',new_name);
	row_cont.attr('data-footerCategory',new_name);
	target_input.attr('data-footerCategory',new_name);

	chk_cont.unbind();
	target_input.unbind();

	chk_cont.change({footer_category: new_name}, passFooterCategory);
	target_input.change({footer_category: new_name}, renameFooterCategory);

	selectFooterCategory(new_name);
}


function addCategoryLink(event){
	var footer_category = event.data.footer_category;
	var new_link = $("#dropdown_link_input").val();
	if (new_link == ""){ return false; }
	var default_uri = "/";


	currentHTML = "";
	currentHTML += "<div class=\"dropdown_link_cont\" data-footerCategory=\"" + footer_category + "\" data-dropdownLink=\"" + new_link + "\">";
	currentHTML += "<input type=\"text\" class=\"form-control footer_edit input_link_label\" value=\"" + new_link + "\">";
	currentHTML += "<input type=\"text\" class=\"form-control footer_edit input_link_href\" value=\"" + default_uri + "\">";
	currentHTML += "<button type=\"button\" class=\"btn btn-danger btn_delete_footer_link\" data-dropdownLink=\"" + new_link + "\"> <span class=\"glyphicon glyphicon-minus-sign\"> </span> </button>";
	currentHTML += "</div>";

	$("#dropdown_link_container").append(currentHTML);


	$(".input_link_label").each(function(){
		var footer_category = $("#span_footer_category").html();
		$(this).unbind();
		$(this).change({footer_category: footer_category}, updateFooterData);
	});

	$(".input_link_href").each(function(){
		var footer_category = $("#span_footer_category").html();
		$(this).unbind();
		$(this).change({footer_category: footer_category}, updateFooterData);
	});

	$(".btn_delete_footer_link").each(function(){
		var footer_link = $(this).attr('data-dropdownLink');
		var footer_category = $(this).attr('data-footerCategory');

		$(this).click({footer_link:footer_link}, deleteFooterLink);
	})


	$("#dropdown_link_input").val("");

	updateFooterData(event);

}

function deleteFooterLink(event){
	var footer_link = event.data.footer_link;
	var selectorString = '[data-dropdownLink="' + footer_link + '"]';
	var footer_link_cont = $("div"+selectorString)
	var footer_category = footer_link_cont.attr('data-footerCategory');
	event.data.footer_category = footer_category;

	footer_link_cont.remove();
	updateFooterData(event);
}




function updateFooterData(event){
	var footer_category = event.data.footer_category;
	console.log("Updating: " + footer_category);

	if (footerData[footer_category]["type"] == "dropdown_list"){

		var c_title = $("#dropdown_title_input").summernote('code');
		console.log(footerData);	
		footerData[footer_category]["data"] = "title:" + c_title + "<split>";

		$(".input_link_label").each(function(){
			footerData[footer_category]["data"] += $(this).val();
			footerData[footer_category]["data"] += ":" + $(this).next(".input_link_href").val() + "<split>";
		});
		footerData[footer_category]["data"] = footerData[footer_category]["data"].slice(0,-7);

	}
	else if (footerData[footer_category]["type"] == "single_link"){
		footerData[footer_category]["data"] = $("#single_link_input").val();
	}

	//console.log(footerData);	

}




function parseDropdownData(data){
	data = data.split('<split>')
	parsedData = {};

	for (var i=0;i<data.length;i++){
		var splitData = data[i].split(':');
		parsedData[splitData[0]] = splitData[1];
	}

	return parsedData;
}



function getFooterData(){
	$(".row_footer_category").each(function(){
		var footerCategory = $(this).attr('data-footerCategory');
 		var footer_data = $(this).find(".footer_data");
 		var resource_id = $(this).find(".resource_id").val();
 		var initial_category = $(this).find(".initial_category").val();

 		footerData[footerCategory] = {}

 		if (footer_data.hasClass("dropdown")){
 			footerData[footerCategory]["type"] = "dropdown_list";
 		}

 		footerData[footerCategory]["data"] = footer_data.val();
 		footerData[footerCategory]["resource_id"] = resource_id;
 		footerData[footerCategory]["initial_category"] = initial_category;
 		footerData[footerCategory]["action"] = "update";
	});
}




function createFooterData(footerCategory){
		var selectorString = '[data-footerCategory="' + footerCategory + '"]';
		var footerCategoryRow = $("tr" + selectorString);
 		var footer_data = $(footerCategoryRow).find(".footer_data");
 		var initial_category = $(footerCategoryRow).find(".initial_category").val();

 		footerData[footerCategory] = {}

 		if (footer_data.hasClass("dropdown")){
 			footerData[footerCategory]["type"] = "dropdown_list";
 		}

 		footerData[footerCategory]["data"] = footer_data.val();
 		footerData[footerCategory]["resource_id"] = "new";
 		footerData[footerCategory]["initial_category"] = initial_category;
 		footerData[footerCategory]["action"] = "insert";
}


function redirect_Store(){
	window.location.href = '/';

}