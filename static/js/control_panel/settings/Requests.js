function saveStripeAPIKeys(event){
	//console.log(paymentSettings);
	
	var stripe_api_keys = "secret_key:" + paymentSettings["SecretKey"] + ",publishable_key:" + paymentSettings["PublishableKey"];

	
	$.ajax({
	  method: "POST",
	  url: "/actions/saveStripeAPIKeys",
	  dataType: "json",
	  data: { stripe_api_keys: JSON.stringify(stripe_api_keys) },
	  traditional: true
	})
	  .done(function(msg) {
	  	window.location.reload();
	  });
	
}