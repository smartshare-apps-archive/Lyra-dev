
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



/* functions to deal with shipment generation and fulfillment */

function createShipmentObject(){
	shipment_obj = null;

	$("#wait-glyph-01").css("display","block");


	$.ajax({
	  method: "POST",
	  url: "/actions/createShipmentObject",
	  dataType: "json",
	  data: { order_id: JSON.stringify(order_id), shipping_address_to: JSON.stringify(shippingAddress_to), shipping_address_from: JSON.stringify(shippingAddress_from), parcel_data: JSON.stringify(parcelData) },
	  traditional: true
	})
	  .done(function( response ) {

	  		shipment_obj = response; // store shipment object for later use

	  		currentCarrierRates = [];
	  		currentCarrierRates = response.rates;

	  		parseShippingRates();

	  		$("#wait-glyph-01").css("display","none");
	  		//$("#shipment_output_cont").html("Success.");

	  });

}


function generateShippingLabel(event){
	var selected_option = event.data.selected_option;

	$("#wait-glyph-02").css("display","block");

	$.ajax({
	  method: "POST",
	  url: "/actions/generateShippingLabel",
	  dataType: "json",
	  data: { order_id: JSON.stringify(order_id), shipment_obj: JSON.stringify(shipment_obj), selected_option: JSON.stringify(selected_option) },
	  traditional: true
	})
	  .done(function( response ) {
	  		$("#wait-glyph-02").css("display","none");

	  		if("error_messages" in response){
	  			console.log("Error generating label.");
	  		}
	  		else{
	  			generated_label_data.html("");
	  			var labelHTML = "";
	  			labelHTML += "Tracking number: &nbsp;&nbsp;<b>" + response["tracking_number"] + "</b><br><br>";
	  			labelHTML += "<a href=\"" + response["label_url"] + "\" target=\"" + "_blank\"><button type=\"button\" class=\"btn btn-primary btn-lg\"> <span class=\"glyphicon glyphicon-barcode\"></span> &nbsp;&nbsp; Click for label </button></a>";

	  			generated_label_data.append(labelHTML);


	  		}
	  		

	  });

}