// this handles the checkout form validation

var fieldValidity = {
	"Email":false,
	"cc":false,
	"cvc":false,
	"exp":false,
	"ShippingAddress1":false,
	"ShippingPostalCode":false,
	"ShippingFirstName":false,
	"ShippingLastName":false,
	"ShippingCity":false,
	"ShippingState":false,
	"ShippingCountry":false,
	"BillingAddress1":false,
	"BillingPostalCode":false,
	"BillingFirstName":false,
	"BillingLastName":false,
	"BillingCity":false,
	"BillingState":false,
	"BillingCountry":false,
};

var shippingIsBilling = true;

var validatedFields = [
	"cc", "cvc", "exp", "Email", "ShippingAddress1", "ShippingPostalCode", "ShippingFirstName",
	"ShippingLastName",  "ShippingCity", "ShippingState", "ShippingCountry","BillingAddress1", "BillingPostalCode", "BillingFirstName",
	"BillingLastName",  "BillingCity", "BillingState", "BillingCountry"
];


//checkout state manager
var checkoutSteps = ["shipping","payment","confirm"];
var checkoutNextMessages = ["Continue to payment", "Verify payment method"];
var checkoutPreviousMessages = ["", "Return to shipping", ""];
var currentCheckoutStep = "shipping";

var cardType = "";

// element handles
var cc_input;
var cvc_input;
var exp_input;
var postal_input;

// other container handles
var shipping_info_container;
var payment_info_container;
var next_message;
var previous_message;


// button handles
var btn_checkoutNext;
var btn_checkoutPrevious;
var btn_confirmOrder;

$(document).ready(function(){
	bindElements();
	bindEvents();
	restrictForm();
	loadProductThumbnails();
});


function bindElements(){
	cc_input = $("#customer_cc");
	cvc_input = $("#customer_cvc");
	exp_input = $("#customer_exp");
	postal_input = $("#customer_ShippingPostalCode");

	btn_checkoutNext = $("#btn_checkoutNext");
	btn_checkoutPrevious = $("#btn_checkoutPrevious");
	btn_confirmOrder = $("#btn_confirmOrder");
	btn_chkShippingAddress = $("#chk_ship_to_address");

	shipping_info_container = $("#shipping_info_container");
	billing_info_container = $("#billing_info_container");
	payment_info_container = $("#payment_info_container");
	next_message = $("#next_message");
	previous_message = $("#previous_message");

}	



function bindEvents(){
	$(".customer_info_input").each(function(){
		$(this).on('change keyup paste',validateFieldEvent);
		
		var currentField = $(this).attr('data-fieldID');
		// this is for validating data that appears on load (from logged in customers)
		if(currentField){
			validateField(currentField);
		}
		


		
	});

	btn_chkShippingAddress.click(toggleShippingAddress);
}



// jquery payment form restriction as a preliminary validator
function restrictForm(){
	cc_input.payment('formatCardNumber');
	cvc_input.payment('formatCardCVC');
	exp_input.payment('formatCardExpiry');
	postal_input.payment('restrictNumeric');

}

// proceed to next step in checkout
function checkoutNext(){
	var checkoutStepIndex = checkoutSteps.indexOf(currentCheckoutStep);

	if (currentCheckoutStep == "shipping"){
		billing_info_container.slideToggle();

		if (shippingIsBilling == false) {
			shipping_info_container.slideToggle();
		}

		payment_info_container.slideToggle();
	}

	currentCheckoutStep = checkoutSteps[checkoutStepIndex + 1];
	next_message.html(checkoutNextMessages[checkoutStepIndex + 1]);
	previous_message.html(checkoutPreviousMessages[checkoutStepIndex + 1]);

	var step_valid = validateCheckoutStep(currentCheckoutStep);
}



function checkoutPrevious(){
	var checkoutStepIndex = checkoutSteps.indexOf(currentCheckoutStep);

	if (currentCheckoutStep == "payment"){
		billing_info_container.slideToggle();

		if(shippingIsBilling == false){
			shipping_info_container.slideToggle();
		}

		payment_info_container.slideToggle();
	}

	currentCheckoutStep = checkoutSteps[checkoutStepIndex - 1];
	next_message.html(checkoutNextMessages[checkoutStepIndex - 1]);
	previous_message.html(checkoutPreviousMessages[checkoutStepIndex - 1]);
	
	var step_valid = validateCheckoutStep(currentCheckoutStep);
}



