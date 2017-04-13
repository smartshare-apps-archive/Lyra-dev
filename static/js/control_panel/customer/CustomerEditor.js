var btn_editShippingInfo;
var btn_updateShippingInfo;
var btn_updateContactInfo;

var btn_saveCustomer;
var btn_confirmCustomerChanges;

var customerData = {}


var selectAll = true;


$(document).ready(function(){
	bindElements();
	bindEvents();

});


function bindElements(){
	btn_editShippingInfo = $("#btn_editShippingInfo");
	btn_updateShippingInfo = $("#btn_updateShippingInfo");
	btn_updateContactInfo = $("#btn_updateContactInfo");

	btn_saveCustomer = $("#btn_saveCustomer");
	btn_confirmCustomerChanges = $("#btn_confirmCustomerChanges");
	customerData["customer_id"] = $("#customer_id").val();

}

function bindEvents(){
	btn_updateShippingInfo.click(updateDisplayFields);
	btn_updateContactInfo.click(updateDisplayFields);

	
	$(".editor_input_field").each(function(){
		var fieldID = $(this).attr('id').split('_')[0];
		$(this).change({fieldID: fieldID}, updateCustomerData);

		customerData[fieldID] = $(this).val();
	});

	btn_confirmCustomerChanges.click(saveCustomerData);
	

	$("#select_all_orders").change(toggleAllOrders);
	
	$(".selectTableItem").each(function(){
		var order_id = $(this).attr('id').split('_')[1];
		console.log(order_id);
		$(this).change({order_id: order_id}, selectOrder);
	});
}	


function confirmPageExit(){
	$("#modal_saveCustomer").modal('show');
}

function updateDisplayFields(){
	$(".editor_input_field").each(function(){
		var fieldID = $(this).attr('id').split('_')[0];
		var fieldValue = $(this).val();
		var span = $("#span_"+fieldID).html(fieldValue);
	});
}


function updateCustomerData(event){
	var fieldID = event.data.fieldID;
	var fieldValue = $("#"+fieldID+"_input").val();

	customerData[fieldID] = fieldValue;
	console.log(customerData);
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
		$("#order_action_bar").css("display","block");
		$("#n_orders_selected").css("display","inline");
		
		if(nOrders == 1){
			$("#n_orders_selected").html("<b>" + nOrders + "</b> order selected ");
		}
		else{
			$("#n_orders_selected").html("<b>" + nOrders + "</b> orders selected ");

		}

	}
	else if (nOrders == 0){
		$("#n_orders_selected").css("display","none");
		$("#order_action_bar").css("display","none");
	}

	selectAll = !selectAll;
}



function selectOrder(event){
	event.stopPropagation();

	selectedOrder = $("#chk_" + event.data.order_id);
	
	
	if(selectedOrder.is(':checked')){
		console.log("SELECTED: " + event.data.order_id);
		selectedOrders[event.data.order_id] = event.data.order_id;
	}
	else{
		delete selectedOrders[event.data.order_id]
	}

	var nOrders = Object.keys(selectedOrders).length;

	if (nOrders > 0){

		$("#order_action_bar").css("display","block");
		$("#n_orders_selected").css("display","inline");
		
		if(nOrders == 1){
			$("#n_orders_selected").html("<b>" + nOrders + "</b> order selected ");
		}
		else{
			$("#n_orders_selected").html("<b>" + nOrders + "</b> orders selected ");

		}

	}
	else if (nOrders == 0){
		 $("#n_orders_selected").css("display", "none");
		 $("#order_action_bar").css("display","none");
	}

}

