function saveNewProduct(event){
	var productData = {};
	productData["Title"] = $("#new_product_title").val();
	
	if (productData["Title"] == ""){
		return false;
	}

	$.ajax({
	  method: "POST",
	  url: "/actions/addProduct",
	  dataType: "json",
	  traditional:true,
	  data: { productData: JSON.stringify(productData) }
	})
	  .done(function(product_id) {
			window.location.replace("/control/products/"+product_id);
	  });
}


function saveNewCollection(){
	var collectionData = {};
	collectionData["Title"] = $("#new_collection_title").val();
	
	if (collectionData["Title"] == ""){
		return false;
	}

	$.ajax({
	  method: "POST",
	  url: "/actions/addCollection",
	  dataType: "json",
	  traditional:true,
	  data: { collectionData: JSON.stringify(collectionData) }
	})
	  .done(function(collection_id) {
			window.location.replace("/control/products/collections/"+collection_id);
	  });
}





// updates a products inventory quantity from the quick edit modal
function updateProductInventory(product_id, inventory_qty){
	$.ajax({
	  method: "POST",
	  url: "/actions/updateProductInventory",
	  dataType: "json",
	  traditional:true,
	  data: { product_id: JSON.stringify(product_id), inventory_qty: JSON.stringify(inventory_qty)}
	})
	  .done(function(product_id) {
			var selectorString = '[data-productID="' + product_id + '"]'; 
			var label_inventory = $(".info_product_inventory" + selectorString);
			label_inventory.html(inventory_qty);

			productInventory[String(product_id)] = inventory_qty;
	  });
}




function saveNewProductVariant(variantData, product_id){
	variantData = JSON.stringify(variantData);
	product_id = JSON.stringify(product_id);

	$.ajax({
	  method: "POST",
	  url: "/actions/addProductVariant",
	  dataType: "json",
	  traditional:true,
	  data: { product_id: product_id, variantData: variantData }
	})
	  .done(function(product_id) {
			window.location.replace("/control/products/"+product_id);
	  });
}



function saveVariantTypes(event){
	variantTypes = JSON.stringify(event.data.variantTypes)
	product_id = JSON.stringify(event.data.product_id)
	stripe_id = JSON.stringify(event.data.stripe_id)

	$.ajax({
	  method: "POST",
	  url: "/actions/updateVariantTypes",
	  dataType: "json",
	  traditional:true,
	  data: { product_id: product_id, stripe_id: stripe_id, variantTypes: variantTypes }
	})
	  .done(function(product_id) {
			window.location.replace("/control/products/"+product_id);
	  });
}



function saveProductChanges(event){
	product_data = JSON.stringify(event.data.product_data);
	console.log(product_data);
	$.ajax({
	  method: "POST",
	  url: "/actions/updateProductData",
	  dataType: "json",
	  data: { product_data:product_data },
	  traditional:true
	})
	  .done(function( msg ) {
		location.reload();
	  });
}



function saveProductTags(event){
	var product_id = JSON.stringify(event.data.product_id);
	var product_tags = JSON.stringify($("#currentProductTags").val());
	
	$.ajax({
		method: "POST",
		url: "/actions/updateProductTags",
		dataType: "json",
		data: {product_id: product_id, product_tags: product_tags},
		traditional: true
	})
	.done(function(msg) {
		location.reload();

		});
	
}
 
// updates global product type categories
function saveProductTypes(event){
	var product_types = JSON.stringify($("#currentProductTypes").val());
	
	$.ajax({
		method: "POST",
		url: "/actions/updateProductTypes",
		dataType: "json",
		data: {product_types: product_types},
		traditional: true
	})
	.done(function(msg) {
		location.reload();
	});

}


// updates global product vendor list
function saveProductVendors(){

	$.ajax({
		method: "POST",
		url: "/actions/updateProductVendors",
		dataType: "json",
		data: {product_vendors: JSON.stringify(vendorData)},
		traditional: true
	})
	.done(function(msg) {
		location.reload();
	});

}



//  request action for deleting a single product 
function deleteProduct(event){
	product_id = event.data.product_id;

	$.ajax({
	  method: "POST",
	  url: "/actions/deleteProduct",
	  data: { product_id: product_id}
	})
	  .done(function(msg) {
			window.location.replace("/control/products/");
	  });
}


function deleteCollection(){
	$.ajax({
	  method: "POST",
	  url: "/actions/deleteCollection",
	  data: { collection_id: collection_id}
	})
	  .done(function(msg) {
			window.location.replace("/control/products/collections");
	  });
}




function deleteVariant(event){
	variant_id = event.data.variant_id;

	$.ajax({
	  method: "POST",
	  url: "/actions/deleteVariant",
	  data: { variant_id: variant_id }
	})
	  .done(function(msg) {
			window.location.replace("/control/products/inventory/");
	  });
}



function saveProductInventoryChanges(event){
	var variantData = event.data.variant_data;
	console.log(variantData);
	$.ajax({
	  method: "POST",
	  url: "/actions/updateVariantData",
	  dataType: "json",
	  data: { variant_data: JSON.stringify(variantData) },
	  traditional:true
	})
	  .done(function( msg ) {
		location.reload();
	});
}



