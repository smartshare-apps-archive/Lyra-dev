var form_collection_conditions;
var rule_policy;

var conditionIDList = [];
var collectionData = {}

var collectionID;
var currentConditions = "";
var collection_description = "";

var defaultCondition = ["Title","isequalto",""]

var btn_saveCollection;
var btn_deleteCollection;
var btn_confirmCollectionChanges;
var btn_addCondition;


$(document).ready(function(){
	collectionID = $("#collection_id").val();

	bindElements();
	setupInitialConditions();
	remapConditions();
	setupDescriptionEditor();
	loadImages();

	btn_confirmCollectionChanges.click({collection_data: collectionData}, saveCollectionChanges);
	btn_saveCollection.click(updateCollectionData);


});


function clearEvents(){
	btn_addCondition.unbind();

	$(".condition_field").unbind();
	$(".select_collection_condition").unbind();
	$(".condition_input_field").unbind();

	$(".btn_remove_condition").each(function(){
		$(this).unbind();
	});

}


function bindEvents(){
	btn_addCondition.click(createNewCondition);

	$(".condition_field").change(replaceConditionInput);
	$(".select_collection_condition").change(formatConditions);
	$(".condition_input_field").change(formatConditions);

	// button event handling

	$(".btn_remove_condition").each(function(){
		$(this).click({conditionID:$(this).attr('id')}, removeCondition);
	});

	btn_deleteCollection.click({collection_id: collectionID}, deleteCollection);

	$('#collection_description_editor').on('summernote.change', function(e) {
		$("#collection_description").val($('#collection_description_editor').summernote('code'));
	});

}



function bindElements(){
	form_collection_conditions = $("#form_collection_conditions");
	rule_policy = $("#rule_policy");
	

	btn_addCondition = $("#btn_addCondition");
	btn_saveCollection = $("#btn_saveCollection")
	btn_deleteCollection = $("#btn_deleteCollection");
	btn_confirmCollectionChanges = $("#btn_confirmCollectionChanges")
}



function setupDescriptionEditor(){
	$('#collection_description_editor').summernote({
		  height: 200,                 // set editor height
		  minHeight: 200,             // set minimum height of editor
		  maxHeight: 250,             // set maximum height of editor
		  focus: false                  // set focus to editable area after initializing summernote
		});

	collection_description = $("#collection_description").val();
	$('#collection_description_editor').summernote('code', collection_description);

	updateCollectionData();
}



function setupInitialConditions(){
	$(".collection_condition").each(function(){
		var currentCondition = $(this).val();

		currentCondition = replaceAll(currentCondition,' ','');

		var currentConditionID = $(this).attr('id').split('_')[1];

		conditionIDList.push(currentConditionID);

		condition = currentCondition.slice(1,-1);
		condition = condition.split(',');
		
		field = condition[0].slice(1,-1);
		rule = condition[1].slice(1,-1);
		value = condition[2].slice(1,-1);


		condition = [field, rule, value];

		// build a template for each condition selector specific to it's ID 
		conditionTemplate = buildConditionTemplate(currentConditionID, condition=condition);

		// add the condition into the html of the collection condition form
		addCondition(currentConditionID, conditionTemplate, condition=condition);


	})

	rule_policy_value = rule_policy.val();
	
	if(rule_policy_value == 1){
		$("#radio_Strict").prop("checked","true");
		$("#radio_Lax").prop("checked","false");
	}
	else{
		$("#radio_Lax").prop("checked","true");
		$("#radio_Strict").prop("checked","false");
	}

	conditionIDList.sort();
}


// dynamically assembly the html for a collection condition 
function buildConditionTemplate(conditionID, condition=defaultCondition){
	conditionContainer = "<div class=\"condition_container\" id=\"condition_" + conditionID + "\">";
	conditionFieldTemplate = $("#condition_template").html();
	conditionRuleTemplate = $("#condition_rule_template").html();
	deleteConditionTemplate = $("#delete_condition_template").html();

	var field = condition[0];
	
	if(field == "Tags"){
		conditionInputTemplate = $("#condition_tag_selection").html();
		conditionInputTemplate = conditionInputTemplate.replace("tag_x", "tag_"+conditionID)
	}
	else{
		conditionInputTemplate = $("#condition_text_input").html();
		conditionInputTemplate = conditionInputTemplate.replace("input_x", "input_"+conditionID)
	}

	conditionFieldTemplate = conditionFieldTemplate.replace("field_x", "field_"+conditionID)
	conditionRuleTemplate = conditionRuleTemplate.replace("rule_x", "rule_"+conditionID)
	deleteConditionTemplate = deleteConditionTemplate.replace("_x","_"+conditionID);
	

	return conditionContainer + conditionFieldTemplate + conditionRuleTemplate + "<br><br>" + conditionInputTemplate + deleteConditionTemplate + "<hr></div>";

}



