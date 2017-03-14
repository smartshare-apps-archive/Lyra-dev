// this file manages inventory list functions, similar to Main.js

var minimumScroll = 0;
var isPositionFixed = false;
var actionBar;
var btn_viewProducts;

var ratio = 1.3;
var productData = {};
var currentSearchFilter = {"filter":"Title"};
var selectAll = true;

$(document).ready(function(){
		bindElements();
		bindTableEvents();
		bindEvents();
		setupActionBar();
		scaleTiles();
		setupVariantTable();
		loadImageResources();
		
	$(".product_data").each(function(){
		var product_id = $(this).attr('id').split('_')[2];
		productData[product_id] = $(this).val();

		});
});


function bindElements(){
	btn_viewProducts = 	$("#btn_viewProducts");
	btn_bulkEditVariants = $(".btn_bulk_edit_variants");
	btn_bulkShowVariants = $(".btn_bulk_publish_variants");
	btn_bulkHideVariants = $(".btn_bulk_hide_variants");
	btn_bulkDeleteVariants = $(".btn_bulk_delete_variants");
}


function bindEvents(){
	btn_bulkEditVariants.click({product_id_list: selectedProducts}, goToBulkInventoryEditor);
	btn_bulkShowVariants.click({published:"true", product_id_list: selectedProducts}, bulkPublish);
	btn_bulkHideVariants.click({published:"false", product_id_list: selectedProducts}, bulkPublish);
	btn_bulkDeleteVariants.click({product_id_list: selectedProducts}, bulkDelete);
	btn_viewProducts.click(goToProductView);

	$(".btn_showVariants").each(function(){
		var productID = $(this).attr('id').split('_')[2];
		$(this).click({product_id:productID}, showProductVariants);
	});

	$(".btn_editVariant").each(function(){
		var variant_id = $(this).attr('id').split('_')[1];
		$(this).click({variant_id:variant_id}, goToProductInventoryEditor);
	});
}



function bindTableEvents(){
	$(window).resize(scaleTiles);
	
	$(".product_container").each(function(){
		if(!$(this).hasClass("variant")){
			var productID = $(this).attr('id').split('_')[1];
			$(this).find(".product_link").attr("href","/control/products/"+productID);
			$(this).find(".selectProduct").change({product_id: productID}, selectProduct);
			$(this).mouseenter({product_id: productID}, showProductInfo);
			$(this).mouseleave({product_id: productID}, hideProductInfo);
			$(document).mouseleave({product_id: productID}, hideProductInfo);
			}
		});

	$("#search_filter").change(updateProductFilter);
	$("#product_search_input").keyup(filterProducts);

	$("#select_all_products").change(toggleAllProducts);
}


function setupVariantTable(){
	$(".product_container.variant").each(function(){
		$(this).hide();
	});

}


function setupActionBar(){
	actionBar = $("#product_action_bar");

	$(window).scroll(function(){
		var top = $(this).scrollTop();

		if(top > minimumScroll && isPositionFixed == false){
		isPositionFixed = true;
		actionBar.css("position","fixed");
		actionBar.css("top","0px");
		}
		else if(top < minimumScroll && isPositionFixed == true){
		isPositionFixed = false;
		actionBar.css("position","absolute");
		actionBar.css("top",minimumScroll+"px");
		}

	});

}


function goToProductView(event){
	window.location.replace("/control/products/");
}


function goToProductInventoryEditor(event){
	window.location.replace("/control/products/inventory/"+event.data.variant_id);
}



function goToBulkInventoryEditor(event){
	var variantIdList = ""

	for (var key in selectedProducts) {
	    var product_id = selectedProducts[key];
	    variantIdList += (product_id + ",")
	}

	variantIdList = variantIdList.slice(0, -1);
	window.location.replace("/control/products/inventory/bulkEditor?ids="+variantIdList);
}

function hideProductInfo(event){
	var imageDiv = $(event.target).closest('.product_container').find('.product_img_cont');
	var targetProductContainer = $("#default_content_" + event.data.product_id);
	var targetProductInfoContainer = $("#info_content_" + event.data.product_id);

	targetContainers = [targetProductContainer, targetProductInfoContainer];
	

		targetContainers[0].show();
		targetContainers[1].hide();
		
		imageDiv.stop().animate({ "height":"100%",
						  "width":"100%",
						  "left":"0%"

						}, 200, function(){
							
						});
}



