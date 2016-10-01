/*火狐低版本浏览器侧边栏不显示问题  */
var Sys = {};
var userAgent = navigator.userAgent.toLowerCase();
var browserVersion;
(browserVersion = userAgent.match(/firefox\/([\d.]+)/)) ? Sys.firefox = browserVersion[1]
		: 0;
if (userAgent.indexOf("firefox") > -1 && Sys.firefox < 20) {
	$(".wrapper").css({
		"position" : "static",
		"overflow" : "hidden"
	});
	$("body").css("position", "static");
	$(".main-panel").css("width", "-moz-calc(100% - 260px)");
}