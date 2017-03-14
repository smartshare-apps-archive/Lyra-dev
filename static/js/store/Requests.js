function addToCart(event){
	var productData = $("#selectedProduct").val();		// product data is passed in as the item SKU and quantity (e.g. "hat-xxl;2" )
	
	$.ajax({
	  method: "POST",
	  url: "/store/addToCart",
	  dataType: "json",
	  traditional:true,
	  data: { productData: JSON.stringify(productData) }
	})
	  .done(function(product_id) {
			getMessageHTML(productData);

			// toggle the color of the cart button to show that cart isn't empty (this change is maintained with session data passed to the nav bar render function)
			$("#cart_link").toggleClass("black", false);
			$("#cart_link").toggleClass("green", true);
	  });
}



function updateCartItem(productData){
	
	$.ajax({
	  method: "POST",
	  url: "/store/updateCartItem",
	  dataType: "json",
	  traditional:true,
	  data: { productData: JSON.stringify(productData) }
	})
	  .done(function(product_id) {
	  	window.location.reload();
	  });
}

function getMessageHTML(message){
	$.ajax({
	  method: "POST",
	  url: "/store/popupMessage",
	  dataType: "json",
	  traditional:true,
	  data: { message: JSON.stringify(message) }
	})
	  .done(function(messageHTML) {
			popup_Message(messageHTML);
	  });

}