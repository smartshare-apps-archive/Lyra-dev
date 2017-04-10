var btn_buyLabel;
var btn_markFulfilled;
var btn_fulfillItems;
var btn_createNewShipment;
var btn_saveShipment;

var cont_buy_label;
var cont_mark_fulfilled;

var cont_summary_buy_label;
var cont_summary_fulfill;

// various table handles
var shipment_products_table;
var shipment_details_table;
var generated_label_data;
var shipment_options_table;
var selected_shipping_method;
var order_shipment_details;


var fulfillmentData = {};
var orderFulfilled;

var shippingAddress_to = {};
var shippingAddress_from = {};

var shippingData = {};
var selectedProducts = {};
var productData = {};
var parcelData = {};

var currentCarrierRates = [];
var parsedCarrierRates = [];

var currentShipmentDetails;

//store shipment obj response from shippo locally
var shipment_obj;
var order_id;

$(document).ready(function(){
	bindElements();
	bindEvents();

	populateProductData();
	populateShippingAddress();

	parseShippingData();
	updateItemFulfillmentState();
	
});


function bindElements(){
	btn_buyLabel = $("#btn_buyLabel");
	btn_markFulfilled = $("#btn_markFulfilled");
	btn_fulfillItems = $("#btn_fulfillItems");
	btn_createNewShipment = $("#btn_createNewShipment");
	btn_saveShipment = $("#btn_saveShipment");

	cont_buy_label = $("#cont_buy_label");
	cont_mark_fulfilled = $("#cont_mark_fulfilled");
	cont_summary_fulfill = $("#cont_summary_fulfill");
	cont_summary_buy_label = $("#cont_summary_buy_label");

	order_shipment_details = $("#order_shipment_details");
	shipment_products_table = $("#shipment_products_table");
	shipment_details_table = $("#shipment_details_table");
	shipment_options_table = $("#shipment_options_table");
	selected_shipping_method = $("#selected_shipping_method");

	generated_label_data = $("#generated_label_data");

	order_id = parseInt($("#order_id").val());
}



function bindEvents(){



	btn_fulfillItems.click(fulfillManually);
}


