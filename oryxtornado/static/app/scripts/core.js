
var mainC = document.getElementById("mainC");

function HeaderView(props)
{
	var div = document.createElement("div");
	div.className = "header";
	div.id = div.className+"_1";
	mainC.appendChild(div);
	var logo = document.createElement("img");
	logo.src = props['logo'];
	logo.align = 'left';
	var title = document.createElement("h2");
	title.innerHTML = props['title'];
	document.getElementById(div.id).appendChild(logo);
	document.getElementById(div.id).appendChild(title);
}

function TitleView(props)
{

	var title = document.createElement("h3");
	title.id = "title_1"
	title.innerHTML = props['title'];
	mainC.appendChild(title);
}

function TextView(props)
{

	var title = document.createElement("p");
	title.id = "text_"+props['id'];
	title.innerHTML = props['text'];
	mainC.appendChild(title);
}

function LinkView(props)
{

	var link = document.createElement("a");
	link.id = "link"+props['id'];
	link.className = 'link';
	link.href = props['link'];
	mainC.appendChild(link);
	var w = document.createElement("div");
	w.innerHTML = props['text'];
	document.getElementById(link.id).appendChild(w);
}

function ImageView(props)
{

/* 	var contt = document.createElement("div");
	contt.className = "thumbImage";
	mainC.appendChild(contt);
	var cont = document.createElement("div");
	cont.className = "smallImg";
	mainC.appendChild(cont); */
	
	var logo = document.createElement("img");
	logo.id="img_"+props['id'];
	logo.src = props['src'];
	logo.className = "rss-img";
	logo.align = "left";
	tid = logo.id;
	logo.onclick = function(tid) { showRSSImgs(tid) };
	mainC.appendChild(logo);
	
}

function ErrorView(props)
{

	var w = document.createElement("div");
	w.className = 'error';
	w.innerHTML = props['text'];
	mainC.appendChild(w);
	
}

function InfoView(props)
{

	var w = document.createElement("div");
	w.className = 'info';
	w.innerHTML = props['text'];
	mainC.appendChild(w);
	
}

function showImgs(idd)
{
	var it = idd.toElement.id;
	var imm = document.getElementById("c_"+it).style.marginLeft;
	var ml = '0%';
	if (imm === '0%'){
		ml = '70%';
	}
	$('#c_'+it).animate({
        marginLeft: ml
    });
}

function RSSHeader(props)
{
	var div = document.createElement("div");
	div.className = "rssheader";
	mainC.appendChild(div);
	
	var title = document.createElement("h2");
	title.innerHTML = props['title'];
	div.appendChild(title);
	
	var hr = document.createElement("hr");
	div.appendChild(hr);
}

function RSSItem(props)
{
	var div = document.createElement("div");
	div.className = "rss-item";
	mainC.appendChild(div);
	
	var date = document.createElement("p");
	date.className = "rss-date";
	date.innerHTML = "<span>"+props['date']+"</span>";
	div.appendChild(date);
	
	var tp = document.createElement("p");
	tp.className = "rss-topic";
	tp.innerHTML = props['topic'];
	tp.id = props['link'];
	var rssid = tp.id;
	tp.onclick = function(rssid) { showPost(rssid) };
	div.appendChild(tp);
	
	var img = document.createElement("img");
	img.className = "rss-img";
	img.src = props['img'];
	img.align = "left";
	img.id = "rss_"+props['id'];
	idd = img.id;
	img.onclick = function(idd) { showRSSImgs(idd) };
	div.appendChild(img);
	
	var c = document.createElement("p");
	c.className = "rss-content";
	c.innerHTML = props['content'] + "... <span>&raquo</span>";
	div.appendChild(c);
	
	var hr = document.createElement("hr");
	div.appendChild(hr);
	

}

function showPost(link)
{
	var ll = link.toElement.id;
	ll = ll.substring(7);
	var linkk = ll;
	
	var myNode = document.getElementById("mainC");
	while (myNode.firstChild) {
		myNode.removeChild(myNode.firstChild);

	}
	
	createHTML(linkk);
	
}

function showRSSImgs(idd)
{
	var it = idd.toElement.id;
	
	var imm = document.getElementById(it).style.width;
	var ml = '100%';
	if (imm === '100%'){
		ml = '30%';
	}
	
	$('#'+it).animate({
        width: ml
    });
}

function createContainer()
{
	var div = document.createElement("div");
	div.className = "main";
	div.id = "mainC";
	document.body.appendChild(div); 
}


