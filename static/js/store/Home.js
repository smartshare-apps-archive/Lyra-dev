var tile_positions = {
	"featured_products": [0],
	"recommended_products": [0,1,2,3,4,5],

};

var current_index = {
	"popular_products":0,
	"recommended_products":0,
	"featured_products":0
};


$(document).ready(function(){
	bindElements();
	bindEvents();
	scaleTiles();

	//refreshContent("popular_products", 0);
	refreshContent("recommended_products", 0);
	//refreshContent("featured_products", 0);


});


function bindEvents(){

	$(window).resize(scaleTiles);
}



function scaleTiles(){
	$(".home_product_tile").each(function(){
		$(this).height($(this).width());
	});
}

function popup_Menu(event){
	var nav_link = $(event.target);
	var offset = nav_link.offset();

	var menuID = event.data.menuID;

	var top = offset.top;
	var left = offset.left;

	$(menuID).css('display',"inline");
	$(menuID).css('top',top + "px");
	$(menuID).css('left',left + "px");

	$(menuID).mouseleave({menuID: menuID}, close_Menu);
}


function close_Menu(event){
	var menuID = event.data.menuID
	$(menuID).css('display',"none");
}



function scrollLeft(event){
		var productRowID = event.data.productRowID;
		var firstTile = ".tile_" + tile_positions[productRowID][0];
		var lastTile = ".tile_" + tile_positions[productRowID][tile_positions[productRowID].length-1];

		if(firstTile == lastTile){
			$("#row_"+productRowID).find(firstTile).hide("slide",{ direction: "left" }, 300, function(){
				refreshContent(productRowID, current_index[productRowID]);
				$(this).show("slide", { direction: "right" }, 300);
			});

			current_index[productRowID] -= 1;
		}
		else{

		$("#row_"+productRowID).find(firstTile).insertBefore($("#row_"+productRowID).find(lastTile));

		for(var index=(tile_positions[productRowID].length-1);index>=0;index--){
			var newIndex = index-1;
			if(newIndex < 0){
				var first_tile = tile_positions[productRowID][index];
				tile_positions[productRowID].shift();	
				tile_positions[productRowID].push(first_tile);
			}
		}
		current_index[productRowID] -= 1;
		refreshContent(productRowID, current_index[productRowID]);
	}
}


function scrollRight(event){
		var productRowID = event.data.productRowID;
		var firstTile = ".tile_" + tile_positions[productRowID][0];
		var lastTile = ".tile_" + tile_positions[productRowID][tile_positions[productRowID].length-1];


		if(firstTile == lastTile){
			$("#row_"+productRowID).find(firstTile).hide("slide",{ direction: "right" }, 300, function(){
				refreshContent(productRowID, current_index[productRowID]);
				$(this).show("slide", { direction: "left" }, 300);
			});

			current_index[productRowID] += 1;
		}
		else{
			$("#row_"+productRowID).find(lastTile).insertBefore($("#row_"+productRowID).find(firstTile));
		
		

		for(var index=0;index<=(tile_positions[productRowID].length-1);index++){
			var newIndex = index+1;
			if(newIndex > tile_positions[productRowID].length-1){
				var last_tile = tile_positions[productRowID][index];
				tile_positions[productRowID].pop();	
				tile_positions[productRowID].unshift(last_tile);
			}
		}

			current_index[productRowID] += 1;
			refreshContent(productRowID, current_index[productRowID]);
	}
}



function refreshContent(productRowID, current_index){
	n_products = $(".product_data_container#"+productRowID+" .n_products").val();

	if (current_index == 0){
		$(".btn_scrollLeft#sl_"+productRowID).unbind("click");
		$(".btn_scrollLeft#sl_"+productRowID).toggleClass("disabled", true);
	}
	else {
		$(".btn_scrollLeft#sl_"+productRowID).unbind("click");
		$(".btn_scrollLeft#sl_"+productRowID).click({productRowID:productRowID}, scrollLeft);
		$(".btn_scrollLeft#sl_"+productRowID).toggleClass("disabled", false);
	}

	if(current_index == (n_products - tile_positions[productRowID].length)){
		$(".btn_scrollRight#sr_"+productRowID).unbind("click");
		$(".btn_scrollRight#sr_"+productRowID).toggleClass("disabled", true);

	}
	else{
		$(".btn_scrollRight#sr_"+productRowID).unbind("click");
		$(".btn_scrollRight#sr_"+productRowID).click({productRowID:productRowID}, scrollRight);
		$(".btn_scrollRight#sr_"+productRowID).toggleClass("disabled", false);
	}


	product_metadata = [];

	for(var i=0;i<(tile_positions[productRowID].length);i++){
		var cdata = grabMetaData(productRowID, current_index+i);
		product_metadata.push(cdata);
	}

	$("#row_"+productRowID).find(".product_cont").each(function(index){
		$(this).css('background-image',"url('" + product_metadata[index]["ImageSrc"] + "')");
		$(this).find(".product_title").html(product_metadata[index]["Title"]);
		
		$(this).unbind();
		$(this).click({product_id:product_metadata[index]["product_id"]}, goto_product);
	});
}


function grabMetaData(productRowID, current_index){
	var metadata_container = $("#"+productRowID).find(".product_metadata").eq(current_index);

	var product_id = metadata_container.find(".product_id").val();
	var product_title = metadata_container.find(".product_title").val();
	var product_price = metadata_container.find(".product_price").val();
	var product_thumbnail_src = metadata_container.find(".product_thumbnail_src").val();

	var metadata = {"product_id":product_id, "Title":product_title, "Price":product_price, "ImageSrc":product_thumbnail_src}
	return metadata;
}


function goto_product(event){
	var product_id = event.data.product_id;
	window.location.href = "/product/"+product_id ;

}


function bindElements(){
	n_products = parseInt($("#n_products").val());

}



function loadProductThumbnails(){
	$(".product_thumbnail_src").each(function(){

		var product_id = $(this).attr('id').split('_')[1];
		var product_thumbnail_src = $(this).val();

		$("#product_" + product_id).css('background-image',"url('" + product_thumbnail_src + "')");


	})

}
