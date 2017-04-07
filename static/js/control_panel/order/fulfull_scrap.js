
function toggle_fulfillmentMethod(event){
	var el = $(event.target);
	var methodID = el.attr('id');
	
	if (methodID == "btn_buyLabel" && fulfillmentMethod != "buy_label"){
		fulfillmentMethod = "buy_label";
		$("#btn_buyLabel").prop("checked",true);
		$("#btn_markFulfilled").prop("checked",false);

		toggle_fulfillmentMethodPanels();
	}
	else if(methodID == "btn_markFulfilled" && fulfillmentMethod != "mark_fulfilled"){
		fulfillmentMethod = "mark_fulfilled";
		$("#btn_buyLabel").prop("checked",false);
		$("#btn_markFulfilled").prop("checked",true);
		
		toggle_fulfillmentMethodPanels();
	}
	else{
		el.prop("checked",true);
	}

		
}


function toggle_fulfillmentMethodPanels(){
		cont_buy_label.toggle();
		cont_mark_fulfilled.toggle();
		cont_summary_fulfill.toggle();
		cont_summary_buy_label.toggle();
}