function saveCollectionChanges(){

	$.ajax({
	  method: "POST",
	  url: "/actions/updateCollectionData",
	  dataType: "json",
	  data: { collection_data: JSON.stringify(collectionData) },
	  traditional:true
	})
	  .done(function( msg ) {
		location.reload();
	  });
}


function applyCollectionConditions(){
	//console.log(collectionConditions);
	
	$.ajax({
	  method: "POST",
	  url: "/actions/getCollectionProducts",
	  dataType: "json",
	  data: { collection_conditions: JSON.stringify(collectionConditions), collection_policy: JSON.stringify(collectionData["Strict"]) },
	  traditional:true
	})
	  .done(function( products ) {

		if(products){
			populateProductTable(products);
		}
		else{	
			table_collectionProducts.hide();
			message_noProductsInCollection.show();

			table_collectionProducts_body.html("");
		}

	  });

}



function updateBulkProductEditorFields(selectedFields){
	selectedFields = JSON.stringify(selectedFields)

	$.ajax({
	  method: "POST",
	  url: "/actions/updateBulkProductEditorFields",
	  dataType: "json",
	  data: { selectedFields:selectedFields },
	  traditional: true
	})
	  .done(function(msg) {
	  	location.reload();
	  });
	
}



function updateBulkInventoryEditorFields(selectedFields){
	selectedFields = JSON.stringify(selectedFields)
	console.log(selectedFields);
	
	$.ajax({
	  method: "POST",
	  url: "/actions/updateBulkInventoryEditorFields",
	  dataType: "json",
	  data: { selectedFields:selectedFields },
	  traditional: true
	})
	  .done(function(msg) {
	  	location.reload();
	  });
	

}


function updateBulkCollectionEditorFields(selectedFields){
	selectedFields = JSON.stringify(selectedFields)

	$.ajax({
	  method: "POST",
	  url: "/actions/updateBulkCollectionEditorFields",
	  dataType: "json",
	  data: { selectedFields:selectedFields },
	  traditional: true
	})
	  .done(function(msg) {
	  	location.reload();
	  });
	
}



// bulk functions


function bulkUpdateProducts(event){
	productData = JSON.stringify(event.data.productData);
	variantData = JSON.stringify(event.data.variantData);

	$.ajax({
	  method: "POST",
	  url: "/actions/bulkUpdateProducts",
	  dataType: "json",
	  data: { productData:productData, variantData: variantData},
	  traditional: true
	})
	  .done(function(msg) {
	  	location.reload();
	  });
	
}


function bulkUpdateCollections(event){
	collectionData = JSON.stringify(event.data.collectionData)
	
	$.ajax({
	  method: "POST",
	  url: "/actions/bulkUpdateCollections",
	  dataType: "json",
	  data: { collectionData:collectionData },
	  traditional: true
	})
	  .done(function(msg) {
	  	location.reload();
	  });
	
}



function bulkPublish(event){
	product_id_dict = event.data.product_id_list
	product_id_list = []

	published = event.data.published

	for (var key in product_id_dict) {
	    var product_id = product_id_dict[key];
	    product_id_list.push(product_id);
	}


	$.ajax({
	  method: "POST",
	  url: "/actions/bulkPublish",
	  dataType: "json",
	  data: { published: published, product_id_list: JSON.stringify(product_id_list) },
	  traditional: true
	})
	  .done(function( msg ) {
		location.reload();
	  });
	 
}




function bulkDelete(event){
	product_id_dict = event.data.product_id_list
	product_id_list = []

	for (var key in product_id_dict) {
	    var product_id = product_id_dict[key];
	    product_id_list.push(product_id);
	}

	$.ajax({
	  method: "POST",
	  url: "/actions/bulkDelete",
	  dataType: "json",
	  data: { product_id_list: JSON.stringify(product_id_list) },
	  traditional: true
	})
	  .done(function( msg ) {
	  	location.reload();
	  });
	 
}



function deleteProductResource(product_id, resource_id, resource_type){
	var product_id = JSON.stringify(product_id);
	var resource_id = JSON.stringify(resource_id);
	var resource_type  = JSON.stringify(resource_type);
	$.ajax({
		method: "POST",
		url: "/actions/deleteProductResource",
		dataType: "json",
		data: {product_id: product_id, resource_id: resource_id, resource_type: resource_type},
		traditional: true
	})
	.done(function(msg) {
		location.reload();

		});
	
}

function setDefaultProductImage(product_id, resource_id){
	var product_id = JSON.stringify(product_id);
	var resource_id = JSON.stringify(resource_id);

	$.ajax({
		method: "POST",
		url: "/actions/setDefaultProductImage",
		dataType: "json",
		data: {product_id: product_id, resource_id: resource_id},
		traditional: true
	})
	.done(function(msg) {
		location.reload();

		});
	
}



// basic regex title search
function req_filterProducts(searchTerm, currentSearchFilter, productData){
	$.ajax({
	  method: "POST",
	  url: "/actions/filterProducts",
	  dataType: "json",
	  data: { searchTerm: JSON.stringify(searchTerm), searchFilter: JSON.stringify(currentSearchFilter), productData: JSON.stringify(productData) },
	  traditional: true
	})
	  .done(function( matchIDList ) {
	  		filterResults(matchIDList);
	  });
	 
}




