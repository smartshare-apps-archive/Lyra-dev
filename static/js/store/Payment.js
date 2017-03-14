// basic payment functions, implementing stripe


// basic regex field validation (deprecated)
function validate_field(fieldID, fieldValue){
	$.ajax({
	  method: "POST",
	  url: "/validate/",
	  dataType: "json",
	  data: { fieldID: JSON.stringify(fieldID), fieldValue: JSON.stringify(fieldValue) },
	  traditional: true
	})
	  .done(function(message) {
	  		updateFieldValidity(message);
	  });
}


function verifyPaymentMethod(){
	// cc_info is sent to the stripe servers (encrypted with secret key) to verify payment method
	var cc_info = {
		"number": $("#customer_cc").val(),
		"cvc": $("#customer_cvc").val(),
		"exp_month": parseInt($("#customer_exp").val().split('/')[0]),
		"exp_year": parseInt($("#customer_exp").val().split('/')[1]),
		"address_line1": $("#customer_BillingAddress1").val(),
		"address_line2": $("#customer_BillingAddress2").val(),
		"address_city": $("#customer_BillingCity").val(),
		"address_state": $("#customer_BillingState").val(),
		"address_country": $("#customer_BillingCountry").val(),
		"address_zip": $("#customer_BillingPostalCode").val()
	};

	$("#progress_button").slideToggle();			// show progress button

	Stripe.card.createToken(cc_info, stripeResponseHandler);	// attempt to get a valid token
}


// when a response is returned from stripe.card.createToken, handle the various states
function stripeResponseHandler(status, response) {
	$("#progress_button").slideToggle();		// get rid of the progress button

    var token = response.id;

    if(token){
    	console.log("token:" + token); 	//output token id, for debugging

    	$("#error_message_container").html("");

		var billing_info = {
			"BillingFirstName": $("#customer_BillingFirstName").val(),
			"BillingLastName": $("#customer_BillingLastName").val(),
			"BillingAddress1": response.card["address_line1"],
			"BillingAddress2": response.card["address_line2"],
			"BillingCity": response.card["address_city"],
			"BillingPostalCode": response.card["address_zip"],
			"BillingCountry": response.card["address_country"],
			"BillingState": response.card["address_state"]
		}

		var shipping_info = {
			"ShippingAddress1": $("#customer_ShippingAddress1").val(),
			"ShippingAddress2": $("#customer_ShippingAddress2").val(),
			"ShippingCity": $("#customer_ShippingCity").val(),
			"ShippingState": $("#customer_ShippingState").val(),
			"ShippingPostalCode": $("#customer_ShippingPostalCode").val(),
			"ShippingCountry":  $("#customer_ShippingCountry").val(),
			"ShippingFirstName": $("#customer_ShippingFirstName").val(),
			"ShippingLastName": $("#customer_ShippingLastName").val()
		}

		var billingName = $("#customer_BillingFirstName").val() + " " + $("#customer_BillingLastName").val();

		$("#order_BillingName").html(billingName);
		$("#order_BillingAddress1").html(billing_info["BillingAddress1"]);
    	$("#order_BillingAddress2").html(billing_info["BillingAddress2"]);
		$("#order_BillingCity").html(billing_info["BillingCity"]);
		$("#order_BillingState").html(billing_info["BillingState"]);
		$("#order_BillingPostalCode").html(billing_info["BillingPostalCode"]);
		$("#order_BillingCountry").html(billing_info["BillingCountry"]);

		var shippingName = shipping_info["ShippingFirstName"] + " " + shipping_info["ShippingLastName"];

    	$("#order_ShippingName").html(shippingName);
		$("#order_ShippingAddress1").html(shipping_info["ShippingAddress1"]);
    	
    	if(shipping_info["ShippingAddress2"] == "") {
			$("#order_ShippingAddress2").remove();
		}
		else{
    		$("#order_ShippingAddress2").html(shipping_info["ShippingAddress2"]);
    	}

		$("#order_ShippingCity").html(shipping_info["ShippingCity"]);
		$("#order_ShippingState").html(shipping_info["ShippingState"]);
		$("#order_ShippingPostalCode").html(shipping_info["ShippingPostalCode"]);
		$("#order_ShippingCountry").html(shipping_info["ShippingCountry"]);
  		

  		customer_info = {
  			"ShippingAddress1": shipping_info["ShippingAddress1"],
			"ShippingAddress2": shipping_info["ShippingAddress2"],
			"ShippingCity": shipping_info["ShippingCity"],
			"ShippingPostalCode": shipping_info["ShippingPostalCode"],
			"ShippingCountry": shipping_info["ShippingCountry"],
			"ShippingState": shipping_info["ShippingState"],
			"ShippingFirstName": shipping_info["ShippingFirstName"],
			"ShippingLastName": shipping_info["ShippingLastName"],
			"BillingAddress1": billing_info["BillingAddress1"],
			"BillingAddress2": billing_info["BillingAddress2"],
			"BillingCity": billing_info["BillingCity"],
			"BillingPostalCode": billing_info["BillingPostalCode"],
			"BillingCountry": billing_info["BillingCountry"],
			"BillingState": billing_info["BillingState"],
			"BillingFirstName": billing_info["BillingFirstName"],
			"BillingLastName": billing_info["BillingLastName"],
			"Phone": $("#customer_Phone").val(),
			"Email": $("#customer_Email").val(),
			"Company": $("#customer_Company").val()
  		}

  		// open the confirm order container (to submit order)
    	$("#confirm_order_container").slideToggle();

    	// create an order in the database with status payment=unpaid
    	create_order(response, customer_info);
    }
    else if(response.error){
    	$("#confirm_order_container").css('display','none');
    	$("#error_message_container").html("<b>Verification failed:</b> " + response.error.message);
    }

 	
}


