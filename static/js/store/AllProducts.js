$(document).ready(function(){
	bindElements();
	bindEvents();

	scaleTiles();
	loadProductThumbnails();
});


function bindElements(){

}

function bindEvents(){
	$(window).resize(scaleTiles);

	$(".product_tile").each(function(){
		var product_id = $(this).attr('id').split('_')[1];
		$(this).click({product_id: product_id}, go_Product);

	});

}

function go_Product(event){
	window.location.replace('/product/' + event.data.product_id);
}


function scaleTiles(){
	$(".product_tile").each(function(){
		$(this).height($(this).width());
	});

}


function loadProductThumbnails(){
	$(".product_thumbnail_src").each(function(){

		var product_id = $(this).attr('id').split('_')[1];
		var product_thumbnail_src = $(this).val();

		$("#product_" + product_id).css('background-image',"url('" + product_thumbnail_src + "')");


	})

}