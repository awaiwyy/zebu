window.onload = function() {
	var weekday = document.getElementById("cur_day").value;
   document.getElementById("week" + weekday).style.backgroundColor = "#00bfff";
	var x = $(".listyle");
	for (var i = 0; i < x.length; i++) {
		var j=i;
		var total = document.getElementById("total"+j).getAttribute("value");
      var used = document.getElementById("used"+j).value;
        //alert(used);
		if (x[i].innerHTML) {
			if(0 == total) {
				percent = 0
			}else{
				percent = used/total	
			}
			displayPrecent("W3Cfuns_canvas"+j,percent, x[i].innerHTML);
		}
	}
};

// display percent color
function displayPrecent(str, percent, detail) {
	var canvas = document.getElementById(str);
	var content = canvas.getContext("2d");// 取得图形上下文 graphics context
	var height = 174 * (1 - percent);
	content.fillStyle = "#aedeea";// 矩形填充颜色
	content.fillRect(0, height, 96, 174);// 矩形坐标及大小
	content.font = "naomal small-caps normal 40px Arial";
	content.fillStyle = "black";
	content.fillText(parseInt(percent * 100) + "%", 40, 170);
};

/* 点击的日期变色 */
function weekClick(d,tab_id ) {
	for (var j = 1; j <= 7; j++) {
	   // alert("week" + j );
		document.getElementById("week" + j + tab_id).style.backgroundColor = "#f4f4f4";
	}
//	for (var j = 8; j <= 14; j++) {
//		document.getElementById("week" + j).style.backgroundColor = "";
//	}
	document.getElementById("week" + d + tab_id).style.backgroundColor = "#00bfff";
}