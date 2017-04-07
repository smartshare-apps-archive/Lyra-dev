var btn_buyLabel;
var btn_markFulfilled;
var btn_btn_fulfillItems;

var cont_buy_label;
var cont_mark_fulfilled;

var cont_summary_buy_label;
var cont_summary_fulfill;

var fulfillmentMethod = "mark_fulfilled"

// store shipping info in case of updates
var shippingInfo = {}
var fulfillmentData;


$(document).ready(function(){
	bindElements();
	bindEvents();
	updateItemFulfillmentState();
});


function bindElements(){
	btn_buyLabel = $("#btn_buyLabel");
	btn_markFulfilled = $("#btn_markFulfilled");
	btn_fulfillItems = $("#btn_fulfillItems");

	cont_buy_label = $("#cont_buy_label");
	cont_mark_fulfilled = $("#cont_mark_fulfilled");
	cont_summary_fulfill = $("#cont_summary_fulfill");
	cont_summary_buy_label = $("#cont_summary_buy_label");


}


function bindEvents(){
	btn_buyLabel.click(toggle_fulfillmentMethod);
	btn_markFulfilled.click(toggle_fulfillmentMethod);


	$(".order_product_fulfillment").each(function(){
		var product_id = $(this).attr('data-productID');
		$(this).click({product_id: product_id}, selectOrderProduct);
	});

}


function updateItemFulfillmentState(){
	$(".order-fulfillment-glyph").each(function(){
		var product_id = $(this).attr('data-productID');

		/*
		console.log(fulfillmentData[product_id]);

		if(fulfillmentData[product_id] == 0){
			$(this).html("<span class=\"glyph-fulfilled glyphicon glyphicon-remove\"></span>");
		}
		else{
			$(this).html("<span class=\"glyph-fulfilled glyphicon glyphicon-ok\"></span>");		
			}
		*/
	});
}



function selectOrderProduct(event){
	var product_id = event.data.product_id;
	var selectorString = '[data-productID="' + product_id + '"]';

	var currentProductContainer = $(".order_product_fulfillment" + selectorString);

	currentProductContainer.css({
		'opacity':'1.0',
		'border':'3px solid #5CB85C'
	});
}








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




