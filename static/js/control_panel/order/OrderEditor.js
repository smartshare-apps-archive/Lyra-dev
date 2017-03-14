var btn_shipOrder;
var order_id;



$(document).ready(function(){
	order_id = $("#order_id").val();

	loadProductThumbnails();
	bindElements();
	bindEvents();
});


function bindElements(){
	btn_shipOrder = $("#btn_shipOrder");

}


function bindEvents(){
	btn_shipOrder.click(go_fulfillOrder);


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

