// this file manages collection list functions, similar to Main.js

var selectedCollections = {};
var minimumScroll = 0;
var isPositionFixed = false;
var actionBar;
var ratio = 1.3;
var collectionData = {};
var currentSearchFilter = {"filter":"Title"};
var selectAll = true;

$(document).ready(function(){
		collectionIDList = $("#collectionIDList").val().split(',');
		collectionIDList.pop();
		bindTableEvents();
		setupActionBar();
		scaleTiles();
		loadCollectionThumbnails();

});


function bindTableEvents(){
	$(window).resize(scaleTiles);

	$(".product_container").each(function(){
		var collection_id = $(this).attr('id').split('_')[1];
		$(this).find(".selectProduct").change({collection_id: collection_id}, selectCollection);
		
	});


	$("#btn_addCollection").click(go_newCollectionEditor);
	$(".btn_bulk_edit_collections").click({collection_id_list: selectedCollections}, goToBulkCollectionEditor);
	$(".btn_bulk_publish_collections").click({published:"true", collection_id_list: selectedCollections}, bulkPublish);
	$(".btn_bulk_hide_collections").click({published:"false", collection_id_list: selectedCollections}, bulkPublish);
	$(".btn_bulk_delete_collections").click({collection_id_list: selectedCollections}, bulkDelete);

	$(".btn_launch_editor").each(function(){
		var collectionID = $(this).attr('id').split('_')[1];
		$(this).click({collection_id: collectionID}, goToCollectionEditor)
		console.log(collectionID);
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


function selectCollection(event){
	event.stopPropagation();

	selectedCollection = $("#chk_" + event.data.collection_id);
	
	if(selectedCollection.is(':checked')){
		selectedCollections[event.data.collection_id] = event.data.collection_id;
	}
	else{
		delete selectedCollections[event.data.collection_id]
	}

	var nCollections = Object.keys(selectedCollections).length;

	if (nCollections > 0){
		$("#collection_action_bar").css("display","inline");
		
		if(nCollections == 1){
			$("#n_collections_selected").html("<b>" + nCollections + "</b> collection selected");
		}
		else{
			$("#n_collections_selected").html("<b>" + nCollections + "</b> collections selected");
		}

	}
	else if (nCollections == 0){
		$("#collection_action_bar").css("display","none");
	}

}




function loadCollectionThumbnails(){
	var collectionIDList = $("#collectionIDList").val().split(',');
	collectionIDList.pop();

	for (var i=0;i<collectionIDList.length;i++){
		
		var currentCollectionThumbnailContainer = "#collection_img_" + collectionIDList[i]
		var currentCollectionThumbnailSrc = $("#thumbnail_uri_"+collectionIDList[i]).val()
		console.log(currentCollectionThumbnailSrc);
		styleProperty = "url('" + currentCollectionThumbnailSrc + "')"
		$(currentCollectionThumbnailContainer).css('background-image',styleProperty);
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



function goToCollectionEditor(event){
	window.location.replace("/control/products/collections/"+event.data.collection_id);
}



function go_newCollectionEditor(){
	window.location.replace('/control/products/addCollection');

}

function goToBulkCollectionEditor(event){
	var collectionIDList = ""

	for (var key in selectedCollections) {
	    var collection_id = selectedCollections[key];
	    collectionIDList += (collection_id + ",")
	}

	collectionIDList = collectionIDList.slice(0, -1);
	window.location.replace("/control/products/collections/bulkEditor?ids="+collectionIDList);
}
