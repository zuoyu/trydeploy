var url = "http://127.0.0.1:8000/api/authors/2/";

$.getJson(url,function(data){
	$.("#testbody").html(data.username);
});

