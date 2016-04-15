var send_text=function(){
	var text=$('#textpad').val()
	$.get('AAAAAA', {text: text}, function(data){
               $('#textpad').html(data);
               $('#likes').hide();
    });
}


var receive_text=function(){
	$.get('AAAAAA', {text: '1@$AS3^7#fjksjfkslj&&%$&!##'}, function(data){
				console.log(data)
				if(data!='1@$AS3^7#fjksjfkslj&&%$&!##')
               		$('#textpad').val(data);
                $('#likes').hide();
    });	
}

$('#textpad').keyup(send_text)

setInterval(receive_text,500)
