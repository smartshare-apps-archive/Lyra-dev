var btn_saveShippingSettings;
var btn_saveShippoAPIKeys;

var btn_saveDefaultShippingAddress;
var btn_updateShippingInfo;

var btn_createNewPackageType;
var btn_savePackageTypes;
// this container is passed to action db
var shippingSettings = {};

$(document).ready(function(){
	bindElements();
	bindEvents();

});


function bindElements(){
	btn_saveShippingSettings = $("#btn_saveShippingSettings");
	btn_saveShippoAPIKeys = $("#btn_saveShippoAPIKeys");
	btn_updateShippingInfo = $("#btn_updateShippingInfo");
	btn_saveDefaultShippingAddress = $("#btn_saveDefaultShippingAddress");
	btn_createNewPackageType = $("#btn_createNewPackageType");
	btn_savePackageTypes = $("#btn_savePackageTypes");
}


function bindEvents(){
	$(".editor_input_field").each(function(){
		var fieldID = $(this).attr('data-fieldID');

		if(fieldID == "shipping_status"){
			var fieldValue = $(this).prop('checked');
			
			if (fieldValue == true){
				fieldValue = "enabled";
			}
			else{
				fieldValue = "disabled";
			}
			shippingSettings[fieldID] = fieldValue
		}
		else{
			shippingSettings[fieldID] = $(this).val();
		}

		$(this).change({fieldID: fieldID}, updateShippingSettings);
		
	});

	btn_saveShippoAPIKeys.click(saveShippoAPIKeys);
	btn_saveDefaultShippingAddress.click(saveDefaultShippingAddress);

	btn_updateShippingInfo.click(updateDefaultShippingAddress);

	btn_createNewPackageType.click(createNewPackageType);
	btn_savePackageTypes.click(savePackageTypes);
	console.log(shippingSettings);

	bindPackageTableEvents();
}





function bindPackageTableEvents(){
	updatePackageData();

	$(".btn-edit-package").each(function(){
		var packageID = $(this).attr('data-packageID');

		$(this).unbind();
		$(this).click(function(){
			populatePackageModal(packageID);
		});
	});

	$(".btn-delete-package").each(function(){

		var packageID = $(this).attr('data-packageID');
		$(this).unbind();
		$(this).click(function(){
			deletePackageType(packageID);
		});
	});

	
}



function populatePackageModal(packageID){
	console.log("Populating " + packageID);

	$("#btn_updatePackage").unbind();

	$(".package_editor_input_field").each(function(){
		var fieldID = $(this).attr('data-fieldID');
		$(this).val(shippingSettings["PackageTypes"][packageID][fieldID]);

		$(this).unbind();
		
		$(this).change(function(){
			updatePackageField(packageID, fieldID);
		});

	});

}




function updatePackageField(packageID, fieldID){
	var selectorString_field = '[data-fieldID="' + fieldID + '"]';
	var selectorString_package = '[data-packageID="' + packageID + '"]';
	var newValue = $(".package_editor_input_field" + selectorString_field).val();

	var label =  $(".package-label" + selectorString_field + selectorString_package);

	shippingSettings["PackageTypes"][packageID][fieldID] = newValue;

	label.html(newValue);

	console.log(shippingSettings);
}





function updatePackageData(){
	shippingSettings["PackageTypes"] = {};

	$(".package-label").each(function(){
		var packageID = $(this).attr('data-packageID');
		var fieldID = $(this).attr('data-fieldID');

		if(!(packageID in shippingSettings["PackageTypes"])){
			shippingSettings["PackageTypes"][packageID] = {};
		}

			var fieldValue = $(this).html();
			shippingSettings["PackageTypes"][packageID][fieldID] = fieldValue;
		

	});

	console.log(shippingSettings["PackageTypes"]);

}


function deletePackageType(packageID){
	var selectorString_package = '[data-packageID="' + packageID + '"]';
	var packageRow = $("tr" + selectorString_package);
	packageRow.remove();

	delete shippingSettings["PackageTypes"][packageID];

	updatePackageData();
}


