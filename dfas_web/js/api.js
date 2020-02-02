weatherIcons = {
	"Clear": "fa-sun", 
	"Clouds": "fa-cloud-sun",
	"Snow": "fa-snowflake",
	"Rain": "fa-umbrella",
	"Thunderstorm": "fa-poo-storm",
	"Others": "fa-smog"
}

jQuery(function GetEntering() {
	$("#currentTime").text((new Date).toLocaleString());
	$.ajax({
		type: "GET",
		url: "https://bfkjmzh4i2.execute-api.ap-northeast-1.amazonaws.com/prod/entering",
		dataType: "json",
		success: function (result, status, xhr) {
			$("#entering-events").empty();
			$.each(result["History"], function(index, value) {
				b = new Date(0);

				switch(value["event"]){
					case "Entering": color ="btn-success"; icon="fa-check"; text = "Entering detected."; break;
					case "Leaving": color="btn-danger"; icon="fa-walking"; text = "Entering eliminated."; break;
				}
				b.setUTCMilliseconds(value["timestamp"]);
				$("#entering-events").prepend('<div class="m-1"><span class="btn btn-sm '
					+ color
					+ ' btn-circle"><i class="fas '
					+ icon
					+ '"></i></span><span class="h6 m-2">'
					+ b.toLocaleString()
					+ "&nbsp;" + text
					+ "</span>");
			});
		},
		error: function (xhr, status, error) {}
	});
	setTimeout(GetEntering, 1000);
});

jQuery(function GetGps() {
	$.ajax({
		type: "GET",
		url: "https://bfkjmzh4i2.execute-api.ap-northeast-1.amazonaws.com/prod/gps",
		dataType: "json",
		success: function (result, status, xhr) {
			$("#gps-info").html(result["lat"] + ", " + result["lon"]);
			
			drone_location = {lat: parseFloat(result["lat"]), lng: parseFloat(result["lon"])};
			
			map = new google.maps.Map(document.getElementById('gmap'), {
				center: drone_location,zoom: 16
			});
			
			var marker = new google.maps.Marker({
				position: drone_location,
				map: map,
				title: 'Drone'
			});
		},
		error: function (xhr, status, error) {}
	});
	setTimeout(GetGps, 10000);
});

jQuery(function UpdateImage() {
	b = new Date();
	url = "http://ecsimageprovider-insightful-cheetah-rt.cfapps.io/getimage?time=" + b.getTime();
	$("#sky-camera").attr("src", url);
	$("#camera-update").text("Updated on " + b.toLocaleTimeString());
	setTimeout(UpdateImage, 10000);
});

jQuery(function GetTemperature() {
	$.ajax({
		type: "GET",
		url: "https://bfkjmzh4i2.execute-api.ap-northeast-1.amazonaws.com/prod/temperature",
		dataType: "json",
		success: function (result, status, xhr) {
			$("#current-temperature").html(result["temperature"] + "&deg;C");
		},
		error: function (xhr, status, error) {}
	});
	setTimeout(GetTemperature, 3000);
});
	
jQuery(function GetWeather() {
	$.ajax({
		type: "POST",
		url: "http://api.openweathermap.org/data/2.5/weather?units=metric&lat=35.65104&lon=139.573186667&appid=2801b18ca5fb3b028524dc2b64d3b8f4",
		dataType: "json",
		success: function (result, status, xhr) {
			$("#weather-text").html(result["weather"][0]["main"]);
			$("#weather-city").html(result["name"] + ", " + result["sys"]["country"]);
			$("#weather-temperature").html(result["main"]["temp_min"] + "&deg;C to " + result["main"]["temp_max"] + "&deg;C");
			$("#weather-humidity").html(result["main"]["humidity"] + "%");
			$("#weather-humidity-bar").attr("aria-valuenow", result["main"]["humidity"]).width(result["main"]["humidity"]+"%");
			$("#weather-icon").removeClass("fa-question-circle").addClass(function(){
				if (result["weather"][0]["main"] in weatherIcons) { 
					return weatherIcons[result["weather"][0]["main"]];
				} else return weatherIcons["Others"];
			});
			$("#weather-sunset").html(function(){
				b = new Date(0);
				b.setUTCSeconds(result["sys"]["sunset"]);
				return "Sunset at " + b.toLocaleTimeString()
			});
			$("#weather-sunrise").html(function(){
				b = new Date(0);
				b.setUTCSeconds(result["sys"]["sunrise"]);
				return "Sunrise at " + b.toLocaleTimeString()
			});
		},
		error: function (xhr, status, error) {}
	});
	setTimeout(GetWeather, 5000);
});
