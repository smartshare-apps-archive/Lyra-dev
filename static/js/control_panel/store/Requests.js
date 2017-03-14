function saveNavigationSettings(event){
	$.ajax({
	  method: "POST",
	  url: "/actions/saveNavigationSettings",
	  dataType: "json",
	  data: { nav_data: JSON.stringify(navData) },
	  traditional: true
	})
	  .done(function(status) {
	  	window.location.reload();
	  });
}




// saves a single pages data
function savePageSectionData(event){
	var page_id = event.data.page_id;
	var page_section_data = "";

	for(section in pageData[page_id]["sections"]){

		var section_id = pageData[page_id]["sections"][section];
		
		if(section_id != "content"){
			var section_template = pageData[page_id]["section_data"][section_id]["section_template"];

			page_section_data += section_id + ":" + section_template + "<id_split>";
			var sectionAnchors = pageData[page_id]["section_data"][section_id];
			
			for(anchor in sectionAnchors){
				if (anchor == "section_template"){
					continue;
				}
				page_section_data += anchor + "<anchor_id_split>";

				for(anchor_tag in sectionAnchors[anchor]){
					var current_tag = sectionAnchors[anchor][anchor_tag];
					page_section_data += anchor_tag + "=" + current_tag + "<>";
				}

				page_section_data = page_section_data.slice(0,-2);

				page_section_data += "<split>";
			}
			page_section_data = page_section_data.slice(0,-7);

		page_section_data += "<section_split>";
		}
	}
	
	$.ajax({
	  method: "POST",
	  url: "/actions/savePageSectionData",
	  dataType: "json",
	  data: { page_id: JSON.stringify(page_id), page_section_data: JSON.stringify(page_section_data) },
	  traditional: true
	})
	  .done(function(status) {
	  	window.location.reload();
	  });
	  
}



// saves all pages theme data
function savePageThemes(event){
	for(var i=0;i<pageIDList.length;i++){

		var page_id = pageIDList[i];

		var page_section_data = "";

		for(section in pageData[page_id]["sections"]){

			var section_id = pageData[page_id]["sections"][section];
			
			if(section_id != "content"){
				page_section_data += section_id + ":" + pageData[page_id]["section_data"][section_id]["section_template"] + "<id_split>";
				var sectionAnchors = pageData[page_id]["section_data"][section_id];
				
				for(anchor in sectionAnchors){
					if (anchor == "section_template"){
						continue;
					}
					page_section_data += anchor + "<anchor_id_split>";

					for(anchor_tag in sectionAnchors[anchor]){
						var current_tag = sectionAnchors[anchor][anchor_tag];
						page_section_data += anchor_tag + "=" + current_tag + "<>";
					}

					page_section_data = page_section_data.slice(0,-2);

					page_section_data += "<split>";
				}
				page_section_data = page_section_data.slice(0,-7);

			page_section_data += "<section_split>";
			}
		}

		pageData[page_id]["page_section_data"] = page_section_data;
	}

	
	$.ajax({
	  method: "POST",
	  url: "/actions/savePageThemes",
	  dataType: "json",
	  data: {page_id_list: JSON.stringify(pageIDList), page_data: JSON.stringify(pageData) },
	  traditional: true
	})
	  .done(function(status) {
	  	window.location.reload();
	  });
	
}


function saveFooterSettings(event){
	$.ajax({
	  method: "POST",
	  url: "/actions/saveFooterSettings",
	  dataType: "json",
	  data: { footer_data: JSON.stringify(footerData) },
	  traditional: true
	})
	  .done(function(status) {
	  	window.location.reload();
	  });
}


function savePageData(event){
	$.ajax({
	  method: "POST",
	  url: "/actions/savePageData",
	  dataType: "json",
	  data: { page_data: JSON.stringify(pageData) },
	  traditional: true
	})
	  .done(function(status) {
	  	window.location.reload();
	  });
}



function createNewPage(event){
	var newPageData = {};

	$(".add_page_input").each(function(){
		var field_id = $(this).attr('data-fieldID');

		newPageData[field_id] = $(this).val();
	});


	$.ajax({
	  method: "POST",
	  url: "/actions/createNewPage",
	  dataType: "json",
	  data: { new_page_data: JSON.stringify(newPageData) },
	  traditional: true
	})
	  .done(function(status) {
	  	window.location.reload();
	  });
}



function deletePage(event){
	var page_id = pageData["page_id"];

	$.ajax({
	  method: "POST",
	  url: "/actions/deletePage",
	  dataType: "json",
	  data: { page_id: JSON.stringify(page_id) },
	  traditional: true
	})
	  .done(function(status) {
	  	window.location.href = "/control/store/pages";
	  });
}




// bulk functions
function bulkDeleteFiles(event){
	var resource_id_list = [];

	for (var key in selectedFiles) {
	    var resource_id = selectedFiles[key];
	    resource_id_list.push(resource_id);
	}
	
	$.ajax({
	  method: "POST",
	  url: "/actions/bulkDeleteResources",
	  dataType: "json",
	  data: { resource_id_list: JSON.stringify(resource_id_list) },
	  traditional: true
	})
	  .done(function( msg ) {
		location.reload();
	  });

	 
	 console.log(resource_id_list);
	 
}