function updateShippingSettings(event){
	var fieldID = event.data.fieldID;

	if(fieldID == "shipping_status"){
			var fieldValue = $(this).prop('checked');
			
			if (fieldValue == true){
				fieldValue = "enabled";
			}
			else{
				fieldValue = "disabled";
			}
			shippingSettings[fieldID] = fieldValue
		}
	else{
		shippingSettings[fieldID] = $(this).val();
	}
	
	console.log(shippingSettings);
}


function updateDefaultShippingAddress(){
	$(".shipping-label").each(function(){
		var fieldID = $(this).attr('data-fieldID');
		$(this).html(shippingSettings[fieldID]);
		console.log(shippingSettings[fieldID]);
		console.log(fieldID);
	});

}


function createNewPackageType(){

	$(".package_editor_input_field").each(function(){
		$(this).unbind();
		$(this).val("");

		$("#btn_updatePackage").unbind();
		
		$("#btn_updatePackage").click(function(){
			var newPackageData = {};

			var validPackage = true;
			newPackageTitle = $(".package_editor_input_field" + '[data-fieldID="title"]').val();

			if (newPackageTitle == "") {
				validPackage = false;
				return;
			}
			else{
				newPackageData["title"] = newPackageTitle;
			}
			
			$(".package_editor_input_field").each(function(){

				var fieldID = $(this).attr('data-fieldID');
				var fieldValue = $(this).val();

				if(fieldID == "title"){
					return;
				}

				if (fieldValue == ""){
					validPackage = false;
					return;
				}
		
				if (fieldID == "l" || fieldID == "w" || fieldID == "h"){
					if(parseFloat(fieldValue) == "NaN" || parseFloat(fieldValue) <= 0.00){
						validPackage = false;
						return;
					}
					else{
						newPackageData[fieldID] = fieldValue;
					}
				}

				else{
					newPackageData[fieldID] = fieldValue;
				}

			});

			if(validPackage){
				console.log(newPackageData);
				appendNewPackageType(newPackageData);
			}

			else{
				console.log("Invalid package data.");
			}
			
	
		});

	});


}

function appendNewPackageType(newPackageData){
	var packageTable = $("#table_packageTypes_body");

	newPackageRowHTML = "";
	newPackageRowHTML += "<tr data-packageID=\"" + newPackageData["title"] + "\">";
	newPackageRowHTML += "<td class=\"package-label\" data-fieldID=\"title\" data-packageID=\"" + newPackageData["title"] + "\">" + newPackageData["title"] + "</td>";
	newPackageRowHTML += "<td> <span class=\"package-label\" data-fieldID=\"l\" data-packageID=\"" + newPackageData["title"] + "\">" + newPackageData["l"] + "</span> x <span class=\"package-label\" data-fieldID=\"w\" data-packageID=\"" + newPackageData["title"] + "\">" + newPackageData["w"] + "</span> x <span class=\"package-label\" data-fieldID=\"h\" data-packageID=\"" + newPackageData["title"] + "\">" + newPackageData["h"] + "</span></td>";
	newPackageRowHTML += "<td class=\"package-label\"  data-fieldID=\"unit\" data-packageID=\"" + newPackageData["title"] + "\">" + newPackageData["unit"]  + "</td>";
	newPackageRowHTML += "<td> <button type=\"button\" class=\"btn btn-danger btn-delete-package\" data-packageID=\"" + newPackageData["title"] + "\"> Remove &nbsp;<span class=\"glyphicon glyphicon-trash\"> </span> </button> <button type=\"button\" class=\"btn btn-primary btn-edit-package\" data-packageID=\"" + newPackageData["title"] + "\" data-toggle=\"modal\" data-target=\"#modal_editPackage\"> Edit &nbsp;<span class=\"glyphicon glyphicon-pencil\"> </span> </button></td>";
	newPackageRowHTML += "</tr>";

	packageTable.append(newPackageRowHTML);
	bindPackageTableEvents();
}