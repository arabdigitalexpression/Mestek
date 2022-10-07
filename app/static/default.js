$('.range_HS').hide();
$('#picker-no-range').hide();
$("#time2-picker-no-range").prop('disabled', true);





function myFunction() {
    var x = document.getElementById("mySelect").value;
    if (x == "range") {
        $('.range_HS').show(500);
        $('#picker-no-range').hide();
    }
    else if (x == "no_range") {
        $('#picker-no-range').show(500);
        $('.range_HS').hide();
    }
    else {
        $('.range_HS').hide(500);
        $('#picker-no-range').hide(500);
    }
}



var date = new Date();
current_date = date.getFullYear() + "/" + (date.getMonth() + 1) + "/" + date.getDate();
last_month = date.getMonth() + 3;
console.log(last_month)
if (last_month > 12) last_month -= 12;
last_date = date.getFullYear() + "/" + (last_month) + "/" + date.getDate();

//        Range selector
$('.input-daterange').datepicker({
    startDate: current_date,
    endDate: last_date,
    daysOfWeekDisabled: "5,6",
    todayHighlight: true,
    format: "yyyy/mm/dd",
    multidateSeparator: " "
});
function range_date() {
    x = document.querySelector(".date-picker-range").value;
    val = x.split(" - ");
    start = new Date(val[0]);
    end = new Date(val[1]);
    var Difference = end.getTime() - start.getTime();
    var days = (Difference / (1000 * 3600 * 24)) + 1;
    console.log(days);
    console.log(val[0]);
    console.log(val[1]);
    $(".date-picker-range").val("تم تحديد " + days + " / يوم")
    $(".date_from_to").val(val[0] + "," + val[1])
}


//     No_range selector
$('#date-picker-no-range').datepicker({
    startDate: current_date,
    endDate: last_date,
    multidate: true,
    daysOfWeekDisabled: "5,6",
    todayHighlight: true,
    format: "yyyy/mm/dd",
});
function no_range_date() {
    x = document.getElementById("date-picker-no-range").value;
    document.getElementById("date_from_to_no_range").value = x
    val = x.split(",");
    days = val.length;
    console.log(document.getElementById("date_from_to_no_range").value);
    $("#date-picker-no-range").val("تم تحديد " + days + " / يوم")
}

//    time
for (i = 9; i <= 15; i++) {
    val = i;
    option = i;
    pm_am = " ص"
    if (i > 12) {
        option -= 12;
        pm_am = " م"
    }
    else if (i == 12) {
        pm_am = " م"
    }
    $('#time-picker-no-range').append($('<option>', {
        value: val,
        text: option + pm_am,
    }));
    $('#time-picker-no-range').append($('<option>', {
        value: val + ":30",
        text: option + ":30" + pm_am,
    }));
}
function upto() {
    max_res =6;
    res = 0;
    value = document.getElementById("time-picker-no-range").value
    // console.log (value )

    $('#time2-picker-no-range')
    .find('option')
    .remove()
    .end()
    .append('<option value="hide">الي</option>')
    .val('hide');

    if (value == "hide") {
        $("#time2-picker-no-range").prop('disabled', true)
    }
    else {
        $("#time2-picker-no-range").prop('disabled', false);
        time = value.split(":")
        hours = parseInt(time[0]) + 2;
        if (time[1] == undefined) minutes = null;
        else minutes = ":" + time[1];
        // console.log(hours);
        for (hours; hours <= 18; hours = hours + 2) {
            res += 2;
            if (res <= max_res) {
                Hours = hours;
                pm_am = " ص"
                if (Hours > 12) {
                    Hours -= 12;
                    pm_am = " م"
                }
                else if (Hours == 12) {
                    pm_am = " م"
                }
                $('#time2-picker-no-range').append($('<option>', {
                    value: hours + minutes,
                    text: Hours + minutes + pm_am,
                }));

            }
        }
    }
}

$('.form_select').chosen();