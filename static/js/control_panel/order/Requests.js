
// basic regex title search
function req_searchProducts(searchTerm, currentSearchFilter, productData){
	$.ajax({
	  method: "POST",
	  url: "/actions/filterProducts",
	  dataType: "json",
	  data: { searchTerm: JSON.stringify(searchTerm), searchFilter: JSON.stringify(currentSearchFilter), productData: JSON.stringify(productData) },
	  traditional: true
	})
	  .done(function( matchIDList ) {
	  		filterResults(matchIDList);
	  });
	 
}




// basic regex title search
function req_filterOrders(searchTerm, currentSearchFilter, orderData){
	$.ajax({
	  method: "POST",
	  url: "/actions/filterOrders",
	  dataType: "json",
	  data: { searchTerm: JSON.stringify(searchTerm), searchFilter: JSON.stringify(currentSearchFilter), orderData: JSON.stringify(orderData) },
	  traditional: true
	})
	  .done(function( matchIDList ) {
	  		filterResults(matchIDList);
	  });
	 
}




function markOrderFulfillment(event){
	var formattedFulfillmentData = ""; 
	var order_id = $("#order_id").val();

	for (key in fulfillmentData){
		var sku = key;
		
		var quantity = String(fulfillmentData[sku]);
		formattedFulfillmentData += (sku + ";" + quantity + ",");
	}

	formattedFulfillmentData = formattedFulfillmentData.slice(0,-1);
	
	$.ajax({
	  method: "POST",
	  url: "/actions/markOrderFulfillment",
	  dataType: "json",
	  data: { sku_fulfilled: JSON.stringify(formattedFulfillmentData), order_id: JSON.stringify(order_id) },
	  traditional: true
	})
	  .done(function( order_id ) {
	  	location.href = "/control/orders/" + order_id;
	  });
}



// bulk functions
function bulkMarkFulfillment(event){
	var order_id_list = [];

	var fulfillment_status = event.data.fulfillment_status;

	for (var key in selectedOrders) {
	    var order_id = selectedOrders[key];
	    order_id_list.push(order_id);
	}
	
	$.ajax({
	  method: "POST",
	  url: "/actions/bulkMarkOrderFulfillment",
	  dataType: "json",
	  data: { fulfillment_status: JSON.stringify(fulfillment_status), order_id_list: JSON.stringify(order_id_list) },
	  traditional: true
	})
	  .done(function( msg ) {
		location.reload();
	  });
	 
}



function bulkMarkPaymentStatus(event){
	var order_id_list = [];

	var payment_status = event.data.payment_status;

	for (var key in selectedOrders) {
	    var order_id = selectedOrders[key];
	    order_id_list.push(order_id);
	}

	$.ajax({
	  method: "POST",
	  url: "/actions/bulkMarkOrderPaymentStatus",
	  dataType: "json",
	  data: { payment_status: JSON.stringify(payment_status), order_id_list: JSON.stringify(order_id_list) },
	  traditional: true
	})
	  .done(function( msg ) {
		location.reload();
	  });
	 
}


function bulkDeleteOrders(event){
	var order_id_list = [];

	for (var key in selectedOrders) {
	    var order_id = selectedOrders[key];
	    order_id_list.push(order_id);
	}

	$.ajax({
	  method: "POST",
	  url: "/actions/bulkDeleteOrders",
	  dataType: "json",
	  data: { order_id_list: JSON.stringify(order_id_list) },
	  traditional: true
	})
	  .done(function( msg ) {
		location.reload();
	  });
	 
}

