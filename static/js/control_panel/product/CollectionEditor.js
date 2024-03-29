var collection_id;
var collectionData = {};
var collectionConditions = {};

var btn_saveCollection;
var btn_deleteCollection;
var btn_confirmCollectionChanges;
var btn_confirmDeleteCollection;
var btn_addCondition;

var select_newConditionType;
var panel_collection_conditions;

var table_collectionProducts;
var table_collectionProducts_body;
var message_noProductsInCollection;


var conditionFields = {
	"Price": [">", "<", ">=", "<=", "="],
	"Title": ["c"],
	"Tag": ["="],
	"Type": ["="]

};


var allProductTags = [];
var allProductTypes = [];

var conditionTemplates = {
	"condition-input-group": "<div class=\"input-group condition-input-group\"></div>",
	"select-condition-rule": "<select class=\"form-control select-condition-rule\"></select>",
	"condition_type_label": "<span class=\"input-group-addon condition-type-label\" id=\"type-addon\">replace_me</span>",
	"condition_value_text": "<input type=\"text\" class=\"form-control condition-value-input condition-text-value\">",
	"condition_value_tag": "<select class=\"form-control condition-value-input condition-tag-value\"></select>",
	"condition_value_type": "<select class=\"form-control condition-value-input condition-tag-value\"></select>",
	"condition_value_float": "<input type=\"text\" class=\"form-control condition-value-input condition-float-value\">",
	"delete-condition-btn": "<span class=\"input-group-btn delete-condition-btn\"><button type=\"button\" class=\"btn btn-danger\"><span class=\"glyphicon glyphicon-trash\"> </span> </button></span>"
};




$(document).ready(function(){
	bindElements();

	setupDescriptionEditor();
	bindEvents();

	populateInitialConditions();
	updateCollectionData();
});



function bindElements(){
	btn_saveCollection = $("#btn_saveCollection");
	btn_deleteCollection = $("#btn_deleteCollection");
	btn_confirmCollectionChanges = $("#btn_confirmCollectionChanges");
	btn_confirmDeleteCollection = $("#btn_confirmDeleteCollection");
	
	btn_addCondition = $("#btn_addCondition");

	select_newConditionType = $("#select_newConditionType");
	panel_collection_conditions = $("#panel_collection_conditions");

	table_collectionProducts = $("#table_collectionProducts");
	table_collectionProducts_body = $("#table_collectionProducts_body");
	message_noProductsInCollection = $("#message_noProductsInCollection");

	//populate product tags list
	allProductTags = $("#product_tags").val().split(',');
	allProductTags.pop();

	allProductTypes = $("#product_types").val().split(',');
	allProductTypes.pop();

	collection_id = $("#collection_id").val();

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

			//console.log(collectionData);
		});
	});


	btn_addCondition.click(function(){
		addCollectionCondition();
	});

	btn_confirmCollectionChanges.click(saveCollectionChanges);

	btn_confirmDeleteCollection.click(deleteCollection);
}	


function populateInitialConditions(){
	
	$(".collection-condition-data").each(function(){
		var conditionID = $(this).attr('data-conditionID');

		var conditionObj = replaceAll($(this).val(),'u\'','\'');
		conditionObj = replaceAll(conditionObj,"\'","\"");
		conditionObj = JSON.parse(conditionObj);

		collectionConditions[conditionID] = conditionObj;
		collectionConditions[conditionID]["id"] = conditionID;

		addCollectionCondition(conditionObj);
	});

	mapConditions();
}



function updateCollectionData(){

	$(".collection-input-field").each(function(){
		var fieldID = $(this).attr('data-fieldID');
		
		if(fieldID == "Strict"){
			collectionData[fieldID] = $(this).prop("checked");
			
		}
		else if(fieldID == "Published"){
			collectionData[fieldID] = $(this).prop("checked");
		}
		else{
			collectionData[fieldID] = $(this).val();
		}

	});

	collectionData["Conditions"] = collectionConditions;
	collectionData["collection_id"] = collection_id;

	//console.log(collectionData);
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
	

	$('#collection_description_editor').on('summernote.change', function(e) {
 		collectionData["BodyHTML"] = $('#collection_description_editor').summernote('code');
	});

	console.log(collectionData);
}





function addCollectionCondition(conditionObj){
	var nConditions = Object.keys(collectionConditions).length;
	

	if(nConditions == 0){
		panel_collection_conditions.html("");

	}
	
	if(typeof(conditionObj) != 'undefined'){
		var conditionType = conditionObj["type"];
		var conditionID = conditionObj["id"];
	}
	else{
		var conditionType = select_newConditionType.val();
		var conditionID = nConditions + 1;
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
		case "Type": 
				conditionTypeLabel = "Product Type ";
				conditionValueType = "condition_value_type";
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
	else if(conditionValueType == "condition_value_type"){
		for(var i=0; i<allProductTypes.length; i++){
			condition_value_input.append("<option value=\"" + allProductTypes[i] + "\">" + allProductTypes[i] + "</option>");
		}
	}


	collection_input_group.append(conditionTemplates["delete-condition-btn"]);
	var delete_condition_btn = $(".delete-condition-btn").last();

	
	if(typeof(conditionObj) != 'undefined'){
		select_condition_rule.val(conditionObj["rule"]);
		condition_value_input.val(conditionObj["value"]);
	}

	else{
		mapConditions();
	}
	
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

	updateCollectionData();

	if(nConditions == 0){
		$(".collection-input-field" + '[data-fieldID="Strict"]').unbind();

		$(".collection-input-field" + '[data-fieldID="Strict"]').change(function(){
			collectionData["Strict"] = $(this).prop("checked");
			//console.log(collectionData);
		});

		panel_collection_conditions.html("<h5> This collection does not have any conditions yet. </h5>");

	}
	else{

		$('.condition-float-value').keypress(function(event) {
		  if ((event.which != 46 || $(this).val().indexOf('.') != -1) && (event.which < 48 || event.which > 57)) {
		    event.preventDefault();
		  }
		});

		$(".collection-input-field" + '[data-fieldID="Strict"]').unbind();

		$(".collection-input-field" + '[data-fieldID="Strict"]').change(function(){
			collectionData["Strict"] = $(this).prop("checked");
			applyCollectionConditions();
		});



	}
		applyCollectionConditions();
}


function updateCollectionCondition(event){

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

	// returns products that now fit into this collection
	applyCollectionConditions();
}


function deleteCollectionCondition(event){
	var conditionID = event.data.conditionID;

	var selectorString = '[data-conditionID="' + conditionID + '"]';
	var condition_input_group = $(".condition-input-group" + selectorString);

	condition_input_group.remove();

	mapConditions();
}


function populateProductTable(products){
	table_collectionProducts.show();
	message_noProductsInCollection.hide();

	table_collectionProducts_body.html("");

	for(product_id in products){
		var currentProduct = products[product_id];
		var currentProductTitle = currentProduct["Title"];
		var currentProductSKU = currentProduct["VariantSKU"];
		var currentProductRowHTML = "";
		
		currentProductRowHTML += "<tr id=\"row_product\" data-productID=\"\">";
		currentProductRowHTML += "<td class=\"thumbnail_product_40\"></td>";
		currentProductRowHTML += "<td>" + currentProductTitle + "</td>";
		currentProductRowHTML += "<td>" + currentProductSKU + "</td>";
		currentProductRowHTML += "</tr>";

		table_collectionProducts_body.append(currentProductRowHTML);
	}


}