function populateShippingAddress(){
	$(".shipping-address-to-data").each(function(){
		var fieldID = $(this).attr('data-fieldID');
		shippingAddress_to[fieldID] = $(this).val();
	});


	$(".shipping-address-from-data").each(function(){
		var fieldID = $(this).attr('data-fieldID');
		shippingAddress_from[fieldID] = $(this).val();
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

	//console.log(shippingData);
	order_shipment_details.html("");


	for(shipment_id in shippingData){
		var shipmentDetailsHTML = "";



		shipmentDetailsHTML += "Tracking number: " + shippingData[shipment_id]["TrackingNumber"] + "<br>";
		shipmentDetailsHTML += "Carrier: " + shippingData[shipment_id]["Carrier"] + "<br>";

		if(shippingData[shipment_id]["FulfillmentMethod"] == "manual"){
			shipmentDetailsHTML += "Fulfillment method: " + shippingData[shipment_id]["FulfillmentMethod"] + "<br><br>";
		}
		else{
			shipmentDetailsHTML += "Fulfillment method: " + shippingData[shipment_id]["FulfillmentMethod"] + "<br><br>";
			shipmentDetailsHTML += "<a href=\"" + shippingData[shipment_id]["LabelURL"] + "\" target=\"" + "_blank\"><button type=\"button\" class=\"btn btn-primary\"> <span class=\"glyphicon glyphicon-barcode\"></span> &nbsp;&nbsp; Click for label </button></a>";
		}


		shipmentDetailsHTML += "<button type=\"button\" class=\"btn btn-default btn-view-shipment-products\" data-shipmentID=\"" + shipment_id + "\"> <span class=\"glyphicon glyphicon-tag\"></span> &nbsp;&nbsp; Show products </button>";
		shipmentDetailsHTML += "<button type=\"button\" class=\"btn btn-danger pull-right btn-delete-shipment\" data-shipmentID=\"" + shipment_id + "\"> <span class=\"glyphicon glyphicon-remove\"></span> &nbsp;&nbsp; Delete Shipment </button><br>";

		shipmentDetailsHTML += "<div class=\"shipment-product-table\" data-shipmentID=\"" + shipment_id + "\"> </div>";
		
		shipmentDetailsHTML += "<hr>";

		order_shipment_details.append(shipmentDetailsHTML);
		
		var selectorString = '[data-shipmentID="' + shipment_id + '"]';
		
		populateProductTable_shipment(shipment_id);

		$(".btn-view-shipment-products" + selectorString).click({shipment_id: shipment_id}, toggleShipmentProductTable);
		$(".btn-delete-shipment" + selectorString).click({shipment_id: shipment_id}, deleteOrderShipment);
	}


}

function toggleShipmentProductTable(event){
	var shipment_id = event.data.shipment_id;

	var selectorString = '[data-shipmentID="' + String(shipment_id) + '"]';  
	var containerToToggle = $(".shipment-product-table" + selectorString);
	var toggleBtn = $(".btn-view-shipment-products" + selectorString);


	var currentDisplayMode = containerToToggle.css('display');

	if(currentDisplayMode == 'none'){
		containerToToggle.slideToggle();
		toggleBtn.html("<span class=\"glyphicon glyphicon-tag\"></span> &nbsp;&nbsp; Hide products </button>");

	}	
	else{
		containerToToggle.slideToggle();
		toggleBtn.html("<span class=\"glyphicon glyphicon-tag\"></span> &nbsp;&nbsp; Show products </button>");
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
function populateProductTable(containerID){
	var containerToPopulate = $("#"+containerID);

	containerToPopulate.html("");

	var tableTemplateHTML = "<table class=\"table table-bordered table-hover\">";
	tableTemplateHTML += "<thead>";
	tableTemplateHTML += "<th> Product </th>";
	tableTemplateHTML += "<th> Variant SKU </th>";
	tableTemplateHTML += "<th> Weight (kg) </th>";
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

		if(containerID == "shipment_products_table_manual"){
			var productQtyDropdown = "<select class=\"shipment-product-qty  manual form-control\" data-productSKU=\"" + product_sku + "\">"; 
		}
		else if(containerID == "shipment_products_table_ship"){
			var productQtyDropdown = "<select class=\"shipment-product-qty shippo form-control\" data-productSKU=\"" + product_sku + "\">"; 
		}

		for(var i=0;i<quantity_range.length;i++){
			productQtyDropdown += "<option value=\""+quantity_range[i] + "\">" + quantity_range[i] + "</option>";
		}

		productQtyDropdown += "</select>";

		tableTemplateHTML += "<tr>";
		tableTemplateHTML += "<td>" + productData[product_sku]["Title"] + "</td>";
		tableTemplateHTML += "<td>" + product_sku + "</td>";
		tableTemplateHTML += "<td>" + (productData[product_sku]["Weight"]/1000) + "</td>";
		tableTemplateHTML += "<td>" + productQtyDropdown + "</td>";
		tableTemplateHTML += "</tr>";
	}

	tableTemplateHTML += "</tbody></table><hr>";

	containerToPopulate.append(tableTemplateHTML);


	if(containerID == "shipment_products_table_manual"){

		$(".shipment-product-qty.manual").each(function(){
			var product_sku = $(this).attr('data-productSKU');

			$(this).unbind();
			$(this).change({fulfillment_method: "manual"} ,calculateParcelData);
			
		});
	}
	else if(containerID == "shipment_products_table_ship"){

		$(".shipment-product-qty.shippo").each(function(){
			var product_sku = $(this).attr('data-productSKU');

			$(this).unbind();
			$(this).change({fulfillment_method: "shippo"} ,calculateParcelData);
			
		});
	}

	//calculates initial parcel data
	calculateParcelData();

	var shipment_options_table = $("#shipment_options_table");
	var selected_shipping_method = $("#selected_shipping_method");

	shipment_options_table.html("");
	selected_shipping_method.html("");
	generated_label_data.html("");
}



// 
function populateProductTable_shipment(shipment_id){
	var selectorString = '[data-shipmentID="' + String(shipment_id) + '"]';  
	var containerToPopulate = $(".shipment-product-table" + selectorString);

	containerToPopulate.html("");

	var tableTemplateHTML = "<hr><table class=\"table table-bordered table-hover\">";
	tableTemplateHTML += "<thead>";
	tableTemplateHTML += "<th> Product </th>";
	tableTemplateHTML += "<th> Variant SKU </th>";
	tableTemplateHTML += "<th> Weight (kg) </th>";
	tableTemplateHTML += "<th> Quantity </th>";
	tableTemplateHTML += "</thead>";
	tableTemplateHTML += "<tbody>";

	var shipment_products = shippingData[shipment_id]["SKU_List"].split(';');

	shipment_products.pop();	// remove last empty element from list of products and their quantities

	// extract current fulfillment data for each product 
	for(var i=0;i<shipment_products.length;i++){
		var currentProduct = shipment_products[i].split(':');
		
		var product_sku = currentProduct[0];
		var product_qty = currentProduct[1];

		tableTemplateHTML += "<tr>";
		tableTemplateHTML += "<td>" + productData[product_sku]["Title"] + "</td>";
		tableTemplateHTML += "<td>" + product_sku + "</td>";
		tableTemplateHTML += "<td>" + (productData[product_sku]["Weight"]/1000) + "</td>";
		tableTemplateHTML += "<td>" + product_qty +  "</td>";
		tableTemplateHTML += "</tr>";
	}

	tableTemplateHTML += "</tbody></table><hr>";

	containerToPopulate.append(tableTemplateHTML);

}


function populateShipmentDetailsTable(){
	shipment_details_table.html("");

	var tableTemplateHTML = "<table class=\"table table-bordered table-hover\" id=\"shipment_details\">";
	tableTemplateHTML += "<thead>";
	tableTemplateHTML += "<th> Number of items </th>";
	tableTemplateHTML += "<th> Total Weight (kg) </th>";
	tableTemplateHTML += "</thead>";
	tableTemplateHTML += "<tbody>";

	tableTemplateHTML += "<tr>";
	tableTemplateHTML += "<td>" + parcelData["ItemCount"] + "</td>";
	tableTemplateHTML += "<td>" + parcelData["Weight"] + "</td>";
	tableTemplateHTML += "</tr>";

	//console.log(parcelData);

	tableTemplateHTML += "</tbody></table><hr>";

	shipment_details_table.append(tableTemplateHTML);

}



function modal_loadShippingAddressTo(){
	var shippingAddressToContainer = $("#shippingAddressTo");
	var shippingAddressFromContainer = $("#shippingAddressFrom");

	shippingAddressFromContainer.html("<h4>Ship from:</h4>");
	shippingAddressToContainer.html("<h4>Ship to:</h4>");

	var addressHTML = "";

	addressHTML += shippingAddress_to["ShippingFirstName"] + " " + shippingAddress_to["ShippingLastName"] + "<br>";
	addressHTML += shippingAddress_to["ShippingAddress"] + "<br>";

	if(shippingAddress_to["ShippingAddress2"] != ""){
		addressHTML += shippingAddress_to["ShippingAddress2"] + "<br>";
	}

	addressHTML += shippingAddress_to["ShippingCity"] + ",&nbsp;" + shippingAddress_to["ShippingState"] + "&nbsp;&nbsp;" + shippingAddress_to["ShippingPostalCode"] + "<br>";

	addressHTML += shippingAddress_to["ShippingCountry"] + "<br>";
	
	shippingAddressToContainer.append(addressHTML);	



	var addressHTML = "";

	addressHTML += shippingAddress_from["ShippingFirstName"] + " " + shippingAddress_from["ShippingLastName"] + "<br>";
	addressHTML += shippingAddress_from["ShippingAddress1"] + "<br>";

	if(shippingAddress_from["ShippingAddress2"] != ""){
		addressHTML += shippingAddress_from["ShippingAddress2"] + "<br>";
	}

	addressHTML += shippingAddress_from["ShippingCity"] + ",&nbsp;" + shippingAddress_from["ShippingState"] + "&nbsp;&nbsp;" + shippingAddress_from["ShippingPostalCode"] + "<br>";

	addressHTML += shippingAddress_from["ShippingCountry"] + "<br>";
	shippingAddressFromContainer.append(addressHTML);	


}



function calculateParcelData(event){
	if(typeof event == 'undefined'){
		var fulfillment_method = "shippo";
	}
	else{
		var fulfillment_method = event.data.fulfillment_method;
	}

	console.log(fulfillment_method);

	parcelData = {};

	if(fulfillment_method == "shippo"){
		$(".shipment-product-qty.shippo").each(function(){
			var product_sku = $(this).attr('data-productSKU');
			var product_qty = $(this).val();

			//console.log(product_sku + ":" + product_qty);
			parcelData[product_sku] = parseInt(product_qty);
		});
	}
	else if(fulfillment_method == "manual"){
		$(".shipment-product-qty.manual").each(function(){
			var product_sku = $(this).attr('data-productSKU');
			var product_qty = $(this).val();

			//console.log(product_sku + ":" + product_qty);
			parcelData[product_sku] = parseInt(product_qty);
		});
	}


	var totalItemCount = 0;
	var totalParcelWeight = 0.00; //total weight in grams, can be converted later if necessary

	for(product_sku in parcelData){
		var productUnitWeight = productData[product_sku]["Weight"];
		var product_qty = parcelData[product_sku];

		var totalWeight = product_qty * productUnitWeight;
		//console.log(productUnitWeight + ":" + totalWeight);

		totalItemCount += product_qty;
		totalParcelWeight += totalWeight;

	}

	parcelData["Weight"] = (totalParcelWeight/1000);
	parcelData["ItemCount"] = totalItemCount;

	populateShipmentDetailsTable();

	shipment_options_table.html("");
	selected_shipping_method.html("");
	generated_label_data.html("");

	console.log(parcelData);
}



function parseShippingRates(){
	parsedCarrierRates = [];

	for(var i=0;i<currentCarrierRates.length;i++){
		var currentRate = currentCarrierRates[i];
		parsedCarrierRates.push({});

		var provider = currentRate["provider"];
		var nDaysToDest = currentRate["days"];
		var cost = currentRate["amount"];
		var currency = currentRate["currency"];
		var duration_terms = currentRate["duration_terms"];
		
		parsedCarrierRates[i]["provider"] = provider;
		parsedCarrierRates[i]["days"] = nDaysToDest;
		parsedCarrierRates[i]["cost"] = cost;
		parsedCarrierRates[i]["currency"] = currency;
		parsedCarrierRates[i]["duration_terms"] = duration_terms;
		//console.log(currentRate);

	}

	//console.log(parsedCarrierRates);

	populateShippingOptionsTable();

}


function populateShippingOptionsTable(){
	var shipment_options_table = $("#shipment_options_table");
	shipment_options_table.html("");

	var tableTemplateHTML = "<table class=\"table table-bordered table-hover\" id=\"shipment_options\">";
	tableTemplateHTML += "<thead>";
	tableTemplateHTML += "<th class=\"th_select\"> </th>";
	tableTemplateHTML += "<th> Provider </th>";
	tableTemplateHTML += "<th> Duration Terms </th>";
	tableTemplateHTML += "<th> # of Days </th>";
	tableTemplateHTML += "<th> Total Cost </th>";
	tableTemplateHTML += "</thead>";
	tableTemplateHTML += "<tbody>";

	for(var i=0;i<parsedCarrierRates.length;i++){
		tableTemplateHTML += "<tr>";
		tableTemplateHTML += "<td><label class=\"btn btn-default select_container\"><input type=\"checkbox\" data-optionID=\"" + String(i) + "\"class=\"selectTableItem btn-select-shipment-option\"></label></td>";
		tableTemplateHTML += "<td>" + parsedCarrierRates[i]["provider"] + "</td>";
		tableTemplateHTML += "<td>" + parsedCarrierRates[i]["duration_terms"] + "</td>";
		tableTemplateHTML += "<td>" + parsedCarrierRates[i]["days"] + "</td>";
		tableTemplateHTML += "<td>" + parsedCarrierRates[i]["cost"] + "&nbsp;" + parsedCarrierRates[i]["currency"] + "</td>";
		tableTemplateHTML += "</tr>";
	}


	//console.log(parcelData);

	tableTemplateHTML += "</tbody></table>";

	shipment_options_table.append(tableTemplateHTML);

	$(".btn-select-shipment-option").each(function(){
		var option_id = parseInt($(this).attr('data-optionID'));
		$(this).change({option_id: option_id}, selectShippingOption);
	});

}

function selectShippingOption(event){
	var option_id = event.data.option_id;
	var selectorString = '[data-optionID="' + String(option_id) + '"]';  
	var btn_selectedShippingOption = $(".btn-select-shipment-option" + selectorString);

	var isSelected = btn_selectedShippingOption.is(":checked");

	// deselect all the other shipping options 

	$(".btn-select-shipment-option").each(function(){
		$(this).prop('checked',false);
	});
	
	btn_selectedShippingOption.prop('checked', true);

	//console.log("Selected: " + option_id);

	var selected_shipping_method = $("#selected_shipping_method");

	selected_shipping_method.html("");

	shippingMethodHTML = "<div class=\"row\">";

	shippingMethodHTML += "<div class=\"col-xs-6 text-center\">";
	shippingMethodHTML += "Selected Provider:&nbsp;&nbsp;" + parsedCarrierRates[option_id]["provider"] + "<br>";
	shippingMethodHTML += "Days to delivery:&nbsp;&nbsp;" + parsedCarrierRates[option_id]["days"] + "<br>";
	shippingMethodHTML += "Total shipping cost:&nbsp;&nbsp;$" + parsedCarrierRates[option_id]["cost"] + "<br>";
	shippingMethodHTML += "</div>";

	shippingMethodHTML += "<div class=\"col-xs-6 text-center\">";
	shippingMethodHTML += "<button type=\"button\" class=\"btn btn-lg btn-success\" id=\"btn_generateShippingLabel\"> Create Shipping Label </button>";
	shippingMethodHTML += "</div></div>";

	selected_shipping_method.append(shippingMethodHTML);

	$("#btn_generateShippingLabel").unbind();
	$("#btn_generateShippingLabel").click({selected_option: option_id}, generateShippingLabel);
}



function updateItemFulfillmentState(){
	//console.log(fulfillmentData);

	orderFulfilled = true;

	$(".order-fulfillment-glyph").each(function(){
		var product_sku = $(this).attr('data-productSKU');
		var selectorString = '[data-productSKU="' + product_sku + '"]';
		var product_qty = parseInt($(".order-product-qty" + selectorString).val());

		// this item is not fulfilled, so it is clickable to allow adding to package
		if(fulfillmentData[product_sku] < product_qty || (!(product_sku in fulfillmentData))){
			$(this).html("<span class=\"glyph-fulfilled glyphicon red glyphicon-remove\"></span>");
				
				// on click enabled
				$(".order_product_fulfillment" + selectorString).click({product_sku: product_sku}, toggleProductSelection);
				orderFulfilled = false;		
		}

		// this item has been fulfilled
		else{
			$(this).html("<span class=\"glyph-fulfilled glyphicon green glyphicon-ok\"></span> &nbsp;<b>Shipped</b>");	

			// unbind any click events and reset the cursor to standard
			$(".order_product_fulfillment" + selectorString).css({
				'cursor':'initial',
				'opacity':'0.7'
			});
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

		// populate product table containers 
		populateProductTable("shipment_products_table_ship");
		populateProductTable("shipment_products_table_manual");

		populateShipmentDetailsTable();
		// load shipping address into modal
		modal_loadShippingAddressTo();



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
	btn_genShipmentObj.click({order_id: order_id}, createShipmentObject);

}




function range(start, end, inc){
	var a = [];
	for(var i=start;i<=end;i+=inc){
		a.push(i);
	}
	return a
}