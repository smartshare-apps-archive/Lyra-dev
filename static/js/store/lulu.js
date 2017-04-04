$(document).ready(function(){
	bindTemplateEvents();
	//console.log("lulu theme loaded.");
});





function bindTemplateEvents(){
	$(".nav_main_link.dropdown").each(function(){
		$(this).mouseenter(showSubmenu);

	});

	$("#nav_dropdown_lulu").mouseleave(hideSubmenu);

	$(".faq-question").each(function(){
		
	});
}


function showSubmenu(){
	$("#nav_dropdown_lulu").slideDown("fast");
}


function hideSubmenu(){
	$("#nav_dropdown_lulu").slideUp("fast");

}


