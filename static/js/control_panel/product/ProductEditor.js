var productData;
var product_id;
var stripe_id;

// page specific button handles
var btn_saveProduct;
var btn_deleteProduct;
var btn_confirmProductChanges;
var btn_addProductVariant;

// variant creation handles
var variant_creation_step = "step1";
var newVariantType = {};
var newVariantData = {};
var variantTypes = {};

// vendor management objects
var vendorData = {};

var newVariantType_input;
var newVariantValue_input;

var btn_saveVariantTypes;
var btn_addVariantValue;
var btn_deleteVariantValue;

// tag stuff
var btn_updateProductTags;
var btn_updateProductTypes;
var btn_createProductType;

//variant stuff
var btn_addVariantType;
var btn_confirmNewVariant;
var btn_variantSummary;
var select_newVariantValues;
var newVariantType_label;

$(document).ready(function(){
	productData = {};
	bindElements();
	setupDescriptionEditor();	// bind events to summernote wysiwyg editor and fill it with initial description html
	bindEvents();
	setupVariantTable();			// bind events to the product variants table
	loadImageResources();
});


function bindElements(){
	btn_saveProduct = $("#btn_saveProduct")
	btn_confirmProductChanges = $("#btn_confirmProductChanges")
	btn_deleteProduct = $("#btn_deleteProduct");
	btn_addProductVariant = $("#btn_addProductVariant");

	newVariantType_input = $("#newVariantType_input");
	newVariantValue_input = $("#newVariantValue_input");

	btn_saveVariantTypes = $("#btn_saveVariantTypes");
	btn_addVariantType = $("#btn_addVariantType");
	btn_addVariantValue = $("#btn_addVariantValue");
	btn_deleteVariantValue = $("#btn_deleteVariantValue");
	btn_confirmNewVariant = $("#btn_confirmNewVariant");
	btn_variantSummary = $("#btn_variantSummary");
	select_newVariantValues = $("#select_newVariantValues");
	newVariantType_label = $("#newVariantType_label");

	//gets the current variant type data from a container
	retrieveVariantTypes();

	btn_updateProductTags = $("#btn_updateProductTags");
	btn_updateProductTypes = $("#btn_updateProductTypes");
	btn_createProductType = $("#btn_createProductType");

	$(".btn-tag").each(function(){
		$(this).click(updateProductTags);
	});

	product_id = $('#currentProductId').val();
	stripe_id = $('#currentStripeID').val();

	productData["product_id"] = product_id;
	productData["stripe_id"] = stripe_id;

	$('[data-toggle="tooltip"]').tooltip(); 
}


function bindEvents(){
	btn_confirmProductChanges.click({product_data: productData}, saveProductChanges);
	btn_deleteProduct.click({product_id:product_id}, deleteProduct);


	$('#input_BodyHTML').on('summernote.change', function(e) {
 		productData["BodyHTML"] = $('#input_BodyHTML').summernote('code');
		});


	$(".editor_input_field").each(function(){
		var fieldID = $(this).attr('id').split('_')[1];
		$(this).change({fieldID: fieldID}, updateProductData);
	});

	btn_addVariantType.click(createVariantType);
	btn_addVariantValue.click(addVariantValue);
	btn_deleteVariantValue.click(deleteVariantValue);
	btn_variantSummary.click(reviewNewVariants);

	$(".btn_deleteVariantType").each(function(){
		var variantType = $(this).attr('id').split('_')[1];
		$(this).click({variantType: variantType}, deleteVariantType);

	});

	$(".btn_editVariantType").each(function(){
		var variantType = $(this).attr('id').split('_')[2];
		$(this).click({variantType: variantType}, editVariantType);

	});


	if(btn_addProductVariant.length) {
		$(".new_variant_select").each(function(){
			$(this).change(updateNewVariantData);
			// fill the container with default data
			newVariantData[$(this).attr('id').split('_')[2]] = $(this).val();
		});

		btn_addProductVariant.click(addProductVariant);
		
	}

	$("#select_filename").change(function(){
		var filename = $(this).val().split('\\');
		var pathLength = filename.length;
		filename = filename[pathLength-1];

		$("#input_filename").val(filename);
		
	});

	btn_updateProductTags.click({product_id: product_id}, saveProductTags);

	btn_createProductType.click(addProductType);
	btn_updateProductTypes.click(saveProductTypes);

	$(".btn-type").each(function(){
		var typeID = $(this).attr('data-ptype');
		$(this).click({typeID: typeID}, deleteProductType);

	});



	// vendor management details
	populateVendorData();

	$("#select_productVendor").change(function(){
		var currentVendor = $(this).val();
		loadVendorDetails(currentVendor);
	});

	$("#btn_updateProductVendors").click(saveProductVendors);

}

