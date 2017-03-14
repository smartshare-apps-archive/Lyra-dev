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
		var fieldID = $(this).attr('id').split('_')[1];

		$(this).change({fieldID: fieldID}, updatePaymentSettings);
		paymentSettings[fieldID] = $(this).val();
	});

	btn_saveStripeAPIKey.click(saveStripeAPIKeys);
}


function updatePaymentSettings(event){
	var fieldID = event.data.fieldID;
	paymentSettings[fieldID] = $("#input_"+fieldID).val();

}