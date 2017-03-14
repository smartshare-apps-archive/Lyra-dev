// this file manages functions specific to the inventory editor page, including all event handling that deals with variant editing

var variantData = {};
var variant_id;

// page specific button handles
var btn_saveProduct;
var btn_confirmProductChanges;


$(document).ready(function(){
	productData = {};
	bindElements();
	bindTableEvents();			// bind events to the product variants table
	bindChangeEvents();
	setupVariantTable();			// bind events to the product variants table
	loadImageResources();
});


function bindElements(){
	btn_saveProduct = $("#btn_saveProduct")
	btn_confirmProductChanges = $("#btn_confirmProductChanges")
	btn_deleteVariant = $("#btn_deleteVariant");
}

function bindChangeEvents(){
	variant_id = $('#currentVariantID').val();

	btn_confirmProductChanges.click({variant_data: variantData}, saveProductInventoryChanges);
	btn_saveProduct.click(updateVariantData);
	btn_deleteVariant.click({variant_id: variant_id}, deleteVariant);

	$("#input_VariantPrice").on('change', updateDataContainer);
	$("#input_VariantCompareAtPrice").on('change', updateDataContainer);
	$("#input_VariantBarcode").on('change', updateDataContainer);
	$("#input_VariantSKU").on('change', updateDataContainer);
	$("#input_VariantStock").on('change', updateDataContainer);

	updateVariantData();
}


function bindTableEvents(){

}


function goToProductInventoryEditor(event){
	window.location.replace("/control/products/inventory/"+event.data.variant_id);
}


function updateDataContainer(){
	$('#currentVariantPrice').val($("#input_VariantPrice").val());
	$('#currentVariantCompareAtPrice').val($("#input_VariantCompareAtPrice").val());
	$("#currentVariantBarcode").val($("#input_VariantBarcode").val());
	$("#currentVariantSKU").val($("#input_VariantSKU").val());
	$("#currentVariantStock").val($("#input_VariantStock").val());
}



function updateVariantData(event = null){
	
	var VariantPrice = $('#currentVariantPrice').val();
	var VariantCompareAtPrice = $('#currentVariantCompareAtPrice').val();
	var VariantBarcode = $("#currentVariantBarcode").val();
	var VariantSKU = $("#currentVariantSKU").val();
	var VariantStock = $("#currentVariantStock").val();

	variantData["VariantPrice"] = VariantPrice;
	variantData["VariantCompareAtPrice"] = VariantCompareAtPrice;
	variantData["VariantSKU"] = VariantSKU;
	variantData["VariantBarcode"] = VariantBarcode;
	variantData["VariantInventoryQty"] = VariantStock;
	variantData["variant_id"] = variant_id;
}


function loadImageResources(){
	$(".image_resource").each(function(){
		var resource_id = $(this).attr('id').split('_')[1];
		var resource_uri = $("#resource_uri_"+resource_id).val();
		var bg_image = "url('" + resource_uri + "')";
		$(this).css('background-image',bg_image);
	});

}



function setupVariantTable(){
	if($("#variantIDList").length){
		var variantIDList = $("#variantIDList").val().split(',');
		variantIDList.pop();

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
		$(this).css("background-image",bg_image);
	});
}
	