function populateVendorData(){

	$(".vendor-data").each(function(){
		var vendorID = $(this).attr('data-vendorID');
		var field = $(this).attr('data-vendorField');

		if (vendorID in vendorData){
			vendorData[vendorID][field] = $(this).val();
		} 
		else{
			vendorData[vendorID] = {};
			vendorData[vendorID][field] = $(this).val();
		}
	});

	for(vendorID in vendorData){
		loadVendorDetails(vendorID);
		break;
	}

}

function loadVendorDetails(currentVendor){
	$(".vendor-edit").each(function(){
		var currentField = $(this).attr('data-vendorField');
		var currentValue = vendorData[currentVendor][currentField];
		$(this).val(currentValue);
		$(this).unbind();
		$(this).change({vendorID:currentVendor}, updateVendorData);
	});

}

function updateVendorData(event){
	var vendorID = event.data.vendorID;
	var targetFieldContainer = $(event.currentTarget);
	var vendorField = targetFieldContainer.attr('data-vendorField');

	var newValue = targetFieldContainer.val();

	vendorData[vendorID][vendorField] = newValue;

	//console.log("updating: " + vendorID);

}


// update the container that stores new variant data 
function updateNewVariantData(event){
	var variantOptionID = $(event.target).attr('id').split('_')[2];
	newVariantData[variantOptionID] = $(this).val();
}



function addProductVariant(event){
	saveNewProductVariant(newVariantData, product_id);
}


function updateProductTags(event){
	var selectedHTML = "&nbsp;&nbsp;<span class=\"glyphicon glyphicon-ok\"></span>";

	var currentTags = $("#currentProductTags").val().split(',');
	var tagObject = $(event.currentTarget);

	var tagID = tagObject.attr('id').split('_')[1];

	var tagIndex = currentTags.indexOf(tagID);

	if(tagIndex >= 0){
		var newHTML = tagObject.html().replace(selectedHTML,"");
		tagObject.html(newHTML);

		tagObject.toggleClass("btn-primary", true);
		tagObject.toggleClass("btn-default", false);

		currentTags.splice(tagIndex, 1);
	}
	else{
		var newHTML = tagObject.html() + selectedHTML;
		tagObject.html(newHTML);
		tagObject.toggleClass("btn-primary", false);
		tagObject.toggleClass("btn-default", true);
		currentTags.push(tagID);
	}

	currentTags = currentTags.filter(removeEmpty);
	var newTags = currentTags.join(',');
	

	$("#currentProductTags").val(newTags);
	$("#current_tag_label").html(replaceAll(newTags,",",", "));
	//console.log(newTags);
}



//updates product type list before insertion into settings table
function addProductType(event){

	var currentTypes = $("#currentProductTypes").val().split(',');
	var newProductType = $("#newProductType_input").val();

	var typeIndex = currentTypes.indexOf(newProductType);

	if(typeIndex < 0 && newProductType != ""){
		currentTypes.push(newProductType);
		var newTagHTML = "<button type=\"button\" class=\"btn btn-default btn-type\" data-ptype=\"" + newProductType + "\">" + newProductType +"&nbsp;&nbsp;<span class=\"glyphicon glyphicon-minus-sign\"></span></button>";
		$("#product_type_buttons").append(newTagHTML);
		$("#newProductType_input").val("");
	}

	currentTypes = currentTypes.filter(removeEmpty);
	var newTypes = currentTypes.join(',');
	

	$("#currentProductTypes").val(newTypes);

	$(".btn-type").each(function(){
		var typeID = $(this).attr('data-ptype');
		$(this).unbind();
		$(this).click({typeID: typeID}, deleteProductType);

	});
}



