var btn_savePaymentSettings;
var btn_saveStripeAPIKey;

// this container is passed to action db
var paymentSettings = {};

$(document).ready(function(){
	bindElements();
	bindEvents();

});


function bindElements(){
	btn_savePaymentSettings = $("#btn_savePaymentSettings");
	btn_saveStripeAPIKey = $("#btn_saveStripeAPIKey");
}


function bindEvents(){
	//btn_savePaymentSettings.click(saveSettings);
	$(".editor_input_field").each(function(){
		var fieldID = $(this).attr('data-fieldID');

		if(fieldID == "payment_status"){
			var fieldValue = $(this).prop('checked');
			
			if (fieldValue == true){
				fieldValue = "enabled";
			}
			else{
				fieldValue = "disabled";
			}
			paymentSettings[fieldID] = fieldValue
		}
		else{
			paymentSettings[fieldID] = $(this).val();
		}

		$(this).change({fieldID: fieldID}, updatePaymentSettings);
		
	});

	btn_saveStripeAPIKey.click(saveStripeAPIKeys);
}


function updatePaymentSettings(event){
	var fieldID = event.data.fieldID;

	if(fieldID == "payment_status"){
			var fieldValue = $(this).prop('checked');
			
			if (fieldValue == true){
				fieldValue = "enabled";
			}
			else{
				fieldValue = "disabled";
			}
			paymentSettings[fieldID] = fieldValue
		}
	else{
		paymentSettings[fieldID] = $(this).val();
	}
	
}