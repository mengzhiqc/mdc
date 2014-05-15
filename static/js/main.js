$(document).ready(function(){

	$('#deleteBtn').bind('click',function(){

		if(!confirm("确定要删除这条记录么？")){
			return false;
		}
		
	});
	});

