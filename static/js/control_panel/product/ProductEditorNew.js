var productData;

// page specific button handles
var btn_saveProduct;
var btn_confirmProductChanges;

$(document).ready(function(){

	productData = {};
	bindElements();
	setupDescriptionEditor();	// bind events to summernote wysiwyg editor and fill it with initial description html
	bindTableEvents();			// bind events to the product variants table
	bindEvents();
	updateProductData();
	loadImageResources();

});


function bindElements(){
	btn_saveProduct = $("#btn_saveProduct")
	btn_confirmProductChanges = $("#btn_confirmProductChanges")

}


function bindEvents(){

	$("#input_product_title").change(function(){
		$("#currentProductTitle").html($("#input_product_title").val())
	})


	$('#product_description_editor').on('summernote.change', function(e) {
 		$("#currentProductDescription").html($('#product_description_editor').summernote('code'));
		});

	// button events
	btn_confirmProductChanges.click({productData: productData}, saveNewProduct);
	btn_saveProduct.click(updateProductData);
}


function setupDescriptionEditor(){
	$('#product_description_editor').summernote({
		  height: 200,                 // set editor height
		  minHeight: 200,             // set minimum height of editor
		  maxHeight: 250,             // set maximum height of editor
		  focus: false                  // set focus to editable area after initializing summernote
		});

	product_description_html = $("#product_description_html").val();
	$('#currentProductDescription').html(product_description_html);

}




function bindTableEvents(){
//placeholder
}


function loadImageResources(){
	$(".image_resource").each(function(){
		var resource_id = $(this).attr('id').split('_')[1];
		var resource_uri = $("#resource_uri_"+resource_id).val();
		var bg_image = "url('" + resource_uri + "')";
		$(this).css('background-image',bg_image);
		
		console.log(resource_uri);
	});

}


function updateProductData(event = null){
	productData["BodyHTML"] = $('#currentProductDescription').html();
	productData["Title"] = $('#currentProductTitle').html();
	productData["VariantTypes"] = "";
	productData["ImageSrc"] = ""


	console.log(productData);
}




function goToProductInventoryEditor(event){
	window.location.replace("/control/products/inventory/"+event.data.product_id);
}
