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
var fulfillmentData = {};
var shippingData = {};


$(document).ready(function(){
	bindElements();
	bindEvents();

	parseShippingData();
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
	//btn_buyLabel.click(toggle_fulfillmentMethod);
	//btn_markFulfilled.click(toggle_fulfillmentMethod);


	$(".order_product_fulfillment").each(function(){
		var product_id = $(this).attr('data-productID');
		$(this).click({product_id: product_id}, selectOrderProduct);
	});

}




// parses the shipment data for this order to allow for the viewing of tracking info and shipping labels
function parseShippingData(){
	// go through each shipment linked to this order by order_id
	$(".shipment-data").each(function(){

		var shipment_id = $(this).attr('data-shipmentID');
		var currentShipmentData = replaceAll($(this).val(),'u\'','\'');

		// bunch of garbage cleanup for JSON parsing (replace later)
		currentShipmentData = replaceAll(currentShipmentData, '\'', '\"');
		currentShipmentData = replaceAll(currentShipmentData, 'L,', ',');
		currentShipmentData = replaceAll(currentShipmentData, 'L}', '}');
		currentShipmentData = JSON.parse(currentShipmentData);

		shippingData[shipment_id] = currentShipmentData;
	});

	// go through each parcel to determine which products it contains
	for (shipment_id in shippingData){
		var shipment_products = shippingData[shipment_id]["SKU_List"].split(';');

		shipment_products.pop();	// remove last empty element from list of products and their quantities

		// extract current fulfillment data for each product 
		for(var i=0;i<shipment_products.length;i++){
			var currentProduct = shipment_products[i].split(':');
			
			var product_sku = currentProduct[0];
			var product_qty = parseInt(currentProduct[1]);
			
			if(product_sku in fulfillmentData){
				fulfillmentData[product_sku] += product_qty;
			}
			else{
				fulfillmentData[product_sku] = product_qty;
			}
		}

	}

}





function updateItemFulfillmentState(){
	$(".order-fulfillment-glyph").each(function(){
		var product_sku = $(this).attr('data-productSKU');
		var selectorString = '[data-productSKU="' + product_sku + '"]';
		var product_qty = parseInt($(".order-product-qty" + selectorString).val());

		console.log(fulfillmentData[product_sku]);

		if(fulfillmentData[product_sku] < product_qty || (!(product_sku in fulfillmentData))){
			$(this).html("<span class=\"glyph-fulfilled glyphicon glyphicon-remove\"></span>");
		}

		else{
			$(this).html("<span class=\"glyph-fulfilled glyphicon glyphicon-ok\"></span>");		
		}
	

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











