var productData;
var variantData;
var selectedFields;
var productIdList = [];
var variantIdList = [];

// page specific button handles
var btn_saveProduct;
var btn_closeEditor;
var btn_confirmProductChanges;


$(document).ready(function(){
	productData = {};
	variantData = {};
	selectedFields = [];

	$(".variant_row").each(function(){
		var currentRowID = $(this).attr('id');
		currentRowID = currentRowID.split('_');

		var currentRowClass = currentRowID[0];
		var currentID = currentRowID[1];

		if (currentRowClass == "variant"){
			variantData[currentID] = {};
			variantIdList.push(currentID);	
		}
		else if(currentRowClass == "product"){
			productData[currentID] = {};
			productIdList.push(currentID);	
		}

	})

	updateProductData();
	updateVariantData();


	bindElements();
	bindTableEvents();

});



function bindElements(){
	btn_saveProduct = $("#btn_saveProduct");
	btn_confirmProductChanges = $("#btn_confirmProductChanges");
	btn_closeEditor = $("#btn_closeEditor");
}


function bindTableEvents(){
	btn_confirmProductChanges.click({productIdList: productIdList, variantIdList: variantIdList, productData:productData, variantData: variantData}, bulkUpdateProducts);
	
	btn_saveProduct.click(updateProductData);
	btn_saveProduct.click(updateVariantData);
	
	btn_closeEditor.click(goto_products);

	$(".bulk_editor_input_field").each(function(){
		registerChangeEvent($(this).attr('id'));
	});

	$(".toggle_bulk_editor_field").each(function(){
		var fieldID = $(this).attr('data-fieldID');
		console.log(fieldID);
		$(this).click({id: fieldID}, updateSelectedFields);
	});

}

function goto_products(){
	window.location.href = '/control/products';
}


function updateDataContainer(event){
	id = event.data.id;
	newValue = $("#"+id).val();
	hiddenField = "#current_" + id;
	$(hiddenField).val(newValue);
}



function updateProductData(event){
	$(".bulk_editor_input_field").each(function(){
		var parentRow = $(this).closest("tr").attr('id');
		var rowClass = parentRow.split('_')[0];
		if(rowClass == "product"){
			currentField = ($(this).attr('id'));
			c = currentField.split('_');		
			field = c[0];
			product_id = c[1];
			productData[product_id][field] = $(this).val();
			//console.log(productData);
		}
	});
}

function updateVariantData(event){
	$(".bulk_editor_input_field").each(function(){
		var parentRow = $(this).closest("tr").attr('id');
		var rowClass = parentRow.split('_')[0];

		if(rowClass == "variant"){
			currentField = ($(this).attr('id'));
			c = currentField.split('_');		
			field = c[0];
			variant_id = c[1];
			variantData[variant_id][field] = $(this).val();
			//console.log(variantData);
		}
	});
}



function updateSelectedFields(event){
	
	selectedFields = $("#selectedFields").val();
	selectedFields = selectedFields.slice(0,-1).split(',');

	var fieldID = event.data.id;
	console.log("toggle:" + fieldID);
	var index = selectedFields.indexOf(fieldID);

	if(index != -1) {
		selectedFields.splice(index, 1);
	}
	else{
		selectedFields.push(fieldID)
	}

	selectedFields = selectedFields.join(',');

	updateBulkProductEditorFields(selectedFields);
}


function registerChangeEvent(id){
	$("#"+id).change({id:id}, updateDataContainer);
}