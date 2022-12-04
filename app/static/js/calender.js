let events = [
{
                title: 'Business Lunch',
                start: '2020-09-03T13:00:00',
                constraint: 'businessHours'
            },
            {
                title: 'Meeting',
                start: '2020-09-13T11:00:00',
                constraint: 'availableForMeeting', // defined below
                color: '#257e4a'
            },
            {
                title: 'Conference',
                start: '2020-09-18',
                end: '2020-09-20'
            },
            {
                title: 'Party',
                start: '2020-09-29T20:00:00'
            }, {
                title: 'Party',
                start: '2020-09-29T21:00:00'
            },

            // areas where "Meeting" must be dropped
            {
                groupId: 'availableForMeeting',
                start: '2020-09-11T10:00:00',
                end: '2020-09-11T16:00:00',
                display: 'background'
            },
            {
                groupId: 'availableForMeeting',
                start: '2020-09-13T10:00:00',
                end: '2020-09-13T16:00:00',
                display: 'background'
            },

            // red areas where no events can be dropped

            {
                start: '2020-09-25',
                end: '2020-09-26',
                overlap: false,
                display: 'background',
                color: '#ff9f89'
            }]

myData()

async function myData(){
   const res = await fetch('http://127.0.0.1:5000/api/dashboard/reservations/')
   const data = await res.json()
   console.log(data)
}

document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {

        timeZone: 'locale',
        locale: 'ar',

        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay,listMonth'
        },
        navLinks: true,
        businessHours: {
          // days of week. an array of zero-based day of week integers (0=Sunday)
          daysOfWeek: [ 0, 1, 2, 3, 4 ], // Monday - Thursday

          startTime: '10:00', // a start time (10am in this example)
          endTime: '18:00', // an end time (6pm in this example)
        },
        selectable: true,
        events: events
    });
    calendar.render();
});