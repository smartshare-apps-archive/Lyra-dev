var minimumScroll = 0;
var isPositionFixed = false;
var actionBar;
var customerData = {};
var currentSearchFilter = {"filter":"customer_name"};
var selectAll = true;

//button handles
var btn_addCustomer;


$(document).ready(function(){
		bindElements();
		bindEvents();
		//bindTableEvents();
		setupActionBar();

		$(".customer_data").each(function(){
		var customer_id = $(this).attr('data-customerID');
		customerData[customer_id] = $(this).val();

		});
});

function bindElements(){

}

function bindEvents(){
	//btn_addDraft.click(go_CreateDraft);

	$("#search_filter").change(updateCustomerFilter);
	$("#customer_search_input").keyup(filterCustomers);


	$(".row_customer").each(function(){
		var customerID = $(this).attr('data-customerID');
		$(this).find(".selectTableItem").change({customer_id: customerID}, selectCustomer);
	});

	$("#select_all_customers").change(toggleAllCustomers);

	//bulk action event bindings
	$(".btn_bulk_delete_customers").click(bulkDeleteCustomers);

}


function setupActionBar(){
	actionBar = $("#customer_action_bar");

	$(window).scroll(function(){
		var top = $(this).scrollTop();

		if(top > minimumScroll && isPositionFixed == false){
		isPositionFixed = true;
		actionBar.css("position","fixed");
		actionBar.css("top","0px");
		}
		else if(top < minimumScroll && isPositionFixed == true){
		isPositionFixed = false;
		actionBar.css("position","absolute");
		actionBar.css("top",minimumScroll+"px");
		}

	});

}


// toggles all customers either selected or deselected
function toggleAllCustomers(){
	var customerIDList = $("#customerIDList").val().split(',');
	customerIDList.pop();
	

	for(var i=0;i<customerIDList.length;i++){
		var customer_id = customerIDList[i];

		if(selectAll == true){
			selectedCustomers[customer_id] = customer_id;
		}
		else{
			if (customer_id in selectedCustomers){
				delete selectedCustomers[customer_id];
			}
		}
	}

	if(selectAll){
		$(".selectTableItem").each(function(){
			$(this).prop('checked',true);
		});
	}
	else{
		$(".selectTableItem").each(function(){
			$(this).prop('checked',false);
		});
	}

	var nCustomers = Object.keys(selectedCustomers).length;

	if (nCustomers > 0){
		$("#customer_action_bar").css("display","inline");
		
		if(nCustomers == 1){
			$("#n_customers_selected").html("<b>" + nCustomers + "</b> customer selected ");
		}
		else{
			$("#n_customers_selected").html("<b>" + nCustomers + "</b> customers selected ");

		}

	}
	else if (nCustomers == 0){
		$("#customer_action_bar").css("display","none");
	}

	selectAll = !selectAll;
}

function selectCustomer(event){
	var customer_id = event.data.customer_id;

	var deleteKey = false;		// holds delete/add state
	var selectorString = '[data-customerID="' + customer_id + '"]';

	event.stopPropagation();

	selectedCustomerCheckbox = $("input:checkbox" + selectorString);

	if (customer_id in selectedCustomers){
		deleteKey = true;
		delete selectedCustomers[customer_id]
	}
	else{
		selectedCustomers[customer_id] = customer_id;
	}

	// this ensures that checkboxes in every customer table are updated to reflect the current selection state
	selectedCustomerCheckbox.each(function(){
		if (deleteKey){
			$(this).prop("checked",false);
		}
		else{
			$(this).prop("checked",true);
		}

	});

	var nOrders = Object.keys(selectedCustomers).length;

	if (nOrders > 0){
		$("#customer_action_bar").css("display","inline");
		
		if(nOrders == 1){
			$("#n_customers_selected").html("<b>" + nOrders + "</b> customer selected ");
		}
		else{
			$("#n_customers_selected").html("<b>" + nOrders + "</b> customers selected ");

		}
	}
	else if (nOrders == 0){
		$("#customer_action_bar").css("display","none");
	}
}




function bindTableEvents(){
	$(".row_order").each(function(){
		var orderID = $(this).attr('id').split('_')[1];
		$(this).find(".customer_id").attr("href","/control/orders/"+orderID);

	});

}



// basic title search functions below

function updateCustomerFilter(event){
	currentSearchFilter = {"filter": $(event.target).val()};
	filterCustomers();
}


function filterCustomers(event){
	var currentInput = {"input": $("#customer_search_input").val()};
	req_filterCustomers(currentInput, currentSearchFilter,customerData);
}


function filterResults(matchIDList){
	//console.log(matchIDList);
	$(".row_customer").each(function(){
		var customer_id = $(this).attr('data-customerID');
		var inMatchList = matchIDList.indexOf(customer_id);
		
		if(inMatchList < 0){
			$(this).hide();
		}
		else{
			$(this).show();
		}

	});


}
