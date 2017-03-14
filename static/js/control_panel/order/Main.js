var minimumScroll = 0;
var isPositionFixed = false;
var actionBar;
var orderData = {};
var currentSearchFilter = {"filter":"customer_name"};
var selectAll = true;

//button handles
var btn_addDraft;


$(document).ready(function(){
		bindElements();
		bindEvents();
		bindTableEvents();
		setupActionBar();

		$(".order_data").each(function(){
			var order_id = $(this).attr('data-orderID');
			orderData[order_id] = $(this).val();

		});

});

function bindElements(){
	btn_addDraft = $("#btn_addDraft");

}

function bindEvents(){
	btn_addDraft.click(go_CreateDraft);

	$("#search_filter").change(updateOrderFilter);
	$("#order_search_input").keyup(filterOrders);

	$("#select_all_orders").change(toggleAllOrders);

	$(".row_order").each(function(){
		var orderID = $(this).attr('data-orderID');
		$(this).find(".selectTableItem").change({order_id: orderID}, selectOrder);
	});


	$(".btn_bulk_mark_fulfilled").click({fulfillment_status:"fulfilled"}, bulkMarkFulfillment);
	$(".btn_bulk_mark_unfulfilled").click({fulfillment_status:"unfulfilled"}, bulkMarkFulfillment);

	$(".btn_bulk_mark_paid").click({payment_status:"paid"}, bulkMarkPaymentStatus);
	$(".btn_bulk_mark_pending").click({payment_status:"pending"}, bulkMarkPaymentStatus);
	$(".btn_bulk_mark_unpaid").click({payment_status:"unpaid"}, bulkMarkPaymentStatus);

	$(".btn_bulk_delete_orders").click(bulkDeleteOrders);

}


function bindTableEvents(){
	$(".row_order").each(function(){
		var orderID = $(this).attr('data-orderID');
		$(this).find(".order_link").attr("href","/control/orders/"+orderID);

	});

}

function go_CreateDraft(){
	window.location.href = "/control/orders/addDraft";
}


function go_OrderEditor(event){
	window.location.href = "/control/orders/"+event.data.order_id;
}



function setupActionBar(){
	actionBar = $("#order_action_bar_main");

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


// toggles all orders either selected or deselected
function toggleAllOrders(){
	var orderIDList = $("#orderIDList").val().split(',');
	orderIDList.pop();
	

	for(var i=0;i<orderIDList.length;i++){
		var order_id = orderIDList[i];

		if(selectAll == true){
			selectedOrders[order_id] = order_id;
		}
		else{
			if (order_id in selectedOrders){
				delete selectedOrders[order_id];
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

	var nOrders = Object.keys(selectedOrders).length;

	if (nOrders > 0){
		$("#order_action_bar_main").css("display","inline");
		
		if(nOrders == 1){
			$("#n_orders_selected").html("<b>" + nOrders + "</b> order selected ");
		}
		else{
			$("#n_orders_selected").html("<b>" + nOrders + "</b> orders selected ");

		}

	}
	else if (nOrders == 0){
		$("#order_action_bar_main").css("display","none");
	}

	selectAll = !selectAll;
}



function selectOrder(event){
	var order_id = event.data.order_id;

	var deleteKey = false;		// holds delete/add state
	var selectorString = '[data-orderID="' + order_id + '"]';

	event.stopPropagation();

	selectedOrderCheckbox = $("input:checkbox" + selectorString);

	// deletes or adds the order_id to the selectedOrders dict
	if (order_id in selectedOrders){
		deleteKey = true;
		delete selectedOrders[order_id]
	}
	else{
		selectedOrders[order_id] = order_id;
	}

	// this ensures that checkboxes in every order table are updated to reflect the current selection state
	selectedOrderCheckbox.each(function(){
		if (deleteKey){
			$(this).prop("checked",false);
		}
		else{
			$(this).prop("checked",true);
		}

	});

	var nOrders = Object.keys(selectedOrders).length;

	if (nOrders > 0){
		$("#order_action_bar_main").css("display","inline");
		
		if(nOrders == 1){
			$("#n_orders_selected").html("<b>" + nOrders + "</b> order selected ");
		}
		else{
			$("#n_orders_selected").html("<b>" + nOrders + "</b> orders selected ");

		}
	}
	else if (nOrders == 0){
		$("#order_action_bar_main").css("display","none");
	}
}





// basic title search functions below

function updateOrderFilter(event){
	currentSearchFilter = {"filter": $(event.target).val()};
	filterOrders();
}

function filterOrders(event){
	var currentInput = {"input": $("#order_search_input").val()};
	req_filterOrders(currentInput, currentSearchFilter,orderData);
}


function filterResults(matchIDList){

	$(".row_order").each(function(){
		var order_id = $(this).attr('data-orderID');
		var inMatchList = matchIDList.indexOf(order_id);
		
		if(inMatchList < 0){
			$(this).hide();
		}
		else{
			$(this).show();
		}

	});


}
