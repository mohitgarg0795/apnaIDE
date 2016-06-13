var url=window.location.pathname


var send_text=function(){
	var text=$('#textpad').val()
	$.get('ajaxtextpadcall', {text: text, url : url}, function(data){
               $('#textpad').html(data);
    });
}


var receive_text=function(){
	$.get('ajaxtextpadcall', {text: '1@$AS3^7#fjksjfkslj&&%$&!##', url: url}, function(data){
				//console.log(data)
				if(data!='1@$AS3^7#fjksjfkslj&&%$&!##')
                $('#textpad').val(data);
    });	
}

$('#textpad').keyup(send_text)

setInterval(receive_text,500)