function createNewCondition(){
	var nConditions = conditionIDList.length;
	var newConditionID = (nConditions).toString();
	var newConditionTemplate = buildConditionTemplate(newConditionID);

	conditionIDList.push(newConditionID);
	
	addCondition(newConditionID, newConditionTemplate);
	
	clearEvents();
	bindEvents();

}



function removeCondition(event){
	conditionID = event.data.conditionID
	conditionContainer = $("#"+conditionID).parent();
	conditionContainer.remove();
	
	remapConditions();
}



// sorts out condition rules on the page to be in the proper order, allowing for easy dynamic editing
function remapConditions(){

	conditionIDList = [];
	nConditions = $(".condition_container").length;

	for(var i=0;i<nConditions;i++){
		conditionIDList.push(i.toString());
	}

	$(".condition_container").each(function(index){

		//temporarily store the previous condition attributes in these
		field = $(this).children(".condition_field").val();
		rule = $(this).children(".condition_rule").val();
		value = $(this).children(".condition_input_field").val();

		currentConditionID = $(this).attr('id').split('_')[1];
		
		beforeHTML = $(this).html()
		afterHTML = replaceAll(beforeHTML, "_"+currentConditionID, "_"+index)
		$(this).attr("id","condition_"+index);

		$(this).html(afterHTML);

		// repopulate remapped fields
		$(this).children(".condition_field").val(field);
		$(this).children(".condition_rule").val(rule);
		$(this).children(".condition_input_field").val(value);

	});


	clearEvents();
	bindEvents();
	formatConditions();
}



function formatConditions(){
	var conditions = "";
	$(".condition_container").each(function(){
		var field = $(this).children(".condition_field").val();
		var rule = $(this).children(".condition_rule").val();
		var value = $(this).children(".condition_input_field").val();
		conditions += field + ":" + rule + ":" + value + ";"
	});

	
	currentConditions = conditions;
}


function replaceConditionInput(e){
	var conditionContainer = $(e.target).closest('.condition_container');
	var selectedField = $(e.target).val();
	var conditionID = $(e.target).attr("id").split('_')[1];
	
	var conditionInputField  = conditionContainer.children(".condition_input_field");

	var replacementField = ""
	
	switch(selectedField){
		case "Tags":
			replacementField = $("#condition_tag_selection").html();
			replacementField = replacementField.replace("tag_x", "tag_"+conditionID)
			break;
		case "Title":
			replacementField = $("#condition_text_input").html();
			replacementField = replacementField.replace("input_x", "tag_"+conditionID)
			break;
		default:
			console.log("No, not recognized.");
	}		

	conditionInputField.replaceWith(replacementField);
	
	clearEvents();
	bindEvents();

}


function addCondition(conditionID, conditionTemplate, condition=defaultCondition){
	
	form_collection_conditions.append(conditionTemplate);	// add the new condition template to the conditions panel

	var selectedField = "";
	var selectedRule = "";
	var selectedValue = condition[2];

	var dropDown = "";

	var field = condition[0];
	var rule = condition[1];
	var value = condition[2];

	switch(field){
		case "Tags":
			selectedField = "Tags";
			$("#tag_"+conditionID).val(selectedValue);
			break;
		case "Title":
			selectedField = "Title";
			$("#input_"+conditionID).val(selectedValue);
			break;
		case "Type":
			selectedField = "Type";
			$("#type_"+conditionID).val(selectedValue);
			break;
		default:
			selectedField = "Title";
			$("#input_"+conditionID).val(selectedValue);
	}


	switch(value){
		case "isequalto":
			selectedRule = "=";
			break;
		case "isnotequalto":
			selectedRule = "!=";
			break;
		case "contains":
			selectedRule = "c";
			break;
		case "islessthan":
			selectedRule = "<";
			break;
		case "isgreaterthan":
			selectedRule = ">";
			break;
		default:
			selectedRule = "=";
	}



	$("#field_"+conditionID).val(selectedField);
	$("#rule_"+conditionID).val(selectedRule);
}


function updateCollectionData(){
	collectionData["collection_id"] = collectionID;
	collectionData["Conditions"] = currentConditions;
	collectionData["Published"] = 1;
	collectionData["Title"] = $("#input_collection_title").val();
	collectionData["BodyHTML"] = $("#collection_description").val();
	console.log(collectionData);

}




function loadImages(){
	collectionImageURL = $("#collection_img_src").val();
	main_image_container = $(".collection_image_main");
	main_image_container.css("background-image","url('" + collectionImageURL + "')");


}