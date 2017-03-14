var btn_confirmAddPage;

$(document).ready(function(){
	bindTableEvents();
	
	bindElements();
	bindEvents();

});

function bindElements(){
	btn_confirmAddPage = $("#btn_confirmAddPage");

}

function bindEvents(){
	btn_confirmAddPage.click(createNewPage);

}


function bindTableEvents(){
}