// after a charge is attempted on customer payment method, handle the various charge states
// if failed, get rid of the record and allow them to try another payment method
function paymentResponseHandler(charge){
	if (charge["status"] == "succeeded"){
		window.location.replace('/order_success?ch='+charge["id"]);
	}
	else if(charge["status"] == "pending"){

	}
	// when the charge status turns up as failed, the record in db is deleted
	// if they try to verify again, a new stripe token will be requested
	else if(charge["status"] == "failed"){

		$("#progress_button").slideToggle(); // get rid of progress button

		// hide confirm order button and events
		$("#confirm_order_button").unbind("click");
		$("#confirm_order_container").slideToggle();

		// allow them to go back and change their payment options
		btn_checkoutNext.toggleClass("disabled", false);
		btn_checkoutNext.click(verifyPaymentMethod);

		btn_checkoutPrevious.click(checkoutPrevious);
		btn_checkoutPrevious.toggleClass("disabled", false);

		$("#error_message_container").html(charge.failure_message);
	}
}


// when this is done, allow them to confirm the order and charge card, if they wish
function orderResponseHandler(response){
	btn_checkoutPrevious.unbind("click");
	btn_checkoutNext.unbind("click");

	btn_checkoutNext.toggleClass("disabled", true);
	btn_checkoutPrevious.toggleClass("disabled", true);

	btn_confirmOrder.click({token_id: response["id"], customer_info: response["customer_info"]}, charge_card);
}


// creates a record of the order in the database
function create_order(response, customer_info){
	$.ajax({
	  method: "POST",
	  url: "/create_order/",
	  dataType: "json",
	  data: { response: JSON.stringify(response), customer_info: JSON.stringify(customer_info)},
	  traditional: true
	})
	  .done(function(response) {
	  		orderResponseHandler(response);
	  });
}



function charge_card(event){
	$("#progress_button").slideToggle();

	var token_id = event.data.token_id;
	var customer_info = event.data.customer_info;


	$.ajax({
	  method: "POST",
	  url: "/charge/",
	  dataType: "json",
	  data: { token_id: JSON.stringify(token_id), customer_info: JSON.stringify(customer_info)},
	  traditional: true
	})
	  .done(function(charge) {
	  		paymentResponseHandler(charge);
	  });
}