function validateCheckoutStep(currentCheckoutStep){
	// reset button states
	btn_checkoutNext.unbind("click");
	btn_checkoutPrevious.unbind("click");

	btn_checkoutNext.toggleClass("disabled", true);
	btn_checkoutPrevious.toggleClass("disabled", true);

	// check if current step is validated
	if (currentCheckoutStep == "shipping") {

		var validatedFields = ["Email","BillingAddress1", "BillingPostalCode", "BillingFirstName",
								"BillingLastName",  "BillingCity", "BillingState", "BillingCountry"]

		// if there is a separate shipping address, add those fields as validation requirements
		if(shippingIsBilling == false){
			validatedFields.push("ShippingFirstName", "ShippingLastName", "ShippingAddress1","ShippingPostalCode","ShippingCity", "ShippingState", "ShippingCountry");
		}
		
		// check if any validated field returns invalid, if so, get outta there
		for (var i = 0; i < validatedFields.length; i++){
			if (fieldValidity[validatedFields[i]] == false){
				return false;
			}
		}
		//if step is valid, attach event handlers and toggle class
		btn_checkoutNext.click(checkoutNext);
		btn_checkoutNext.toggleClass("disabled", false);

	}

	else if(currentCheckoutStep == "payment"){
		btn_checkoutPrevious.click(checkoutPrevious);
		btn_checkoutPrevious.toggleClass("disabled", false);

		var validatedFields = ["cc","cvc","exp"];

		for (var i = 0; i < validatedFields.length; i++){
			if (fieldValidity[validatedFields[i]] == false){
				return false;
			}
		}

		btn_checkoutNext.click(verifyPaymentMethod);
		btn_checkoutNext.toggleClass("disabled", false);
	}

	return true
}


function toggleShippingAddress(event){
	shipping_info_container.slideToggle();

	if(btn_chkShippingAddress.is(":checked")){
		shippingIsBilling = true;

		var step_valid = validateCheckoutStep(currentCheckoutStep);

		$(".customer_info_input").each(function(){
			var targetFieldID = $(this).attr('data-fieldID');
			var currentFieldValue =  $(this).val();

			//replace the content in the shipping container to match the billing container, if "Ship to this address" is selected
			if(targetFieldID.indexOf("Billing") >= 0){
				var el = targetFieldID.replace("Billing","Shipping");

				$(".customer_info_input"+el).val(currentFieldValue);
				validateFieldContent(el, currentFieldValue);
			}

		});

	}
	// revalidate the step assuming that shipping info isn't that same as billing info
	else{
		shippingIsBilling = false;
		var step_valid = validateCheckoutStep(currentCheckoutStep);
	}
}




function validateField(fieldID) {
	var targetFieldID = fieldID;
	var selectorString = '[data-fieldID="' + targetFieldID + '"]';
	var currentFieldValue = $(".customer_info_input"+selectorString).val();

	validateFieldContent(targetFieldID, currentFieldValue);
}


function validateFieldEvent(event){
	var targetFieldID = $(event.target).attr('data-fieldID');
	var currentFieldValue = $(event.target).val();
	validateFieldContent(targetFieldID, currentFieldValue);

	console.log("Updating: " + targetFieldID);
	if(shippingIsBilling){
		if(targetFieldID.indexOf("Billing") >= 0){
			var el = '[data-fieldID="' + targetFieldID.replace("Billing","Shipping") + '"]';

			$(".customer_info_input" + el).val($(event.target).val());

			validateFieldContent($(".customer_info_input" + el), currentFieldValue);
			}
	}
}



