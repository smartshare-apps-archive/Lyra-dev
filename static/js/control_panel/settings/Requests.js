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



function saveRedisConfig(event){
	console.log("Updating redis config;");

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
	  	window.location.reload();
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
	  	window.location.reload();
	  });
}