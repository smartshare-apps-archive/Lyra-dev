var btn_saveShippingSettings;
var btn_saveShippoAPIKeys;

var btn_saveDefaultShippingAddress;
var btn_updateShippingInfo;

// this container is passed to action db
var shippingSettings = {};

$(document).ready(function(){
	bindElements();
	bindEvents();

});


function bindElements(){
	btn_saveShippingSettings = $("#btn_saveShippingSettings");
	btn_saveShippoAPIKeys = $("#btn_saveShippoAPIKeys");
	btn_updateShippingInfo = $("#btn_updateShippingInfo");
	btn_saveDefaultShippingAddress = $("#btn_saveDefaultShippingAddress");
}


function bindEvents(){
	$(".editor_input_field").each(function(){
		var fieldID = $(this).attr('data-fieldID');

		if(fieldID == "shipping_status"){
			var fieldValue = $(this).prop('checked');
			
			if (fieldValue == true){
				fieldValue = "enabled";
			}
			else{
				fieldValue = "disabled";
			}
			shippingSettings[fieldID] = fieldValue
		}
		else{
			shippingSettings[fieldID] = $(this).val();
		}

		$(this).change({fieldID: fieldID}, updateShippingSettings);
		
	});

	btn_saveShippoAPIKeys.click(saveShippoAPIKeys);
	btn_saveDefaultShippingAddress.click(saveDefaultShippingAddress);

	btn_updateShippingInfo.click(updateDefaultShippingAddress);
	console.log(shippingSettings);
}




function updateShippingSettings(event){
	var fieldID = event.data.fieldID;

	if(fieldID == "shipping_status"){
			var fieldValue = $(this).prop('checked');
			
			if (fieldValue == true){
				fieldValue = "enabled";
			}
			else{
				fieldValue = "disabled";
			}
			shippingSettings[fieldID] = fieldValue
		}
	else{
		shippingSettings[fieldID] = $(this).val();
	}
	
	console.log(shippingSettings);
}


function updateDefaultShippingAddress(){
	$(".shipping-label").each(function(){
		var fieldID = $(this).attr('data-fieldID');
		$(this).html(shippingSettings[fieldID]);
		console.log(shippingSettings[fieldID]);
		console.log(fieldID);
	});

}