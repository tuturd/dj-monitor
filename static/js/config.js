document.addEventListener("DOMContentLoaded", () => {
    const textInput = document.getElementById('text');
    const colorInput = document.getElementById('color');
    const blinkModeInput = document.getElementById('blink_mode');
    const dateInput = document.getElementById('date');
    const timeInput = document.getElementById('time');
    const warningMinutesInput = document.getElementById('warningMinutes');
    const clock = document.getElementById('clock');
    const countdown = document.getElementById('countdown');

    textInput.focus();

    document.getElementById('configForm').addEventListener('submit', function (e) {
        e.preventDefault();
        const formData = new FormData(this);
        const body = JSON.stringify({
            text: formData.get('text'),
            color: formData.get('color'),
            blink_mode: formData.get('blink_mode') == 'yes'
        });
        fetch('/publication', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: body
        })
            .then(response => response.json())
            .then(data => {
                updateConfigInputs(data);
            });
    });

    document.getElementById('clearBtn').addEventListener('click', function (e) {
        const body = JSON.stringify({
            clear: 1,
            color: colorInput.value,
            blink_mode: blinkModeInput.value == 'yes'
        })
        fetch('/publication', {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
            body: body
        })
            .then(response => response.json())
            .then(data => {
                updateConfigInputs(data);
            });
    });

    document.getElementById('blinkBtn').addEventListener('click', function (e) {
        const body = JSON.stringify({
            color: colorInput.value,
        })
        fetch('/blink', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: body
        });
    });

    document.getElementById('scheduleForm').addEventListener('submit', function (e) {
        e.preventDefault();
        const formData = new FormData(this);
        const config = {
            date: formData.get('date'),
            time: formData.get('time'),
            warning_minutes: formData.get('warningMinutes')
        };
        fetch('/config/end-time', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(config)
        })
            .then(() => {
                setCountdownTarget(config.date, config.time, config.warning_minutes);
            });
    });

    const updateConfigInputs = (data) => {
        textInput.value = data.text;
        colorInput.value = data.color;
        blinkModeInput.value = data.blink_mode ? 'yes' : 'no';
        textInput.focus();
    }

    let countdownTarget = null;
    let warningMinutes = 0;

    if (dateInput && timeInput && dateInput.value && timeInput.value) {
        countdownTarget = new Date(`${dateInput.value}T${timeInput.value}`);
    }
    if (warningMinutesInput && warningMinutesInput.value) {
        warningMinutes = parseInt(warningMinutesInput.value, 10) || 0;
    }

    const setCountdownTarget = (dateStr, timeStr, warning) => {
        if (dateStr && timeStr) {
            countdownTarget = new Date(`${dateStr}T${timeStr}`);
        }
        warningMinutes = warning ? parseInt(warning, 10) || 0 : 0;
    }

    const updateClocks = () => {
        const now = new Date();
        const hh = String(now.getHours()).padStart(2, '0');
        const mm = String(now.getMinutes()).padStart(2, '0');
        const ss = String(now.getSeconds()).padStart(2, '0');
        clock.textContent = `${hh}:${mm}:${ss}`;

        if (countdownTarget && countdown) {
            let diff = Math.floor((countdownTarget - now) / 1000);
            if (diff > 0) {
                const hours = Math.floor(diff / 3600);
                const minutes = Math.floor((diff % 3600) / 60);
                const seconds = diff % 60;
                if (hours >= 1) {
                    countdown.textContent = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
                } else {
                    countdown.textContent = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
                    countdown.classList.remove('text-light', 'text-warning', 'text-danger');
                    if (diff <= 0) {
                        countdown.classList.add('text-danger');
                        countdown.textContent = '00:00';
                    } else if (minutes < warningMinutes) {
                        countdown.classList.add('text-warning');
                    } else {
                        countdown.classList.add('text-light');
                    }
                }
            } else {
                countdown.classList.remove('text-warning');
                countdown.classList.add('text-danger');
                countdown.textContent = '00:00';
            }
        } else if (countdown) {
            countdown.classList.remove('text-warning', 'text-danger');
            countdown.textContent = '';
        }
    }

    setInterval(updateClocks, 1000);

    updateClocks();
})