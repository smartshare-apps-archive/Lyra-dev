// buttons
var btn_addToCart;
var select_productQty;

//filtering selection stuff
var available_variants = {};
var option_names = [];
var currentOptions = {};

$(document).ready(function(){
	bindElements();
	bindEvents();
	loadProductImages();
	scaleTiles();
	filterVariants();
	formatVariantChoice();
});


function loadProductImages(){
	var main_product_img_src = $(".main_product_img_src").val();
	console.log(main_product_img_src);
	$("#main_product_img").css('background-image',"url('" + main_product_img_src + "')");

	$(".variant_product_img").each(function(){
		var img_src = $(this).find('.variant_product_img_src').val();
			
			if(img_src != ""){
				$(this).css('background-image',"url('" + img_src + "')");
			}
			else{
				$(this).remove();
				}
	});
}


function bindElements(){
	btn_addToCart = $("#btn_addToCart");
	select_productQty = $("#cart_quantity");

}


function bindEvents(){
	$(window).resize(scaleTiles);
	select_productQty.change(updateQuantity);

	
	$(".variant_choice").each(function(){
		$(this).on('change', updateChoices);
		var optionName = $(this).attr('id').split('_')[1];
		option_names.push(optionName);
	});
	
}


function filterVariants(){
	$(".variant_choice").each(function(){
		var variantOption = $(this).attr('id').split('_')[1];
		available_variants[variantOption] = {};
		
		$("option", this).each(function(){
			var value = $(this).val().trim();
			available_variants[variantOption][value] = [];
		});
	});

	//console.log(available_variants);

	$("#available_variants > option").each(function(){
		var variant = JSON.parse(replaceAll($(this).text(),"'","\""));
		//console.log(variant);
		for (var option in variant){
			if(available_variants[option][variant[option]]){
				available_variants[option][variant[option]].push(variant);
			}
			else{
				available_variants[option][variant[option]] = [variant];
			}
		}
	});

	// console.log(available_variants);
}


function updateChoices(event){
	var optionName = $(event.target).attr('id').split('_')[1];
	var optionValue = $(event.target).val().trim();

	$(":selected",$(event.target)).text(optionValue);
	var variants = available_variants[optionName][optionValue];


	currentOptions = {}

	for(var i=0; i<option_names.length;i++){
		currentOptions[option_names[i]] = [];
	}

	for(var i=0;i<variants.length;i++){
		$(".variant_choice").each(function(){
			var option = $(this).attr('id').split('_')[1];
			if (option != optionName) {
				if(i==0){
					currentOptions[option] = [ variants[i][option] ]
					
				}
				else{
					currentOptions[option].push(variants[i][option]);
				}
			}

		});
	}


	$(".variant_choice").each(function(){
		var option = $(this).attr('id').split('_')[1];
		if(option != optionName){
			
			$(this).find('option').each(function(){
	
				if(currentOptions[option].indexOf($(this).val().trim()) >= 0){
					$(this).text($(this).val().trim());
				}
				
				else{
					$(this).text($(this).val().trim() + " (unavailable)");
				}
			})

		}
		
	});

	formatVariantChoice();
}

function formatVariantChoice(){
	var validChoice = false;
	var variantChoice = "";

	if($("#has_variants").val() == "false"){
		validChoice = true;
		btn_addToCart.toggleClass("disabled",false);
		btn_addToCart.click(addToCart);
		return;
	}

	


	$(".variant_choice").each(function(){
		var optionName = $(this).attr('id').split('_')[1];
		variantChoice += optionName + ":" + $(":selected", this).val() + ";";
	});
	variantChoice = variantChoice.slice(0,-1);
	
	$("#available_variant_sku > option").each(function(){
		if (variantChoice == $(this).text()){
			var variantSKU = $(this).val();
			var currentQuantity = $("#cart_quantity").val();
			$("#selectedProduct").val(variantSKU + ";" + currentQuantity);
			validChoice = true;
		}
	})

	if (validChoice){
		btn_addToCart.toggleClass("disabled",false);
		btn_addToCart.click(addToCart);
	}
	else{
		btn_addToCart.unbind("click");
		btn_addToCart.toggleClass("disabled",true);
	}

}

function updateQuantity(event){
	var product_sku = $("#selectedProduct").val().split(';')[0];
	var quantity = $(event.target).val();

	var productData = product_sku + ";" + quantity;

	$("#selectedProduct").val(productData);
}


function scaleTiles(){
	$("#main_product_img").height($("#main_product_img").width())
}
