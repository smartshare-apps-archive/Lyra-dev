function saveCustomerData(event){
	var customerDataString = JSON.stringify(customerData)
	console.log(customerData);
	$.ajax({
	  method: "POST",
	  url: "/actions/updateCustomerData",
	  dataType: "json",
	  traditional:true,
	  data: { customer_data: customerDataString }
	})
	  .done(function(customer_id) {
			window.location.replace("/control/customers/"+customer_id);
	  });
}



// basic regex title search
function req_filterCustomers(searchTerm, currentSearchFilter, customerData){
	$.ajax({
	  method: "POST",
	  url: "/actions/filterCustomers",
	  dataType: "json",
	  data: { searchTerm: JSON.stringify(searchTerm), searchFilter: JSON.stringify(currentSearchFilter), customerData: JSON.stringify(customerData) },
	  traditional: true
	})
	  .done(function( matchIDList ) {
	  		filterResults(matchIDList);
	  });
	 
}




// bulk functions
function bulkDeleteCustomers(event){
	var customer_id_list = [];

	for (var key in selectedCustomers) {
	    var customer_id = selectedCustomers[key];
	    customer_id_list.push(customer_id);
	}
	
	$.ajax({
	  method: "POST",
	  url: "/actions/bulkDeleteCustomers",
	  dataType: "json",
	  data: { customer_id_list: JSON.stringify(customer_id_list) },
	  traditional: true
	})
	  .done(function( msg ) {
		location.reload();
	  });
	 
}


