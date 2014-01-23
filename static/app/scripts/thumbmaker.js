


function makeThumb()
{
var list = img_find();

	for(var i=0;i<list.length;i++)
	{
		//new ThumbImageView(list[i]["src"],list[i]["id"].split("_")[1],100);
	}
}


function ThumbImageView(imgs,id,offsettop)
{

	var thumI = document.createElement("img");
	thumI.className = "thumb";
	var tid = "thumb_"+id;
	thumI.id = tid;
	thumI.src = imgs;
	thumI.style.marginTop = offsettop;
	thumI.onclick = function(tid) { showImgs(tid) };
	document.getElementById("resView").appendChild(thumI);
}

function img_find() {
    var imgs = document.getElementsByTagName("img");
    var imgSrcs = [];
    for (var i = 0; i < imgs.length; i++) {
	
		var val = {};
		val['src'] = imgs[i].src;
		val['id'] = imgs[i].id;
        imgSrcs.push(val);
		
    }

    return imgSrcs;
}

function showImgskjk(idd)
{
	var t = idd.toElement.id;
	var id = t.split("_")[1];
	$("#img_"+id).slideToggle("medium");

}