// this file manages functions specific to the inventory editor page, including all event handling that deals with variant editing

var variantData = {};
var variant_id;

// page specific button handles
var btn_saveProduct;
var btn_confirmProductChanges;


$(document).ready(function(){
	productData = {};

	bindElements();
	bindEvents();

	setupVariantTable();			// bind events to the product variants table
});



function bindElements(){
	btn_saveProduct = $("#btn_saveProduct")
	btn_confirmProductChanges = $("#btn_confirmProductChanges")
	btn_deleteVariant = $("#btn_deleteVariant");
}



function bindEvents(){
	variant_id = $('#currentVariantID').val();
	variantData["variant_id"] = variant_id;

	btn_confirmProductChanges.click({variant_data: variantData}, saveProductInventoryChanges);
	btn_saveProduct.click(updateVariantData);
	btn_deleteVariant.click({variant_id: variant_id}, deleteVariant);


	$(".editor_input_field").each(function(){
		var fieldID = $(this).attr('data-fieldID');

		$(this).change(function(){
			variantData[fieldID] = $(this).val();
		});
	});

	updateVariantData();

	$("#select_filename").change(function(){
		var filename = $(this).val().split('\\');
		var pathLength = filename.length;
		filename = filename[pathLength-1];

		$("#input_filename").val(filename);
		
	});
}




function updateVariantData(){
	$(".editor_input_field").each(function(){
		var fieldID = $(this).attr('data-fieldID');
		variantData[fieldID] = $(this).val();
	});
}


function goToProductInventoryEditor(event){
	window.location.replace("/control/products/inventory/"+event.data.variant_id);
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
	
