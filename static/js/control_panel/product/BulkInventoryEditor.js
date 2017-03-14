var productData;
var selectedFields;
var productIdList = [];

// page specific button handles
var btn_saveProduct;
var btn_confirmProductChanges;


$(document).ready(function(){
	productData = {};
	selectedFields = [];

	$(".variant_row").each(function(){
		cId = $(this).attr('id');
		cId = cId.split('_')[1];

		productData[cId] = {};
		productIdList.push(cId);	
	})

	updateProductData();

	bindElements();
	bindTableEvents();

});



function bindElements(){
	btn_saveProduct = $("#btn_saveProduct");
	btn_confirmProductChanges = $("#btn_confirmProductChanges");
}


function bindTableEvents(){
	btn_confirmProductChanges.click({productIdList: productIdList, productData:productData}, bulkUpdateProducts);
	btn_saveProduct.click(updateProductData);

	$(".bulk_editor_input_field").each(function(){
		registerChangeEvent($(this).attr('id'));
	});

	$(".toggle_bulk_editor_field").each(function(){
		$(this).click({id:$(this).attr('id')}, updateSelectedFields);
	});
}


function updateDataContainer(event){
	id = event.data.id;
	newValue = $("#"+id).val();
	hiddenField = "#current_" + id;
	$(hiddenField).val(newValue);
}



function updateProductData(event){
	$(".bulk_editor_input_field").each(function(){
		currentField = ($(this).attr('id'));
		c = currentField.split('_');		
		field = c[0];
		product_id = c[1];
		productData[product_id][field] = $(this).val();
		
	});

}


function updateSelectedFields(event){
	selectedFields = $("#selectedFields").val();
	selectedFields = selectedFields.slice(0,-1).split(',');

	field = event.data.id.split('_')[1];

	var index = selectedFields.indexOf(field);

	if(index != -1) {
		selectedFields.splice(index, 1);
	}
	else{
		selectedFields.push(field)
	}

	selectedFields = selectedFields.join(',');
	console.log(selectedFields);

	updateBulkInventoryEditorFields(selectedFields);
}


function registerChangeEvent(id){
	$("#"+id).change({id:id}, updateDataContainer);
}