//var url  = Android.getURL();
//var url = "shahani-w.blogspot.com/2013/02/on-overcoming-delusional-religious.html";
//var url = "thenextweb.com";
var url = "gizmodo.com";


function showDemo(){

	var demo = document.getElementById("demo");
	demo.style.opacity = 1;
	demo.style.zIndex = "9999";
	var name = document.getElementById("name");
	console.log(name.value);
	createHTML(name.value);


}

function closeDemo(){

	var demo = document.getElementById("demo");
	demo.style.opacity = 0;
	demo.style.zIndex = "-1";
	var myNode = document.getElementById("mainC");
	while (myNode.firstChild) {
		myNode.removeChild(myNode.firstChild);

	}

}

//createHTML(url);

function createHTML(url,callback){

		
		var urll = "http://4.oryx-web-engine.appspot.com/"+url+"/main";
		
	$.get(urll, function(xml){
	
		
		
		var outputjson = $.xml2json(xml);
		
		if(outputjson.HTTP.code != 200){
		
			var val = {};
				val['text'] = "Error file transforming url "+ url;
				new ErrorView(val);
				
				
		}
		
		
		if(outputjson.info.homepage != 1){
			var vcontent = outputjson.article.content;
			createNoneHomePage(vcontent);
		}
		else{
		
			createBlogHomePage(outputjson);
		}
		
		
		
		
	});
	
	
}

function cleanUp(){

		var myNode = document.getElementById("mainC");
		myNode.style.backgroundColor = "#fff";
}

function createNoneHomePage(vcontent){

		

		for(var i=0;i<vcontent.item.length;i++){
		
			if(vcontent.item[i]["tag"]=="text"){
				var val = {};
				val['text'] = vcontent.item[i];
				val['id'] = ""+i;
				new TextView(val);
			}
			
			else if(vcontent.item[i]["tag"]=="img"){
				var val = {};
				val['src'] = vcontent.item[i].attrVal;
				val['id'] = ""+i;
				new ImageView(val);
			}
			
			else if(vcontent.item[i]["tag"]=="a"){
				var val = {};
				val['link'] = vcontent.item[i].attrVal;
				var txt = vcontent.item[i].text;
				if(typeof txt == 'undefined'){
					continue;
				}
				val['text'] = txt;
				val['id'] = ""+i;
				new LinkView(val);
			}
		
		}

}

function createBlogHomePage(outputjson)
{

	var val = {};
	val['title'] = outputjson.info.pagetitle;
	new RSSHeader(val);
	
	var rssitems = outputjson.post;

	
	for(var i = 0; i<rssitems.item.length;i++){
	
		var val = {};
		val['id'] = i+"";
		val['date'] = rssitems.item[i].published;
		val['topic'] = rssitems.item[i].title;
		val['img'] = rssitems.item[i].image;
		val['link'] = rssitems.item[i].link;
		val['content'] = rssitems.item[i].summary;
		
		new RSSItem(val);
	
	}

}





