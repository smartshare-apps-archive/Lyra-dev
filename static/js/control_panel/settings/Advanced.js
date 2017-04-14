var btn_saveRedisConfig;
var btn_saveDatabaseConfig;

var btn_saveSetting;


// this container is passed to action db
var redisConfig = {};
var databaseConfig = {};


$(document).ready(function(){
	bindElements();
	bindEvents();

});


function bindElements(){
	btn_saveRedisConfig = $("#btn_saveRedisConfig");
	btn_saveDatabaseConfig = $("#btn_saveDatabaseConfig");
	btn_saveSetting = $("#btn_saveSetting");
}



function bindEvents(){
	//btn_savePaymentSettings.click(saveSettings);
	$(".editor_input_field").each(function(){
		var settingID = $(this).attr('data-settingID');
		var fieldID = $(this).attr('data-fieldID');

		if(settingID == "redis"){
			redisConfig[fieldID] = $(this).val();
 		}
		else if(settingID == "database"){
			databaseConfig[fieldID] = $(this).val();
		}

		$(this).change({setting_id:settingID, field_id: fieldID}, updateSettingData);

	});


	btn_saveRedisConfig.click({setting_id: "redis"}, confirmSettings);
	btn_saveDatabaseConfig.click({setting_id: "database"}, confirmSettings);
}



function updateSettingData(event){
	var setting_id = event.data.setting_id;
	var field_id = event.data.field_id;
	
	var selectorString_field = '[data-fieldID="' + field_id + '"]';
	var selectorString_setting = '[data-settingID="' + setting_id + '"]';

	var field_value = $(".editor_input_field" + selectorString_field + selectorString_setting).val();


	if(setting_id == "redis"){
			redisConfig[field_id] = field_value;
 	}
	else if(setting_id == "database"){
			databaseConfig[field_id] = field_value;
	}
}




function confirmSettings(event){
	var setting_id = event.data.setting_id;

	btn_saveSetting.unbind();

	if (setting_id == "redis"){
		btn_saveSetting.click(saveRedisConfig);
	}

	else if(setting_id == "database"){
		btn_saveSetting.click(saveDatabaseConfig);
	}
	

}
