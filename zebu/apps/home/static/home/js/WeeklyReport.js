window.onload = function () {
	var weekday = document.getElementById("cur_day").value;
	var x = $(".listyle");
	for (var i = 0; i < x.length; i++) {
		var j = i;
		var total = document.getElementById("total" + j).getAttribute("value");
		var used = document.getElementById("used" + j).value;
		if ((i + 1) % 7 == weekday) {
			document.getElementById("week" + (i + 1)).style.backgroundColor = "#00bfff";
		}
        //alert(used);
		if (x[i].innerHTML) {
			if (0 == total) {
				percent = 0
			} else {
				percent = used / total
			}
			displayPrecent("W3Cfuns_canvas" + j, percent, x[i].innerHTML);
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
//function weekClick(d,tab_id ) {
function weekClick(d) {
	var x = $(".listyle");
	var weekday = document.getElementById("cur_day").value;
	for (var j = 1; j <= x.length; j++) {
		document.getElementById("week" + j).style.backgroundColor = "#e2e3e3";
		if (j % 7 == weekday) {
			document.getElementById("week" + j).style.backgroundColor = "#00bfff";
			
		}
		
		if (parseInt((j-1) / 7) == parseInt((d-1) / 7)) {
//			console.debug(parseInt(j / 7))
//			console.debug(parseInt(d / 7))
			
			document.getElementById("week" + j).style.backgroundColor = "#e2e3e3";
			document.getElementById("week" + d).style.backgroundColor = "#00bfff";
		}

		

		//
	}
	//document.getElementById("week" + d).style.backgroundColor = "#00bfff";
}