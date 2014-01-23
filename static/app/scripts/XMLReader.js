function test(callback){
	x="";
	
	
	 $.get('http://4.oryx-web-engine.appspot.com/shahani-w.blogspot.com/', function(xml){
         
	       var outputjson = $.xml2json(xml);
	       console.log(outputjson.content.item[1]);
	});
//$.ajax({
//    url:'http://4.oryx-web-engine.appspot.com/shahani-w.blogspot.com',
//    dataType: 'xml',
//    success: function(data){
//        var xml = $(data);
//         x=$(xml).find('item');
//         alert(x[0].text());
//         callback(xml);
//    }
//});

}

  