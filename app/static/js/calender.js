let getReservations = async () => {
    let events = []
    const res = await fetch("/api/reservations/");
    const data = await res.json();
    events = data
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        timeZone: 'Africa/Cairo',
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
}
document.addEventListener('DOMContentLoaded', async function () {
    await getReservations()
});