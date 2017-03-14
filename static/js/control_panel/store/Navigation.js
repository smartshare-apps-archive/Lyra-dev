var btn_viewStore;
var btn_saveNavigationSettings;
var btn_addNavCategory;

var navData = {};
var formattedNavData = {};
var selectedNavCategory = null;


$(document).ready(function(){
	bindElements();
	bindEvents();

	getNavData();

	var default_selection = $("#table_navCategories").find(".row_nav_category");
	selectedNavCategory = default_selection.attr('data-navCategory');
	selectNavCategory(selectedNavCategory);


});



function bindElements(){
	btn_viewStore = $("#btn_viewStore");
	btn_saveNavigationSettings = $("#btn_saveNavigationSettings");
	btn_addNavCategory = $("#btn_addNavCategory");
}



function bindEvents(){
	btn_viewStore.unbind();
	btn_viewStore.click(redirect_Store);
	

	$(".selectTableItem").each(function(){
		$(this).unbind();

		var nav_category = $(this).attr('data-navCategory');
		//console.log(nav_category);

		$(this).change({nav_category: nav_category}, passNavCategory);
	});

	btn_saveNavigationSettings.unbind();
	btn_saveNavigationSettings.click(saveNavigationSettings);

	$(".btn_delete_nav_category").each(function(){
		$(this).unbind();

		var nav_category = $(this).attr('data-navCategory');
		$(this).click({nav_category:nav_category}, deleteNavCategory);
		
	});

	btn_addNavCategory.unbind();
	btn_addNavCategory.click(createNavCategory);

	$(".rename_category").each(function(){
		$(this).unbind();
		var nav_category = $(this).attr('data-navCategory');
		$(this).change({nav_category: nav_category}, renameNavCategory);
	});

}


function createNavCategory(event){
	var new_nav_category = $("#input_navCategory").val();
	var new_categoryType = $("#input_categoryType").val();

	console.log(new_categoryType);

	if (new_nav_category == ""){
		return false;
	}

	var templateHTML = "<tr class=\"row_nav_category\" data-navCategory=\"" + new_nav_category + "\">" +
		"<td class=\"td_select\">" + 
		"<label class=\"btn btn-default select_container\">" + 
		"<input type=\"checkbox\" class=\"selectTableItem\" data-navCategory=\"" + new_nav_category + "\">" + 
		"</label>" + 
		"</td>" + 
		"<td class=\"text-center\">" + 
		"<input type=\"text\" class=\"form-control rename_category\" value=\"" + new_nav_category + "\" data-navCategory=\"" + new_nav_category + "\">" + 
		"</td>";

		if (new_categoryType == "single_link"){
			templateHTML += "<input type=\"hidden\" class=\"nav_data single\" data-navCategory=\"" + new_nav_category + "\" value=\"/\">";

		}

		else if (new_categoryType == "dropdown"){
			templateHTML += "<input type=\"hidden\" class=\"nav_data dropdown\" data-navCategory=\"" + new_nav_category + "\" value=\"title:default;default:/\">";

		}


	templateHTML += "<td class=\"text-center\">" +  									
					"<select class=\"form-control\">";

	if (new_categoryType == "single_link"){
		templateHTML += "<option value=\"dropdown\"> Dropdown </option>" +  
						"<option value=\"single_link\" selected> Single Link </option>";
	}

	else if (new_categoryType == "dropdown"){
		templateHTML += "<option value=\"dropdown\" selected> Dropdown </option>" +  
						"<option value=\"single_link\"> Single Link </option>";
	}

		templateHTML += "</select>" + 
		"</td>" + 
		"<input type=\"hidden\" class=\"initial_category\" data-navCategory=\"" + new_nav_category + "\" value=\"" + new_nav_category + "\">" + 
		"<td>" +  
		"<button type=\"button\" class=\"btn btn-danger btn_delete_nav_category\" data-navCategory=\""+ new_nav_category + "\"> &nbsp; <span class=\"glyphicon glyphicon-minus-sign\"></span> &nbsp;" 
		"</td>" + 
		"</tr>";

	$("#nav_categories_body").append(templateHTML);

	createNavData(new_nav_category);
	bindEvents();
}


function deleteNavCategory(event){
	var nav_category = event.data.nav_category;

	var selectorString = '[data-navCategory="' + nav_category + '"]';
	var nav_row = $("tr"+selectorString);
	nav_row.remove();
	navData[nav_category]["action"] = "delete";
}


function passNavCategory(event){
	var nav_category = event.data.nav_category;
	selectNavCategory(nav_category);
}


