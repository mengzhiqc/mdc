$(document).ready(function(){
	$('#uploadImage').click(function(){
		$('#imageHandleForm').ajaxSubmit({
			'url':'/upload',
			'method':'POST',
			'success':function(data){
				$('#displayImage').empty().html(data);
			}
		});
		return false;
	});	
	});