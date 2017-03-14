// main product tab specific functions (the main product list)
// this file manages all the event bindings on that main product table, as well as loading data for list styles

var minimumScroll = 0;
var isPositionFixed = false;
var actionBar;
var ratio = 1.3;
var productData = {};
var currentSearchFilter = {"filter":"Title"};
var selectAll = true;

$(document).ready(function(){
		bindTableEvents();
		loadImageResources();
		setupActionBar();
		scaleTiles();

	$(".product_data").each(function(){
		var product_id = $(this).attr('id').split('_')[2];
		productData[product_id] = $(this).val();

		});
});



function bindTableEvents(){
	$(window).resize(scaleTiles);
	
	
	$(".product_container").each(function(){
		var productID = $(this).attr('id').split('_')[1];
		$(this).find(".product_link").attr("href","/control/products/"+productID);
		$(this).find(".btn_launch_editor").click({product_id: productID}, goToProductEditor)
		$(this).find(".selectProduct").change({product_id: productID}, selectProduct);
		
		$(this).mouseenter({product_id: productID}, showProductInfo);

		$(this).mouseleave({product_id: productID}, hideProductInfo);
		$(document).mouseleave({product_id: productID}, hideProductInfo);
	});



	

	$(".btn_bulk_edit_products").click({product_id_list: selectedProducts}, goToBulkProductEditor);
	$(".btn_bulk_publish_products").click({published:"true", product_id_list: selectedProducts}, bulkPublish);
	$(".btn_bulk_hide_products").click({published:"false", product_id_list: selectedProducts}, bulkPublish);
	$(".btn_bulk_delete_products").click({product_id_list: selectedProducts}, bulkDelete);
	$("#btn_addProduct").click(goToNewProductEditor);

	$("#search_filter").change(updateProductFilter);
	$("#product_search_input").keyup(filterProducts);

	$("#select_all_products").change(toggleAllProducts);
	
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


function scaleTiles(){
	
	$(".product_container").each(function(){
		var img_cont = $(this).find('.product_img_cont');
		//var buffer = (($(this).width()*ratio) - $(this).width()) * 2;
		
		$(this).height($(this).width()*ratio);

		img_cont.css('background-size', "100%");
		
	});

}


function goToProductEditor(event){
	window.location.href = "/control/products/"+event.data.product_id;
}


function goToNewProductEditor(event){
	window.location.href = "/control/products/addProduct";
}


function goToBulkProductEditor(event){
	var variantIdList = ""

	for (var key in selectedProducts) {
	    var product_id = selectedProducts[key];
	    variantIdList += (product_id + ",")
	}

	variantIdList = variantIdList.slice(0, -1);
	window.location.href = "/control/products/bulkEditor?ids="+variantIdList;
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
			$("#n_products_selected").html("<b>" + nProducts + "</b> product selected ");
		}
		else{
			$("#n_products_selected").html("<b>" + nProducts + "</b> products selected ");

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
		console.log("SELECTED: " + event.data.product_id);
		selectedProducts[event.data.product_id] = event.data.product_id;
	}
	else{
		delete selectedProducts[event.data.product_id]
	}

	var nProducts = Object.keys(selectedProducts).length;

	if (nProducts > 0){
		$("#product_action_bar").css("display","inline");
		
		if(nProducts == 1){
			$("#n_products_selected").html("<b>" + nProducts + "</b> product selected ");
		}
		else{
			$("#n_products_selected").html("<b>" + nProducts + "</b> products selected ");

		}

	}
	else if (nProducts == 0){
		$("#product_action_bar").css("display","none");
	}

}




function loadImageResources(){
	$(".product_container").each(function(){
		var product_id = $(this).attr('id').split('_')[1];
		var resource_uri = $("#thumbnail_uri_"+product_id).val();
		var bg_image = "url('" + resource_uri + "')";

		$(this).find('.product_img_cont').css('background-image',bg_image);
		
		console.log(resource_uri);
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