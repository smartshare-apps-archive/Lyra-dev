<script type="text/javascript">

	$(document).ready(function(){
		$("#btn_demoSignUp").click(submit_email);

	});


	function submit_email(){
		var email = $("#input_emailSignup").val();
		var type = "email_signup";

		$.ajax({
		  method: "GET",
		  url: "/actions/store_message",
		  data: { 
		    body: email,
		    type: type
		  },
	
		})
		  .done(function(response) {
		  		updateAndShowModal(response);
		  });

	}

	function updateAndShowModal(response){
		if(response != "\"invalid\""){
			console.log(response);
			$("#modal_emailSignup").modal('show');
			$("#input_emailSignup").val("");
		}
	}

</script>


