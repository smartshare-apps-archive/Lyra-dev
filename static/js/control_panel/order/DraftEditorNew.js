// btn bindings
var btn_previous;
var btn_next;
var btn_shipOrder;
var btn_addToOrder;
var btn_deleteFromOrder;

var productData = {};
var currentSearchFilter = {"filter":"Title"};

var order_id;

var table_order_products;
var tbody_order_products;
var tbody_product_results;

var orderProducts = {};

var current_step = "order_details";
var draft_steps = ["order_details", "customer_details", "payment_details"];


var shippingIsBilling = true;


$(document).ready(function(){
	order_id = $("#order_id").val();

	loadProductThumbnails();
	bindElements();
	bindEvents();
	showStep();

});


function bindElements(){
	btn_shipOrder = $("#btn_shipOrder");
	btn_addToOrder = $("#btn_addToOrder");
	btn_deleteFromOrder = $("#btn_deleteFromOrder");
	btn_previous = $("#btn_previous");
	btn_next = $("#btn_next");

	$(".product_data").each(function(){
		var product_id = $(this).attr('id').split('_')[2];
		productData[product_id] = $(this).val();

	});

	table_order_products = $("#table_order_products");
	tbody_order_products = $("#tbody_order_products");
	tbody_product_results = $("#tbody_product_results");
}



function bindEvents(){
	btn_shipOrder.click(go_fulfillOrder);

	$("#search_filter").change(updateProductFilter);
	$("#product_search_input").keyup(filterProducts);


	$(".selectTableItem").each(function(){
		var product_id = $(this).attr('data-productID');
		$(this).click({product_id: product_id}, selectProduct)
	});

	$(".select_product_qty").each(function(){
		var product_id = $(this).attr('data-productID');
		$(this).change({product_id: product_id}, updateItemQuantity);
	});


	btn_addToOrder.click(addToOrder);
	btn_deleteFromOrder.click(deleteFromOrder);

	btn_previous.click(previousStep);
	btn_next.click(nextStep);	
}


function previousStep(event){
	var currentIndex = draft_steps.indexOf(current_step);
	
	if(currentIndex != 0){
		currentIndex -= 1;
		current_step = draft_steps[currentIndex];
	}

	showStep();
}


function nextStep(event){
	var currentIndex = draft_steps.indexOf(current_step);

	if(currentIndex != (draft_steps.length-1)){
		currentIndex += 1;
		current_step = draft_steps[currentIndex];
	}

	showStep();
}


function showStep(){
	$(".draft-step").each(function(){
		if($(this).is(":visible")){
			$(this).hide();
		}
	});

	if(current_step == "order_details"){
		$("#draft_step_1").show();
		btn_next.toggleClass("disabled",false);
		btn_previous.toggleClass("disabled",true);
	}
	else if(current_step == "customer_details"){
		$("#draft_step_2").show();
		btn_next.toggleClass("disabled",false);
		btn_previous.toggleClass("disabled",false);
	}
	else if(current_step == "payment_details"){
		$("#draft_step_3").show();
		btn_next.toggleClass("disabled",true);
		btn_previous.toggleClass("disabled",false);
	}

}



function selectProduct(event){
	var product_id = event.data.product_id;
	if(product_id in selectedProducts){
		delete selectedProducts[product_id];
	}
	else{
		selectedProducts[product_id] = product_id;
	}
	var nProducts = Object.keys(selectedProducts).length;

}


function addToOrder(event){

	for(key in selectedProducts){
		var product_id = key;
		var selectorString = '[data-productID="' + product_id + '"]';
		var currentProduct = $(".product_row" + selectorString);
		var quantity = $(".select_product_qty" + selectorString).val();


		if (!(product_id in orderProducts)){
			var currentItemCheckbox = currentProduct.find(".selectTableItem");
			tbody_order_products.append(currentProduct);
			orderProducts[product_id] = quantity;
		}
	}

	refreshOrderData();
	$("#product_search_input").val("");
	filterProducts();
}



function deleteFromOrder(event){
	for(key in selectedProducts){
		var product_id = key;
		var selectorString = '[data-productID="' + product_id + '"]';
		var currentProduct = $(".product_row" + selectorString);
		var quantity = $(".select_product_qty" + selectorString).val();

		if (product_id in orderProducts){
				var currentItemCheckbox = currentProduct.find(".selectTableItem");
				tbody_product_results.append(currentProduct);
				delete orderProducts[product_id];
		}

	}

	refreshOrderData();
}


function refreshOrderData(){
	var nOrderProducts = Object.keys(orderProducts).length;
	
	if(nOrderProducts >= 1){
		$("#no_orders").hide();
		$("#btn_deleteFromOrder").show();

	}
	else{
		$("#no_orders").show();
		$("#btn_deleteFromOrder").hide();
	}

	var checkboxObjects = $(".selectTableItem");

	// reset checkboxes to unchecked state so events line up
	checkboxObjects.each(function(){
		$(this).prop("checked", false);
	});	

	// reset the selected products literal
	selectedProducts = {};
}



// updates the product quantity order data object if it's been added to the order already
function updateItemQuantity(event){
	var product_id = event.data.product_id;
	if(product_id in orderProducts){
		var quantity = $(this).val();
		orderProducts[product_id] = quantity;
	}
	console.log(orderProducts);
}



function loadProductThumbnails(){
	$(".thumbnail_product_40").each(function(){
		var currentImageURL = $(this).find('.product_img_src').val();
		$(this).css('background-image',"url('"+currentImageURL+"')");
	});

}


function go_fulfillOrder(event){
	window.location.replace("/control/orders/fulfill/"+order_id);
}



// some basic regex search functions, these are really placeholders till i think of something better (they do work though)
function updateProductFilter(event){
	currentSearchFilter = {"filter": $(event.target).val()};
	filterProducts();
}


function filterProducts(event){
	var currentInput = {"input": $("#product_search_input").val()};
	req_searchProducts(currentInput, currentSearchFilter,productData);
}


function filterResults(matchIDList){
	console.log(matchIDList);

	$(".product_row").each(function(){
		var product_id = $(this).attr('data-productID');
		var inMatchList = matchIDList.indexOf(product_id);
		
		if(inMatchList < 0){
			$(this).hide();
		}
		else{
			$(this).show();
		}

	});


}




function toggleShippingAddress(event){
	shipping_info_container.slideToggle();

	if(btn_chkShippingAddress.is(":checked")){
		shippingIsBilling = true;

		var step_valid = validateCheckoutStep(currentCheckoutStep);

		$(".customer_info_input").each(function(){
			var targetField = $(this).find('input');
			var targetFieldID = targetField.attr('id').split('_')[1];
			var currentFieldValue =  targetField.val();

			//replace the content in the shipping container to match the billing container, if "Ship to this address" is selected
			if(targetFieldID.indexOf("Billing") >= 0){
				var el = targetFieldID.replace("Billing","Shipping");

				//$("#customer_"+el).val(currentFieldValue);
				//validateFieldContent(el, currentFieldValue);
			}

		});

	}
	// revalidate the step assuming that shipping info isn't that same as billing info
	else{
		shippingIsBilling = false;
		//var step_valid = validateCheckoutStep(currentCheckoutStep);
	}
}