// deletes a single product type
function deleteProductType(event){
	var typeID = event.data.typeID;
	var selectorString = '[data-ptype="' + typeID + '"]';
	var currentTypes = $("#currentProductTypes").val().split(',');
	var typeIndex = currentTypes.indexOf(typeID);

	if(typeIndex >= 0){
		currentTypes.splice(typeIndex, 1);
		var currentElement = $(".btn-type" + selectorString);
		currentElement.remove(); 
		
		currentTypes = currentTypes.filter(removeEmpty);
		var newTypes = currentTypes.join(',');
		$("#currentProductTypes").val(newTypes);

	}


}




// removes all elements of a string when used with filter
function removeEmpty(value){
	return value != "";
}


function deleteVariantType(event){
	var variantType = event.data.variantType;
	$("#variantType_"+variantType).remove();

	delete variantTypes[variantType];
	
	btn_saveVariantTypes.unbind("click");
	btn_saveVariantTypes.click({product_id: product_id, stripe_id: stripe_id, variantTypes:variantTypes}, saveVariantTypes);
}


function retrieveVariantTypes(){
	var currentVariantTypes = replaceAll($("#currentVariantTypes").val(), "'","\"");
	currentVariantTypes = replaceAll(currentVariantTypes, "u\"","\"");
	console.log(currentVariantTypes);

	currentVariantTypes = JSON.parse(currentVariantTypes);
	
	for (var variantType in currentVariantTypes){
		variantTypes[variantType] = currentVariantTypes[variantType];
	}
}

function createVariantType(){

	if(newVariantType_input.val() != ""){
		$("#variant_add_step1").slideToggle();
		$("#variant_add_step2").slideToggle();
		variant_creation_step = "step2"
		newVariantType[newVariantType_input.val()] = []
	}
}


function editVariantType(event){
	cleanupVariantTypeEditor();

	var targetVariantType = event.data.variantType;

	newVariantType_input.val(targetVariantType);
	newVariantType[targetVariantType] = variantTypes[targetVariantType];

	$("#variant_add_step1").slideToggle();
	$("#variant_add_step2").slideToggle();
	
	variant_creation_step = "step2"

	for (var i=0; i<newVariantType[targetVariantType].length; i++){
		 		 select_newVariantValues.append($("<option></option>").attr("value", newVariantType[targetVariantType][i]).text(newVariantType[targetVariantType][i])); 
				 select_newVariantValues.val(newVariantType[targetVariantType][i]);
		 	}

}

function cleanupVariantTypeEditor(event){
	select_newVariantValues.empty();
}


function addVariantValue(){
	var newVariantValue = newVariantValue_input.val();
	
	if (newVariantValue != ""){
		 var commaSeparatedValues = newVariantValue.split(',');

		 if (commaSeparatedValues.length > 1){

		 	for (var i=0;i<commaSeparatedValues.length;i++){
		 		 commaSeparatedValues[i] = commaSeparatedValues[i].trim();
		 		 select_newVariantValues.append($("<option></option>").attr("value", commaSeparatedValues[i]).text(commaSeparatedValues[i])); 
				 select_newVariantValues.val(commaSeparatedValues[i]);
				 newVariantType[newVariantType_input.val()].push(commaSeparatedValues[i]);
		 	}

		 }
		 else{
			 select_newVariantValues.append($("<option></option>").attr("value", newVariantValue).text(newVariantValue)); 
			 select_newVariantValues.val(newVariantValue);
			 newVariantValue = newVariantValue.trim();
			 newVariantType[newVariantType_input.val()].push(newVariantValue);
		}

		newVariantValue_input.val("");
	}

}

function deleteVariantValue(){
	var currentValue = select_newVariantValues.val();

	if (currentValue != "") {
		var index = newVariantType[newVariantType_input.val()].indexOf(currentValue);
		
		if (index >= 0){
			newVariantType[newVariantType_input.val()].splice(index, 1);
			$("#select_newVariantValues option[value='" + currentValue + "']").remove();

		}
		
	}

}

