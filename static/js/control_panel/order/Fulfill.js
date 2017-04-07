var btn_buyLabel;
var btn_markFulfilled;
var btn_btn_fulfillItems;
var btn_createNewShipment;

var cont_buy_label;
var cont_mark_fulfilled;

var cont_summary_buy_label;
var cont_summary_fulfill;
var shipment_products_table;

var fulfillmentMethod = "mark_fulfilled"


// store shipping info in case of updates
var shippingInfo = {}

var fulfillmentData = {};
var shippingData = {};
var selectedProducts = {};
var productData = {};



$(document).ready(function(){
	bindElements();
	bindEvents();

	populateProductData();
	parseShippingData();
	updateItemFulfillmentState();
});


function bindElements(){
	btn_buyLabel = $("#btn_buyLabel");
	btn_markFulfilled = $("#btn_markFulfilled");
	btn_fulfillItems = $("#btn_fulfillItems");
	btn_createNewShipment = $("#btn_createNewShipment");

	cont_buy_label = $("#cont_buy_label");
	cont_mark_fulfilled = $("#cont_mark_fulfilled");
	cont_summary_fulfill = $("#cont_summary_fulfill");
	cont_summary_buy_label = $("#cont_summary_buy_label");


	shipment_products_table = $("#shipment_products_table");
}



// why is this empty dumby
function bindEvents(){




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

// loads product metadata from the page to allow for table data population later on
function populateProductData(){
	$(".product-data").each(function(){
		var product_sku = $(this).attr('data-productSKU');
		var fieldID = $(this).attr('data-fieldID');

		if(product_sku in productData){
			productData[product_sku][fieldID] = $(this).val();
		}
		else{
			productData[product_sku] = {}
			productData[product_sku][fieldID] = $(this).val();
		}
	});
}



// pushs selected product data into shipping label generation modal or manual fulfillment modal
function populateProductTable(){
	shipment_products_table.html("");

	var tableTemplateHTML = "<table class=\"table table-bordered table-hover\" id=\"shipment_products\">";
	tableTemplateHTML += "<thead>";
	tableTemplateHTML += "<th> Product </th>";
	tableTemplateHTML += "<th> Variant SKU </th>";
	tableTemplateHTML += "<th> Weight </th>";
	tableTemplateHTML += "<th> Quantity </th>";
	tableTemplateHTML += "</thead>";
	tableTemplateHTML += "<tbody>";

	for(product_sku in selectedProducts){
		var totalQty = parseInt(productData[product_sku]["Quantity"]);

		if(!(product_sku in fulfillmentData)){
			var remainingQty = totalQty;
		}
		else{
			var fulfilledQty = fulfillmentData[product_sku];
			var remainingQty = totalQty - fulfilledQty;

		}
		
		var quantity_range = range(1, remainingQty, 1);
	
		var productQtyDropdown = "<select class=\"shipment-product-qty form-control\" data-productSKU=\"" + product_sku + "\">"; 

		for(var i=0;i<quantity_range.length;i++){
			productQtyDropdown += "<option value=\""+quantity_range[i] + "\">" + quantity_range[i] + "</option>";
		}

		productQtyDropdown += "</select>";

		tableTemplateHTML += "<tr>";
		tableTemplateHTML += "<td>" + productData[product_sku]["Title"] + "</td>";
		tableTemplateHTML += "<td>" + product_sku + "</td>";
		tableTemplateHTML += "<td>" + productData[product_sku]["Weight"] + "</td>";
		tableTemplateHTML += "<td>" + productQtyDropdown + "</td>";
		tableTemplateHTML += "</tr>";
	}

	tableTemplateHTML += "</tbody></table><hr>";

	shipment_products_table.append(tableTemplateHTML);
}







function updateItemFulfillmentState(){
	$(".order-fulfillment-glyph").each(function(){
		var product_sku = $(this).attr('data-productSKU');
		var selectorString = '[data-productSKU="' + product_sku + '"]';
		var product_qty = parseInt($(".order-product-qty" + selectorString).val());

		// this item is not fulfilled, so it is clickable to allow adding to package
		if(fulfillmentData[product_sku] < product_qty || (!(product_sku in fulfillmentData))){
			$(this).html("<span class=\"glyph-fulfilled glyphicon glyphicon-remove\"></span>");
				
				// on click enabled
				$(".order_product_fulfillment" + selectorString).click({product_sku: product_sku}, toggleProductSelection);		
		}

		// this item has been fulfilled
		else{
			$(this).html("<span class=\"glyph-fulfilled glyphicon glyphicon-ok\"></span>");	

			// unbind any click events and reset the cursor to standard
			$(".order_product_fulfillment" + selectorString).css('cursor','initial');
			$(".order_product_fulfillment" + selectorString).unbind();
		}
	

	});
}



function toggleProductSelection(event){
	var product_sku = event.data.product_sku;
	var selectorString = '[data-productSKU="' + product_sku + '"]';

	var currentProductContainer = $(".order_product_fulfillment" + selectorString);

	if(product_sku in selectedProducts){
		delete selectedProducts[product_sku];

		currentProductContainer.css({
			'opacity':'1.0',
			'border':'1px solid black'
		});
	}
	else{
		selectedProducts[product_sku] = product_sku;
		
		currentProductContainer.css({
			'opacity':'1.0',
			'border':'3px solid #5CB85C'
		});
	}
	
	var nSelectedProducts = Object.keys(selectedProducts).length;
	
	if(nSelectedProducts > 0){
		btn_createNewShipment.toggleClass("disabled",false);
		btn_markFulfilled.toggleClass("disabled",false);

		btn_createNewShipment.attr('data-toggle','modal');
		btn_markFulfilled.attr('data-toggle','modal');

		populateProductTable();
		
		bindShipmentModalEvents();
	}
	else{
		btn_createNewShipment.toggleClass("disabled",true);
		btn_markFulfilled.toggleClass("disabled",true);

		btn_createNewShipment.removeAttr("data-toggle");
		btn_markFulfilled.removeAttr("data-toggle");
	}
}


function bindShipmentModalEvents(){
	var btn_genShipmentObj = $("#btn_genShipmentObj");
	btn_genShipmentObj.unbind();
	btn_genShipmentObj.click({order_id: 2}, createShipmentObject);

}




function range(start, end, inc){
	var a = [];
	for(var i=start;i<=end;i+=inc){
		a.push(i);
	}
	return a
}