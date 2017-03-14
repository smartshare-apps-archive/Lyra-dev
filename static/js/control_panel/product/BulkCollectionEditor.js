var collectionData;
var selectedFields;
var collectionIDList = [];

// page specific button handles
var btn_saveCollections;
var btn_confirmCollectionChanges;


$(document).ready(function(){
	collectionData = {};
	selectedFields = [];

	$(".variant_row").each(function(){
		cId = $(this).attr('id');
		cId = cId.split('_')[1];

		collectionData[cId] = {};
		collectionIDList.push(cId);	
	})

	updateCollectionData();

	bindElements();
	bindTableEvents();

});



function bindElements(){
	btn_saveCollections = $("#btn_saveCollections");
	btn_confirmCollectionChanges = $("#btn_confirmCollectionChanges");
}


function bindTableEvents(){
	btn_confirmCollectionChanges.click({collectionIDList: collectionIDList, collectionData:collectionData}, bulkUpdateCollections);
	btn_saveCollections.click(updateCollectionData);

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



function updateCollectionData(event){
	$(".bulk_editor_input_field").each(function(){
		currentField = ($(this).attr('id'));
		c = currentField.split('_');		
		field = c[0];
		collection_id = c[1];
		collectionData[collection_id][field] = $(this).val();	
	});

	console.log(collectionData);


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

	updateBulkCollectionEditorFields(selectedFields);
}


function registerChangeEvent(id){
	$("#"+id).change({id:id}, updateDataContainer);
}