function selectNavCategory(nav_category){
	var selectorString = 'input:checkbox[data-navCategory="' + nav_category + '"]';
	var chk_box = $(selectorString);
	selectedNavCategory = nav_category;

	$(".selectTableItem").each(function(){
		if($(this).attr('data-navCategory') != chk_box.attr('data-navCategory')){
			$(this).prop("checked",false);
		}
	});


	$("#span_nav_category").html(nav_category);

	if(navData[nav_category]["type"] == "single_link"){
		$("#single_link_input").val(navData[nav_category]["data"]);

		$("#nav_data_dropdown_list").slideUp("fast");
		$("#nav_data_single_link").slideDown("fast");

		$("#single_link_input").unbind();
		$("#single_link_input").change({nav_category: nav_category}, updateNavData);
	}
	else if (navData[nav_category]["type"] == "dropdown_list"){
		$("#nav_data_dropdown_list").slideDown("fast");
		$("#nav_data_single_link").slideUp("fast");
		var parsed_dropdown_data = parseDropdownData(navData[nav_category]["data"]);

		$("#dropdown_list_input").html("");
		
		dropDownMenuData = {};

		var dropDownTitle = parsed_dropdown_data["title"];

		$("#dropdown_title_input").val(dropDownTitle);
		
		$("#dropdown_link_container").html("");

		for(var link in parsed_dropdown_data){
			if (link == "title") { continue; }
			var currentHTML = "";

			currentHTML += "<input type=\"text\" class=\"form-control nav_edit input_link_label\" value=\"" + link + "\">";
			var uri = parsed_dropdown_data[link];	

			currentHTML += "<input type=\"text\" class=\"form-control nav_edit input_link_href\" value=\"" + uri + "\">";
			currentHTML += "<br>";

			$("#dropdown_link_container").append(currentHTML);
		}


		$(".input_link_label").each(function(){
			var nav_category = $("#span_nav_category").html();
			$(this).unbind();
			$(this).change({nav_category: nav_category}, updateNavData);
		});

		$(".input_link_href").each(function(){
			var nav_category = $("#span_nav_category").html();
			$(this).unbind();
			$(this).change({nav_category: nav_category}, updateNavData);
		});

		$("#dropdown_title_input").unbind();
		$("#dropdown_title_input").change({nav_category: nav_category}, updateNavData);

	}
		
	if (!chk_box.is(":checked")){
		chk_box.prop("checked",true);
	}

}


function renameNavCategory(event){

	if (nav_category in navData){
		return false;
	} 

	var nav_category = event.data.nav_category;
	var selectorString = '[data-navCategory="' + nav_category + '"]';


	var target_input = $("input:text"+ selectorString);
	var new_name = target_input.val();

	var nav_data_cont = $("input:hidden"+selectorString);
	var chk_cont = $("input:checkbox" + selectorString);
	var row_cont = $('tr' + selectorString);

	navData[new_name] = navData[nav_category];
	delete navData[nav_category];

	chk_cont.attr('data-navCategory',new_name);
	nav_data_cont.attr('data-navCategory',new_name);
	row_cont.attr('data-navCategory',new_name);
	target_input.attr('data-navCategory',new_name);

	chk_cont.unbind();
	target_input.unbind();

	chk_cont.change({nav_category: new_name}, passNavCategory);
	target_input.change({nav_category: new_name}, renameNavCategory);

	selectNavCategory(new_name);
}



function updateNavData(event){
	var nav_category = event.data.nav_category;

	if (navData[nav_category]["type"] == "dropdown_list"){

		var c_title = $("#dropdown_title_input").val();

		navData[nav_category]["data"] = "title:" + c_title + ";";

		$(".input_link_label").each(function(){
			navData[nav_category]["data"] += $(this).val();
			navData[nav_category]["data"] += ":" + $(this).next(".input_link_href").val() + ";";
		});
		navData[nav_category]["data"] = navData[nav_category]["data"].slice(0,-1);

	}
	else if (navData[nav_category]["type"] == "single_link"){
		navData[nav_category]["data"] = $("#single_link_input").val();
	}
	console.log(navData);
}




function parseDropdownData(data){
	data = data.split(';')
	parsedData = {};

	for (var i=0;i<data.length;i++){
		var splitData = data[i].split(':');
		parsedData[splitData[0]] = splitData[1];
	}

	return parsedData;
}



function getNavData(){
	$(".row_nav_category").each(function(){
		var navCategory = $(this).attr('data-navCategory');
 		var nav_data = $(this).find(".nav_data");
 		var resource_id = $(this).find(".resource_id").val();
 		var initial_category = $(this).find(".initial_category").val();

 		navData[navCategory] = {}

 		if (nav_data.hasClass("dropdown")){
 			navData[navCategory]["type"] = "dropdown_list";
 		}
 		else if (nav_data.hasClass("single")){
 			navData[navCategory]["type"] = "single_link";
 		}

 		navData[navCategory]["data"] = nav_data.val();
 		navData[navCategory]["resource_id"] = resource_id;
 		navData[navCategory]["initial_category"] = initial_category;
 		navData[navCategory]["action"] = "update";
	});
}



function createNavData(navCategory){
		var selectorString = '[data-navCategory="' + navCategory + '"]';
		var navCategoryRow = $("tr" + selectorString);
 		var nav_data = $(navCategoryRow).find(".nav_data");
 		var initial_category = $(navCategoryRow).find(".initial_category").val();

 		navData[navCategory] = {}

 		if (nav_data.hasClass("dropdown")){
 			navData[navCategory]["type"] = "dropdown_list";
 		}
 		else if (nav_data.hasClass("single")){
 			navData[navCategory]["type"] = "single_link";
 		}

 		navData[navCategory]["data"] = nav_data.val();
 		navData[navCategory]["resource_id"] = "new";
 		navData[navCategory]["initial_category"] = initial_category;
 		navData[navCategory]["action"] = "insert";

 		console.log(navData);
}

function redirect_Store(){
	window.location.href = '/';

}