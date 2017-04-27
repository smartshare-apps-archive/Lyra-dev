function saveStripeAPIKeys(event){
	//console.log(paymentSettings);
	
	var stripe_api_keys = "secret_key_test:" + paymentSettings["secret_key_test"] + ",publishable_key_test:" + paymentSettings["publishable_key_test"] +",secret_key_live:" + paymentSettings["secret_key_live"] + ",publishable_key_live:" + paymentSettings["publishable_key_live"] + ",payment_status:" + paymentSettings["payment_status"];

	
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



function saveShippoAPIKeys(event){
	console.log(shippingSettings);
	
	var shippo_api_keys = "api_test_token:" + shippingSettings["api_test_token"] + ",api_live_token:" + shippingSettings["api_live_token"] +",shipping_status:" + shippingSettings["shipping_status"];
	
	$.ajax({
	  method: "POST",
	  url: "/actions/saveShippoAPIKeys",
	  dataType: "json",
	  data: { shippo_api_keys: JSON.stringify(shippo_api_keys) },
	  traditional: true
	})
	  .done(function(msg) {
	  	window.location.reload();
	  });
	
}


function saveDefaultShippingAddress(event){
	var default_shipping_address = "ShippingFirstName:" + shippingSettings["ShippingFirstName"] + ";ShippingLastName:" + shippingSettings["ShippingLastName"];
	default_shipping_address += ";ShippingAddress1:" + shippingSettings["ShippingAddress1"] + ";ShippingAddress2:" + shippingSettings["ShippingAddress2"];
	default_shipping_address += ";ShippingCity:" + shippingSettings["ShippingCity"] + ";ShippingState:"+  shippingSettings["ShippingState"];
	default_shipping_address += ";ShippingPostalCode:" + shippingSettings["ShippingPostalCode"] + ";ShippingCountry:"+  shippingSettings["ShippingCountry"] + ";";

	$.ajax({
	  method: "POST",
	  url: "/actions/saveDefaultShippingAddress",
	  dataType: "json",
	  data: { default_shipping_address: JSON.stringify(default_shipping_address) },
	  traditional: true
	})
	  .done(function(msg) {
	  	window.location.reload();
	  });
	

}



function saveRedisConfig(event){
	//host=redis-14464.c10.us-east-1-4.ec2.cloud.redislabs.com<redis_split>port=14464<redis_split>password=S0v1ndiv!#!
	var formatted_redis_config = "";

	for(field in redisConfig){
		formatted_redis_config += field + '=' + redisConfig[field] + '<redis_split>';
	}


	console.log(formatted_redis_config);
	
	$.ajax({
	  method: "POST",
	  url: "/actions/saveRedisConfig",
	  dataType: "json",
	  data: { redis_config: JSON.stringify(formatted_redis_config) },
	  traditional: true
	})
	  .done(function(msg) {
	  	window.location.href = '/control/settings/advanced/';
	  });
	
	
}


function saveDatabaseConfig(event){
	var formatted_database_config = "";

	for(field in databaseConfig){
		formatted_database_config += field + '=' + databaseConfig[field] + '<database_split>';
	}


	console.log(formatted_database_config);
	
	$.ajax({
	  method: "POST",
	  url: "/actions/saveDatabaseConfig",
	  dataType: "json",
	  data: { database_config: JSON.stringify(formatted_database_config) },
	  traditional: true
	})
	  .done(function(msg) {
	  	window.location.href = '/control/settings/advanced/';
	  });
}