let userID = null;
let currentWeekStart = getMonday(new Date());

/* ------------------- LOGIN ------------------- */
function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch('/api/login?username=' + encodeURIComponent(username) + '&password=' + encodeURIComponent(password))
        .then(r => {
            if (r.status === 200) return r.json();
            else throw new Error('Forkert brugernavn eller kode');
        })
        .then(data => {
            userID = data.UserID;
            document.getElementById('loginSection').style.display = 'none';
            document.getElementById('calendarSection').style.display = 'block';
            loadCalendar();
        })
        .catch(err => document.getElementById('loginMsg').innerText = err.message);
}

/* ------------------- HELPER ------------------- */
function getMonday(d) {
    d = new Date(d);
    const day = d.getDay();
    const diff = d.getDate() - day + (day === 0 ? -6 : 1);
    return new Date(d.setDate(diff));
}

function changeWeek(days) {
    currentWeekStart.setDate(currentWeekStart.getDate() + days);
    loadCalendar();
}

/* ------------------- LOAD CALENDAR ------------------- */
function loadCalendar() {
    const startStr = currentWeekStart.toISOString().split('T')[0];
    document.getElementById('weekLabel').innerText = 'Uge startende ' + startStr;

    fetch('/api/get_week?week_start=' + startStr)
        .then(r => r.json())
        .then(data => renderCalendar(data));
}

/* ------------------- RENDER CALENDAR ------------------- */
function renderCalendar(bookings) {
    const header = document.getElementById('calendarHeader');
    const body = document.getElementById('calendarBody');
    header.innerHTML = '';
    body.innerHTML = '';

    const days = [];
    for (let i = 0; i < 7; i++) {
        const d = new Date(currentWeekStart);
        d.setDate(d.getDate() + i);
        days.push(d);
    }

    // Header
    let th = '<tr><th>Time</th>';
    days.forEach(d => th += `<th>${d.toLocaleDateString('da-DK', { weekday: 'short', day:'numeric', month:'numeric'})}</th>`);
    th += '</tr>';
    header.innerHTML = th;

    // Timeslots 8-19, 2 timer
    for (let h = 8; h <= 19; h++) {
        let tr = `<tr><td>${h}:00 - ${h+2}:00</td>`;
        days.forEach(d => {
            const slotStart = new Date(d);
            slotStart.setHours(h,0,0,0);
            const slotEnd = new Date(slotStart);
            slotEnd.setHours(slotStart.getHours() + 2);

            const booked = bookings.filter(b => {
                const bStart = new Date(b.StartTime);
                const bEnd = new Date(b.EndTime);
                return !(slotEnd <= bStart || slotStart >= bEnd);
            });

            if (booked.length > 0) {
                const ownBooking = booked.find(b => b.UserID === userID);
                if (ownBooking) {
                    tr += `<td class="booked">Optaget (dig) <button onclick='cancelBooking(${ownBooking.BookingID})'>Annuller</button></td>`;
                } else {
                    tr += '<td class="booked">Optaget</td>';
                }
            } else {
                tr += `<td class="available" onclick='bookSlot("${slotStart.toISOString()}")'>Ledig</td>`;
            }
        });
        tr += '</tr>';
        body.innerHTML += tr;
    }
}

/* ------------------- BOOK SLOT ------------------- */
function bookSlot(startTime) {
    fetch('/api/book', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ UserID: userID, Room: 'Vaskerum1', StartTime: startTime })
    })
    .then(r => {
        if (r.status === 201) return r.text();
        else throw new Error('Kunne ikke booke, slot optaget');
    })
    .then(msg => {
        document.getElementById('bookingMsg').innerText = msg;
        loadCalendar();
    })
    .catch(err => document.getElementById('bookingMsg').innerText = err.message);
}

/* ------------------- CANCEL BOOKING ------------------- */
function cancelBooking(bookingID) {
    if (!confirm("Er du sikker på, du vil annullere denne booking?")) return;

    fetch('/api/cancel?BookingID=' + bookingID)
        .then(r => {
            if (r.status === 200) return r.text();
            else throw new Error('Kunne ikke annullere booking');
        })
        .then(msg => {
            document.getElementById('bookingMsg').innerText = msg;
            loadCalendar();
        })
        .catch(err => document.getElementById('bookingMsg').innerText = err.message);
}
