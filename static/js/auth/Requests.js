function login(login_info){
	var login_info = JSON.stringify(login_info)

	$.ajax({
	  method: "POST",
	  url: "/auth/login",
	  dataType: "json",
	  traditional:true,
	  data: { login_info: login_info }
	})
	  .done(function(user_data) {
	  		console.log(user_data);
			return authenticate(user_data);
	  });

}


