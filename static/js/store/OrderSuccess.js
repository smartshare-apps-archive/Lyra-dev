$(document).ready(function(){
	loadProductThumbnails();

});


function loadProductThumbnails(){
	$(".product_thumbnail_src").each(function(){

		var product_id = $(this).attr('id').split('_')[1];
		var product_thumbnail_src = $(this).val();

		$("#product_" + product_id).css('background-image',"url('" + product_thumbnail_src + "')");

	});

}