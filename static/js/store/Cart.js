var btn_goCheckout;

$(document).ready(function(){
	bindElements();
	bindEvents();

	
	loadProductThumbnails();
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


function loadProductThumbnails(){
	$(".product_thumbnail_src").each(function(){

		var product_id = $(this).attr('id').split('_')[1];
		var product_thumbnail_src = $(this).val();

		$("#product_" + product_id).css('background-image',"url('" + product_thumbnail_src + "')");

		console.log(product_id + ":" + product_thumbnail_src);


	})

}