function showProductInfo(event){
	var imageDiv = $(event.target).closest('.product_container').find('.product_img_cont');
	var targetProductContainer = $("#default_content_" + event.data.product_id);
	var targetProductInfoContainer = $("#info_content_" + event.data.product_id);

	targetContainers = [targetProductContainer, targetProductInfoContainer];
	
	imageDiv.stop().animate({ "height":"60%",
				  "width":"60%",
				  "left":"20%"

				}, 200, function(){
					targetContainers[0].hide();
					targetContainers[1].show();
				});
}


function showProductVariants(event){
	var product_id = event.data.product_id;

	var showHTML = "Variants &nbsp;&nbsp;<span class=\"glyphicon glyphicon-arrow-right\"> </span>";
	var hideHTML = "Hide &nbsp;&nbsp;<span class=\"glyphicon glyphicon-arrow-left\"> </span>";
	
	var isVisible = $("#product_variants_"+product_id).is(':visible');

	if(isVisible){
		$("#show_product_" + product_id).find('.btn_txt').html(showHTML);
	}
	else{
		$("#show_product_" + product_id).find('.btn_txt').html(hideHTML);
	}
	

	$("#product_variants_"+product_id).stop().animate({width:'toggle'},100);

}



// toggles all products either selected or deselected
function toggleAllProducts(){
	var productIDList = $("#productIDList").val().split(',');
	productIDList.pop();
	

	for(var i=0;i<productIDList.length;i++){
		var product_id = productIDList[i];

		if(selectAll == true){
			selectedProducts[product_id] = product_id;
		}
		else{

			if (product_id in selectedProducts){
				delete selectedProducts[product_id];
			}
			
		}
		
	}

	if(selectAll){
		$(".selectProduct").each(function(){
			$(this).prop('checked',true);
			
		});
	}
	else{
		$(".selectProduct").each(function(){
			$(this).prop('checked',false);
		});
	}

	var nProducts = Object.keys(selectedProducts).length;

	if (nProducts > 0){
		$("#product_action_bar").css("display","inline");
		
		if(nProducts == 1){
			$("#n_products_selected").html("<b>" + nProducts + "</b> product selected");
		}
		else{
			$("#n_products_selected").html("<b>" + nProducts + "</b> products selected");

		}

	}
	else if (nProducts == 0){
		$("#product_action_bar").css("display","none");
	}

	selectAll = !selectAll;
}



function selectProduct(event){
	event.stopPropagation();
	
	selectedProduct = $("#chk_" + event.data.product_id);

	if(selectedProduct.is(':checked')){
		selectedProducts[event.data.product_id] = event.data.product_id;
	}
	else{
		delete selectedProducts[event.data.product_id]
	}

	var nProducts = Object.keys(selectedProducts).length;

	if (nProducts > 0){
		$("#product_action_bar").css("display","inline");
		
		if(nProducts == 1){
			$("#n_products_selected").html("<b>" + nProducts + "</b> product selected");
		}
		else{
			$("#n_products_selected").html("<b>" + nProducts + "</b> products selected");

		}

	}
	else if (nProducts == 0){
		$("#product_action_bar").css("display","none");

	}

}



function scaleTiles(){
	$(".product_container").each(function(){

		var img_cont = $(this).find('.product_img_cont');
		//var buffer = (($(this).width()*ratio) - $(this).width()) * 2;
		$(this).height($(this).width()*ratio);

		img_cont.css('background-size', "100%");
		
	});

}

function loadImageResources(){
	$(".product_container").each(function(){
		if(!$(this).hasClass("variant")){

			var product_id = $(this).attr('id').split('_')[1];
			var resource_uri = $("#thumbnail_uri_"+product_id).val();
			var bg_image = "url('" + resource_uri + "')";

			$(this).find('.product_img_cont').css('background-image',bg_image);
			
			console.log(resource_uri);
		}
	});

}



// basic title search functions below

function updateProductFilter(event){
	currentSearchFilter = {"filter": $(event.target).val()};
	filterProducts();
}

function filterProducts(event){
	var currentInput = {"input": $("#product_search_input").val()};
	req_filterProducts(currentInput, currentSearchFilter,productData);
}


function filterResults(matchIDList){
	//console.log(matchIDList);

	$(".product_container").each(function(){
		var product_id = $(this).attr('id').split('_')[1];
		var inMatchList = matchIDList.indexOf(product_id);
		
			if(inMatchList < 0){
				$(this).hide();
			}
			else{
				$(this).show();
			}
		

	});


}