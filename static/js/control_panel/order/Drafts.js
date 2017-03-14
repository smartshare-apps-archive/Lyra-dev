
var minimumScroll = 110;
var isPositionFixed = false;
var actionBar;

//button handles
var btn_addDraft;


$(document).ready(function(){
		bindElements();
		bindEvents();
		bindTableEvents();
		//setupActionBar();
});

function bindElements(){
	btn_addDraft = $("#btn_addDraft");

}

function bindEvents(){
	btn_addDraft.click(go_CreateDraft);
}


function bindTableEvents(){
	$(".row_order").each(function(){
		var orderID = $(this).attr('id').split('_')[1];
		$(this).find(".order_link").attr("href","/control/orders/"+orderID);

	});

}

function go_CreateDraft(){
	window.location.href = "/control/orders/addDraft";
}


function go_OrderEditor(event){
	window.location.href = "/control/orders/"+event.data.order_id;
}







