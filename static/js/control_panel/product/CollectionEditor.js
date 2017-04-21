
var collectionData = {};
var collectionConditions = {};

var btn_saveCollection;
var btn_deleteCollection;
var btn_confirmCollectionChanges;
var btn_addCondition;

var select_newConditionType;
var panel_collection_conditions;

var conditionFields = {
	"Price": [">", "<", ">=", "<=", "="],
	"Title": ["c"],
	"Tag": ["c", "="]

};

var allProductTags = [];


var conditionTemplates = {
	"condition-input-group": "<div class=\"input-group condition-input-group\"></div>",
	"select-condition-rule": "<select class=\"form-control select-condition-rule\"></select>",
	"condition_type_label": "<span class=\"input-group-addon condition-type-label\" id=\"type-addon\">replace_me</span>",
	"condition_value_text": "<input type=\"text\" class=\"form-control condition-value-input condition-text-value\">",
	"condition_value_tag": "<select class=\"form-control condition-value-input condition-tag-value\"></select>",
	"condition_value_float": "<input type=\"text\" class=\"form-control condition-value-input condition-float-value\">",
	"delete-condition-btn": "<span class=\"input-group-btn delete-condition-btn\"><button type=\"button\" class=\"btn btn-danger\"><span class=\"glyphicon glyphicon-trash\"> </span> </button></span>"
};




$(document).ready(function(){

	bindElements();

	setupDescriptionEditor();
	bindEvents();

	updateCollectionData();
});



function bindElements(){
	btn_saveCollection = $("#btn_saveCollection");
	btn_deleteCollection = $("#btn_deleteCollection");
	btn_confirmCollectionChanges = $("#btn_confirmCollectionChanges");
	btn_addCondition = $("#btn_addCondition");

	select_newConditionType = $("#select_newConditionType");
	panel_collection_conditions = $("#panel_collection_conditions");

	//populate product tags list
	allProductTags = $("#product_tags").val().split(',');
	allProductTags.pop();


}



function bindEvents(){

	$(".collection-input-field").each(function(){
		var fieldID = $(this).attr('data-fieldID');

		$(this).change(function(){
		
			if(fieldID == "Strict" || fieldID == "Published"){
				collectionData[fieldID] = $(this).prop("checked");
			}
			else{
				collectionData[fieldID] = $(this).val();
			}

			console.log(collectionData);
		});
	});


	btn_addCondition.click(addCollectionCondition);


}	



function updateCollectionData(){

	$(".collection-input-field").each(function(){
		var fieldID = $(this).attr('data-fieldID');
		
		if(fieldID == "Strict" || fieldID == "Published"){
			collectionData[fieldID] = $(this).prop("checked");
		}
		else{
			collectionData[fieldID] = $(this).val();
		}

	});

	collectionData["Conditions"] = collectionConditions;

	console.log(collectionData);
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

}