function reviewNewVariants(){
	if(newVariantType_input.val() != ""){

		$("#variant_add_step2").slideToggle();
		$("#variant_add_step3").slideToggle();
		variant_creation_step = "step3"

		newVariantType_label.html("<b> Variant option: </b>" + newVariantType_input.val());

		for(var i=0; i<newVariantType[newVariantType_input.val()].length; i++){
			$("#new_variant_types").append("<button type=\"button\" class=\"btn btn-primary btn-small btn_newVariantType\" id=\"" + "variant_" + newVariantType[newVariantType_input.val()][i] + "\">" + newVariantType[newVariantType_input.val()][i] + " </button>");
		}

		variantTypes[newVariantType_input.val()] = newVariantType[newVariantType_input.val()];

		btn_confirmNewVariant.click({product_id: product_id, stripe_id: stripe_id, variantTypes:variantTypes}, saveVariantTypes);

	}
}

function loadImageResources(){
	$(".image_resource").each(function(){
		var resource_id = $(this).attr('id').split('_')[1];
		var resource_uri = $("#resource_uri_"+resource_id).val();
		var bg_image = "url('" + resource_uri + "')";
		$(this).css('background-image',bg_image);

		$(this).mouseenter({resource_id: resource_id}, showImageButtons);
		$(this).mouseleave({resource_id: resource_id}, hideImageButtons);

		$(this).find('.image-btn.delete').click({resource_id:resource_id}, deleteProductImage);
		$(this).find('.image-btn.default').click({resource_id:resource_id}, setDefaultImage);
	});

	// this just makes sure the default image is pushed the left, kinda crude
	var mainImage = $("#product_images").find(".main-image");
	var firstSubImage = $("#product_images").children(".sub-image")[0];

	mainImage.insertBefore(firstSubImage);		
}

function showImageButtons(event){
	var resource_id = event.data.resource_id;
	var currentImage = $("#img_"+resource_id);

	currentImage.find(".image-btn").each(function(){
		$(this).show();
	});

}


function hideImageButtons(event){
	var resource_id = event.data.resource_id;
	var currentImage = $("#img_"+resource_id);

	currentImage.find(".image-btn").each(function(){
		$(this).hide();
	});
}

function deleteProductImage(event){
	var resource_id = event.data.resource_id;
	deleteProductResource(product_id, resource_id, "product_image");
}


function setDefaultImage(event){
	var resource_id = event.data.resource_id;
	setDefaultProductImage(product_id, resource_id);
}


// setups the product description editor with summernote and populates it with current product description
function setupDescriptionEditor(){
	$('#input_BodyHTML').summernote({
		  height: 250,                 // set editor height
		  minHeight: 200,             // set minimum height of editor
		  maxHeight: 500,             // set maximum height of editor
		  focus: false                  // set focus to editable area after initializing summernote
		});

	var BodyHTML = $("#currentBodyHTML").val();
	$('#input_BodyHTML').summernote('code', BodyHTML);

}




function setupVariantTable(){
	if($("#variantIDList").length){
		var variantIDList = $("#variantIDList").val().split(',');
		variantIDList.pop();
		console.log(variantIDList);
		for(var i=0;i<variantIDList.length;i++){
			variantID = variantIDList[i];
			currentRowId = "#row_variant_" + variantID;

			currentRow = $(currentRowId);
			currentRow.click({variant_id: variantID}, goToProductInventoryEditor);
		}
	}

	$(".thumbnail_product_40").each(function(){
		var thumbnail_src = $(this).find("input").val();
		var bg_image = "url('" + thumbnail_src + "')"
		console.log(bg_image);
		$(this).css("background-image",bg_image);
	});
}
	




function updateProductData(event){
	var fieldID = event.data.fieldID;

	if(fieldID == "Published"){
		var published = $("#input_"+fieldID).prop("checked");
		if (published == true){
			published = "true";
		}
		else{
			published = "false";
		}
		productData[fieldID] = published;

		return;
	}

	productData[fieldID] = $("#input_"+fieldID).val();

	console.log(productData);

}




function goToProductInventoryEditor(event){
	window.location.replace("/control/products/inventory/"+event.data.variant_id);
}
