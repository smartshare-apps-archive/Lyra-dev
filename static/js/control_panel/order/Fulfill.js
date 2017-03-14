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
	loadProductThumbnails();
	getFulfillmentData();
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
	btn_fulfillItems.click(markOrderFulfillment);

	// for the shipping address change modal
	$("#modal_editShippingAddress").find('.form-control').each(function(){
		field = $(this).attr('id').split('_')[0];
		shippingInfo[field] = $(this).val();
		$(this).change(registerShippingChange);
	});

	$(".product_row").each(function(){
		var product_id = $(this).attr('data-productID');
		var product_sku = $(this).attr('data-productSKU');

		var product_quantity = $(this).find(".product_quantity").val();
		var select_quantity = $(this).find(".select_product_quantity");
		//select_quantity.val(product_quantity);

		select_quantity.change({product_sku:product_sku}, updateFulfillmentData);
	});
}



function updateFulfillmentData(event){
	var product_sku = event.data.product_sku;
	var selectorString = '[data-productSKU="' + product_sku + '"]';

	var select_quantity = $("select" + selectorString);
	var fulfillment_quantity = parseInt(select_quantity.val());

	fulfillmentData[product_sku] = fulfillment_quantity;
}


function getFulfillmentData(){
	fulfillmentData = {}
	var raw_fulfillmentData = $("#sku_fulfillment").val();
	
	raw_fulfillmentData = raw_fulfillmentData.split(',');

	for(var i=0;i<raw_fulfillmentData.length;i++){
		var current_item = raw_fulfillmentData[i].split(';');
		fulfillmentData[current_item[0]] = current_item[1];
	}
}

function registerShippingChange(event){
	var element = $(event.target);
	var newValue = $(element).val();
	var field = event.target.id.split('_')[0];
	shippingInfo[field] = newValue;
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



function loadProductThumbnails(){
	$(".thumbnail_product_40").each(function(){
		var currentImageURL = $(this).find('.product_img_src').val();
		$(this).css('background-image',"url('"+currentImageURL+"')");
	});

}
