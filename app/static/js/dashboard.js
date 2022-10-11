$(".range_HS").hide();
$("#picker-no-range").hide();
$("#time2-picker-no-range").prop("disabled", true);

function myFunction() {
	var x = document.getElementById("mySelect").value;
	if (x == "range") {
		$(".range_HS").show(500);
		$("#picker-no-range").hide();
	} else if (x == "no_range") {
		$("#picker-no-range").show(500);
		$(".range_HS").hide();
	} else {
		$(".range_HS").hide(500);
		$("#picker-no-range").hide(500);
	}
}

mobiscroll.setOptions({
	locale: mobiscroll.localeAr,
	theme: "ios",
	themeVariant: "light",
});

var date = new Date();
var current_date =
	date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate();

//        Range selector
mobiscroll.datepicker(".date-picker-range", {
	controls: ["calendar"],
	display: "anchored",
	selectMultiple: true,
	touchUi: true,
	select: "range",
	rangeHighlight: true,
	showRangeLabels: true,
	min: current_date,
	dateFormat: "MM/DD/YYYY",
	invalid: [
		{
			recurring: {
				repeat: "weekly",
				weekDays: "SA,FR",
			},
		},
	],
});

function range_date() {
	x = document.querySelector(".date-picker-range").value;
	val = x.split(" - ");
	start = new Date(val[0]);
	end = new Date(val[1]);
	var Difference = end.getTime() - start.getTime();
	var days = Difference / (1000 * 3600 * 24) + 1;
	console.log(days);
	console.log(val[0]);
	console.log(val[1]);
	$(".date-picker-range").val("تم تحديد " + days + " / يوم");
	$(".date_from_to").val(val[0] + "," + val[1]);
}

//     No_range selector
mobiscroll.datepicker("#date-picker-no-range", {
	controls: ["calendar"],
	dateFormat: "YYYY-MM-DD",
	selectMultiple: true,
	selectCounter: true,
	min: current_date,
	invalid: [
		{
			recurring: {
				repeat: "weekly",
				weekDays: "SA,FR",
			},
		},
	],
});
function no_range_date() {
	x = document.getElementById("date-picker-no-range").value;
	document.getElementById("date_from_to_no_range").value = x;
	val = x.split(", ");
	days = val.length;
	console.log(document.getElementById("date_from_to_no_range").value);
	$("#date-picker-no-range").val("تم تحديد " + days + " / يوم");
}
mobiscroll.datepicker("#time-picker-no-range", {
	controls: ["time"],
	timeFormat: "hh A",
	invalid: [
		{
			start: "17:00",
			end: "10:00",
			recurring: {
				repeat: "daily",
			},
		},
	],
});
function upto() {
	time1 = document.getElementById("time-picker-no-range").value.substring(0, 2);
	time2 = parseInt(time1);
	if (time2 < 9) time2 += 12;
	console.log(time2);
	$("#time2-picker-no-range").prop("disabled", false);

	mobiscroll.datepicker("#time2-picker-no-range", {
		controls: ["time"],
		timeFormat: "hh A",
		valid: [
			{
				start: time2 + ":00",
				end: "18:00",
				recurring: {
					repeat: "daily",
				},
			},
		],
	});
}

function space_validate() {
	if (document.form.spaceName.value == "hide") {
		alert("برجاء اختيار مساحة");
		return false;
	}
	if (document.form.type.value == "hide") {
		alert("برجاء تحديد نوع الحجز");
		return false;
	} else if (
		document.form.date_from_to.value == "" &&
		document.form.date_from_to_no_range.value == ""
	) {
		alert("برجاء تحديد ميعاد الحجز");
		return false;
	} else if (
		document.form.time_picker_no_range.value == "" &&
		document.form.time2_picker_no_range.value == ""
	) {
		if (document.form.date_from_to_no_range.value != "") {
			alert("برجاء تحديد توقيت الحجز");
			return false;
		} else if (document.form.date_from_to_no_range.value != "") {
			return true;
		}
	}
}

function tool_validate() {
	if (document.form.toolName.value == "hide") {
		alert("برجاء اختيار الأداة");
		return false;
	} else if (document.form.datetimes.value == "") {
		alert("برجاء تحديد ميعاد الحجز");
		return false;
	}
}

(() => {
	"use strict";
	ClassicEditor.create(document.querySelector("#description"), {
		language: "ar",
	}).then(() => {});

	ClassicEditor.create(document.querySelector("#guidelines"), {
		language: "ar",
	}).then(() => {});
	// Graphs
	const ctx = document.getElementById("myChart");
	// eslint-disable-next-line no-unused-vars
	if (ctx != null) {
		const myChart = new Chart(ctx, {
			type: "line",
			data: {
				labels: [
					"الأحد",
					"الإثنين",
					"الثلاثاء",
					"الأربعاء",
					"الخميس",
					"الجمعة",
					"السبت",
				],
				datasets: [
					{
						data: [15339, 21345, 18483, 24003, 23489, 24092, 12034],
						lineTension: 0,
						backgroundColor: "transparent",
						borderColor: "#007bff",
						borderWidth: 4,
						pointBackgroundColor: "#007bff",
					},
				],
			},
			options: {
				scales: {
					yAxes: [
						{
							ticks: {
								beginAtZero: false,
							},
						},
					],
				},
				legend: {
					display: false,
				},
			},
		});
	}
})();
