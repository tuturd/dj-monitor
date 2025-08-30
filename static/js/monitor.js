const updateTime = (clockDiv, endTimestamp, warningMinutes) => {
    if (endTimestamp && endTimestamp > 0) {
        const now = Math.floor(Date.now() / 1000);
        let secondsLeft = endTimestamp - now;
        if (secondsLeft < 0) secondsLeft = 0;
        const h = String(Math.floor(secondsLeft / 3600)).padStart(2, '0');
        const m = String(Math.floor((secondsLeft % 3600) / 60)).padStart(2, '0');
        clockDiv.textContent = `${h}:${m}`;
        if (h == 0 && m <= warningMinutes) {
            if (m <= 0) {
                clockDiv.className = "text-danger";
            } else {
                clockDiv.className = "text-warning";
            }
        } else {
            clockDiv.className = "text-light";
        }
    } else {
        clockDiv.textContent = "--:--";
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const body = document.getElementsByTagName("body")[0];
    const main = document.getElementsByTagName("main")[0];
    const clockDiv = document.getElementById("clock_container");
    const textDiv = document.getElementById("text_container");

    var endTimestamp = 0;
    var warningMinutes = 0;

    var socket = io();

    updateTime(clockDiv);

    socket.on('connect', function () {
        socket.emit('get_config');
    });

    socket.on('update_publication', function (data) {
        textDiv.textContent = data.text;
        textDiv.className = `text-${getBSColor(data.color)}`;
        if (data.text) {
            main.className = "has-text";
        } else {
            main.className = "";
        }
        if (data.blink_mode) {
            const color = textDiv.className.split('-')[1];
            const bgClass = `bg-${color}`;
            body.className = bgClass;
            let blinkCount = 0;
            const blinkInterval = setInterval(() => {
                if (blinkCount >= 4) {
                    clearInterval(blinkInterval);
                    body.classList.add('bg-black');
                    body.classList.remove(bgClass);
                } else {
                    body.classList.toggle('bg-black');
                    body.classList.toggle(bgClass);
                    blinkCount++;
                }
            }, 200);
        }
        endTimestamp = data.end_timestamp;
        warningMinutes = data.warning_minutes
    });

    socket.on('blink', function (data) {
        textDiv.className = `text-${getBSColor(data.color)}`;
        const bgClass = `bg-${getBSColor(data.color)}`;
        body.className = bgClass;
        let blinkCount = 0;
        const blinkInterval = setInterval(() => {
            if (blinkCount >= 4) {
                clearInterval(blinkInterval);
                body.classList.add('bg-black');
                body.classList.remove(bgClass);
            } else {
                body.classList.toggle('bg-black');
                body.classList.toggle(bgClass);
                blinkCount++;
            }
        }, 200);
    });

    const getBSColor = (color) => {
        switch (color) {
            case 'red':
                return "danger";
            case 'orange':
                return "warning";
            default:
                return "light";
        }
    }

    setInterval(function () {
        updateTime(clockDiv, endTimestamp, warningMinutes);
    }, 1000);
})