function validateFieldContent(targetFieldID, currentFieldValue){
	var valid = false;

	console.log(targetFieldID);

	switch(targetFieldID){
		case "cc": 
			valid = $.payment.validateCardNumber(currentFieldValue);
			cardType = $.payment.cardType(currentFieldValue);
			break;
		case "cvc": 
			if(cardType != ""){
				valid = $.payment.validateCardCVC(currentFieldValue, cardType)
			}
			break;
		case "exp": 
			var fv = currentFieldValue.split('/');
			valid = $.payment.validateCardExpiry(fv[0], fv[1]);
			break;
		case "Email": 
			valid = validateEmail(currentFieldValue);
			break;
		case "ShippingFirstName":
			valid = validateName(currentFieldValue);
			break;
		case "ShippingLastName":
			valid = validateName(currentFieldValue);
			break;
		case "ShippingAddress1":
			valid = validateAddress(currentFieldValue);
			break;
		case "ShippingCity":
			valid = validateCity(currentFieldValue);
			break;
		case "ShippingState":
			valid = validateState(currentFieldValue);
			break;
		case "ShippingCountry":
			valid = validateCountry(currentFieldValue);
			break;
		case "ShippingPostalCode":
			valid = validatePostalCode(currentFieldValue);
			break;
		case "BillingFirstName":
			valid = validateName(currentFieldValue);
			break;
		case "BillingLastName":
			valid = validateName(currentFieldValue);
			break;
		case "BillingAddress1":
			valid = validateAddress(currentFieldValue);
			break;
		case "BillingCity":
			valid = validateCity(currentFieldValue);
			break;
		case "BillingState":
			valid = validateState(currentFieldValue);
			console.log(valid);
			break;
		case "BillingCountry":
			valid = validateCountry(currentFieldValue);
			break;
		case "BillingPostalCode":
			valid = validatePostalCode(currentFieldValue);
			break;
		default:
			console.log("No handler for that field.");

	}
		
	fieldValidity[targetFieldID] = valid;

	message = {
				"field":targetFieldID,
				"valid":valid
	}

	updateFieldValidity(message);
}



function updateFieldValidity(message) {
	var fieldID = message["field"];
	var validity = message["valid"];

	var selectorString = '[data-fieldID="' + fieldID + '"]';

	var input_field = $(".customer_info_input"+selectorString);
	
	if(validatedFields.indexOf(fieldID) >= 0) {
		if(validity == true){
			field = input_field.closest('.customer_info_input').closest('.placeholder_addon').toggleClass("green", true);
			field = input_field.closest('.customer_info_input').closest('.placeholder_addon').toggleClass("red", false);
			input_field.css('background-color','#D6FED2');

		}
		else if(validity == false && input_field.val() != ""){
			field = input_field.closest('.customer_info_input').closest('.placeholder_addon').toggleClass("green", false);
			field = input_field.closest('.customer_info_input').closest('.placeholder_addon').toggleClass("red", true);
			input_field.css('background-color','#F6FFF5');


		}
		else{
			input_field.css('background-color','#FFFFFF');
			field = input_field.closest('.customer_info_input').closest('.placeholder_addon').toggleClass("green", false);
			field = input_field.closest('.customer_info_input').closest('.placeholder_addon').toggleClass("red", false);
		}
	}

	var step_valid = validateCheckoutStep(currentCheckoutStep);
}


//some simple regex validators, they just prevent people from being dumb
//server side validation is done on the back end

function validateName(name){
	var re = /^[a-zA-Z\s,'-]+$/;
	return re.test(name);
}

function validateEmail(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}


function validateAddress(address) {
	var re = /^[a-zA-Z0-9\s,'-]+$/;
	return re.test(address);
}


function validatePostalCode(zip) {
	var re = /^[0-9\s-]+$/;
	return re.test(zip);
}

function validateCity(city){
	var re = /^[a-zA-Z\s,'-]+$/;
	return re.test(city);
}


function validateState(state){
	var re = /^[a-zA-Z\s,'-]+$/;
	return re.test(state);
}


function validateCountry(country){
	var re = /^[a-zA-Z\s,'-]+$/;
	return re.test(country);
}


function loadProductThumbnails(){
	$(".product_thumbnail_src").each(function(){

		var product_id = $(this).attr('id').split('_')[1];
		var product_thumbnail_src = $(this).val();

		$("#product_" + product_id).css('background-image',"url('" + product_thumbnail_src + "')");

	});

}
// validation functions
