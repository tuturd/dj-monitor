document.addEventListener("DOMContentLoaded", () => {
    const textInput = document.getElementById('text');
    const colorInput = document.getElementById('color');
    const blinkModeInput = document.getElementById('blink_mode');

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
        });
    });

    const updateConfigInputs = (data) => {
        textInput.value = data.text;
        colorInput.value = data.color;
        blinkModeInput.value = data.blink_mode ? 'yes' : 'no';
        textInput.focus();
    }
})