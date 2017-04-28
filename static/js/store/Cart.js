var btn_goCheckout;

$(document).ready(function(){
	bindElements();
	bindEvents();

	
});


function bindElements(){
	btn_goCheckout = $("#btn_goCheckout");
}

function bindEvents(){
	if(btn_goCheckout){
		btn_goCheckout.click(go_Checkout);
	}

	$(".btn_updateQuantity").each(function(){
		$(this).click({target_item: $(this).attr('id').split('_')[2]}, updateItemQuantity);

	});

	
	$(".btn_removeFromCart").each(function(){
		$(this).click({target_item: $(this).attr('id').split('_')[2]}, deleteItemFromCart);

	});

	$(".selectQuantity").each(function(){
		var startingQuantity = $(this).parent().find(".currentItemQuantity").val();
		$(this).val(startingQuantity);
	});
	
}

function updateItemQuantity(event){
	if(event.data.target_item != null){
		var itemSKU = event.data.target_item;
		var newQuantity = $("#item_quantity_"+itemSKU).val();
		updateCartItem(itemSKU + ";" + newQuantity);
	}
}


function deleteItemFromCart(event){
	if(event.data.target_item != null){
		var itemSKU = event.data.target_item;
		var newQuantity = 0;
		updateCartItem(itemSKU + ";" + newQuantity);
	}	
}


function go_Product(event){
	window.location.replace('/product/' + event.data.product_id);
}


function go_Checkout(event){
	window.location.replace('/checkout');
}