function addCollectionCondition(){
	var conditionType = select_newConditionType.val();

	var nConditions = Object.keys(collectionConditions).length;
	var conditionID = nConditions + 1;

	if(nConditions == 0){
		panel_collection_conditions.html("");

	}

	// append a container for the condition controls, e.g. condition rules
	panel_collection_conditions.append(conditionTemplates["condition-input-group"]);
	var collection_input_group = $(".condition-input-group").last();

	var conditionTypeLabel = "";
	var conditionValueType = "";

		
	switch(conditionType){
		case "Price": 
				conditionTypeLabel = "Price "; 
				conditionValueType = "condition_value_float";
			break;
		case "Tag": 
				conditionTypeLabel = "Tag";
				conditionValueType = "condition_value_tag";
			break;
		case "Title": 
				conditionTypeLabel = "Product Title ";
				conditionValueType = "condition_value_text";
			break;
		default:
			conditionTypeLabel = "Invalid condition type.";
	}


	collection_input_group.append(conditionTemplates["condition_type_label"].replace("replace_me", conditionTypeLabel));

	var condition_type_label = $(".condition-type-label").last();
	condition_type_label.attr('data-conditionType', conditionType);

	collection_input_group.append(conditionTemplates["select-condition-rule"]);

	// append the dropdown to select the condition rule (e.g. gt, eq, lt, contains)
	var select_condition_rule = $(".select-condition-rule").last();

	// add the possible rules to the select box
	for(var i=0; i<conditionFields[conditionType].length; i++){
		var ruleLabel = "";
		
		switch(conditionFields[conditionType][i]){

			case 'c': ruleLabel = "contains"; 
				break;
			case '=': ruleLabel = "is equal to"; 
				break;
			case '>=': ruleLabel = "is greater than or equal to"; 
				break;
			case '<=': ruleLabel = "is less than or equal to"; 
				break;
			case '>': ruleLabel = "is greater than"; 
				break;
			case '<': ruleLabel = "is less than"; 
				break;

			default:
				ruleLabel = "Invalid rule";
		}

		select_condition_rule.append("<option value=\"" + conditionFields[conditionType][i] +"\">" + ruleLabel + "</option>");

	}

	collection_input_group.append(conditionTemplates[conditionValueType]);
	var condition_value_input = $(".condition-value-input").last();

	if(conditionValueType == "condition_value_tag"){

		for(var i=0; i<allProductTags.length; i++){
			condition_value_input.append("<option value=\"" + allProductTags[i] + "\">" + allProductTags[i] + "</option>");
		}
	}

	collection_input_group.append(conditionTemplates["delete-condition-btn"]);
	var delete_condition_btn = $(".delete-condition-btn").last();

	

	mapConditions();
}

function mapConditions(){
	collectionConditions = {};

	$(".condition-input-group").each(function(index){

		var conditionID =  String(index);

		$(this).attr('data-conditionID', conditionID);

		var conditionRuleInput = $(this).find('.select-condition-rule');
		var conditionValueInput = $(this).find(".condition-value-input");
		var deleteConditionBtn = $(this).find(".delete-condition-btn");
		var conditionTypeLabel = $(this).find('.condition-type-label');

		conditionRuleInput.attr('data-conditionID', conditionID);
		conditionValueInput.attr('data-conditionID', conditionID);
		deleteConditionBtn.attr('data-conditionID', conditionID);
		conditionTypeLabel.attr('data-conditionID', conditionID);

		collectionConditions[conditionID] = {};
		collectionConditions[conditionID]["type"] = conditionTypeLabel.attr('data-conditionType');
		collectionConditions[conditionID]["rule"] = conditionRuleInput.val();
		collectionConditions[conditionID]["value"] = conditionValueInput.val();

		conditionRuleInput.unbind();
		conditionValueInput.unbind();
		deleteConditionBtn.unbind();

		conditionRuleInput.change({conditionID: conditionID}, updateCollectionCondition);
		conditionValueInput.change({conditionID: conditionID}, updateCollectionCondition);
		deleteConditionBtn.click({conditionID: conditionID}, deleteCollectionCondition);

	});

	var nConditions = Object.keys(collectionConditions).length;

	if(nConditions == 0){
		panel_collection_conditions.html("<h5> This collection does not have any conditions yet. </h5>");
	}

	updateCollectionData();
}


function updateCollectionCondition(event){
	console.log("Updating: " + conditionID);

	var conditionID = event.data.conditionID;
	var selectorString = '[data-conditionID="' + conditionID + '"]';

	var conditionTypeLabel = $(".condition-type-label" + selectorString);
	var conditionRuleInput = $(".select-condition-rule" + selectorString);
	var conditionValueInput = $(".condition-value-input" + selectorString);
	var deleteConditionBtn = $(".delete-condition-btn" + selectorString);


	collectionConditions[conditionID] = {};
	collectionConditions[conditionID]["type"] = conditionTypeLabel.attr('data-conditionType');
	collectionConditions[conditionID]["rule"] = conditionRuleInput.val();
	collectionConditions[conditionID]["value"] = conditionValueInput.val();

	updateCollectionData();
}


function deleteCollectionCondition(event){
	var conditionID = event.data.conditionID;

	var selectorString = '[data-conditionID="' + conditionID + '"]';
	var condition_input_group = $(".condition-input-group" + selectorString);

	condition_input_group.remove();

	mapConditions();
}