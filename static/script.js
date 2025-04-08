let currentSchedule = [];
let currentDate = "";
let persistentNotification = null;
let activeTaskTitle = null;
let taskStartTime = null;

document.addEventListener("DOMContentLoaded", function () {
    const schedule = JSON.parse(document.getElementById("schedule-data").textContent);
    const now = new Date();
    const currentDay = now.toLocaleString("en-US", { weekday: "long" });

    let currentTaskElement = document.getElementById("current-task");
    let upcomingTaskElement = document.getElementById("upcoming-task");

    function parseTimeToDate(timeStr) {
        const [hours, minutes] = timeStr.split(":").map(Number);
        const date = new Date();
        date.setHours(hours, minutes, 0, 0);
        return date;
    }

    function getCurrentAndNextTask(daySchedule, currentTime) {
        let currentTask = null;
        let nextTask = null;

        for (let i = 0; i < daySchedule.length; i++) {
            const task = daySchedule[i];
            const start = parseTimeToDate(task.start);
            const end = parseTimeToDate(task.end);

            if (currentTime >= start && currentTime <= end) {
                currentTask = task;
                nextTask = daySchedule[i + 1] || null;
                break;
            } else if (currentTime < start) {
                nextTask = task;
                break;
            }
        }

        return { currentTask, nextTask };
    }

    function playBackendAlarm(title, end, nextTask) {
        const audio = new Audio("/static/alarm.mp3");
        audio.play();

        const spokenText = `It's time to ${title} until ${end}. Next: ${nextTask ? nextTask.title : "no more tasks"}`;
        const msg = new SpeechSynthesisUtterance(spokenText);
        speechSynthesis.speak(msg);

        showNotification("Study Task", spokenText);

        taskStartTime = new Date();
        activeTaskTitle = title;
    }

    function showNotification(title, body) {
        if (Notification.permission === "granted") {
            if (persistentNotification) persistentNotification.close();
            persistentNotification = new Notification(title, {
                body: body,
                icon: "/static/icon.png",
                tag: "ongoing-task",
                renotify: true
            });
        }
    }

    function updatePersistentNotification(title) {
        if (!taskStartTime) return;
        const now = new Date();
        const diff = now - taskStartTime;
        const mins = Math.floor(diff / 60000);
        const hours = Math.floor(mins / 60);
        const minutes = mins % 60;
        const body = `${title} is running for ${hours} hour(s) and ${minutes} minute(s).`;

        showNotification("Active Task", body);
    }

    function checkAndNotifyTask() {
        const currentTime = new Date();
        const daySchedule = schedule[currentTime.toLocaleString("en-US", { weekday: "long" })] || [];
        const { currentTask, nextTask } = getCurrentAndNextTask(daySchedule, currentTime);

        updateTaskInfo(currentTask, document.getElementById("current-task"));
        updateTaskInfo(nextTask, document.getElementById("upcoming-task"));

        if (currentTask) {
            const { title, start, end } = currentTask;

            if (!window.lastAlarmTime || window.lastAlarmTime !== start) {
                playBackendAlarm(title, end, nextTask);
                window.lastAlarmTime = start;
            } else {
                updatePersistentNotification(title);
            }
        } else {
            activeTaskTitle = null;
            taskStartTime = null;
            if (persistentNotification) {
                persistentNotification.close();
                persistentNotification = null;
            }
        }
    }

    function updateTaskInfo(task, element) {
        if (task) {
            element.textContent = `${task.title} (${task.start} - ${task.end})`;
        } else {
            element.textContent = "None";
        }
    }

    if (Notification.permission !== "granted" && Notification.permission !== "denied") {
        Notification.requestPermission();
    }

    checkAndNotifyTask();
    setInterval(checkAndNotifyTask, 60000);
});

// Functions for frontend day-schedule (click-based)
function loadDaySchedule(dateStr) {
    $.get("/day_schedule/" + dateStr, function (data) {
        currentSchedule = data;
        currentDate = dateStr;
        $("#selected-date").text(dateStr);
        $("#day-details").empty();

        data.forEach((task, index) => {
            let checked = isTaskCompleted(dateStr, index) ? "checked" : "";
            $("#day-details").append(`
                <li style="${checked ? 'text-decoration:line-through;color:gray;' : ''}">
                    <input type="checkbox" data-index="${index}" onchange="markTaskDone(this)" ${checked}> ${task}
                </li>
            `);
        });

        $("#detail-section").show();
        window.scrollTo(0, document.body.scrollHeight);
    });
}

function isTaskCompleted(date, index) {
    let key = `task_${date}_${index}`;
    return localStorage.getItem(key) === "done";
}

function markTaskDone(elem) {
    let index = elem.getAttribute("data-index");
    let key = `task_${currentDate}_${index}`;
    if (elem.checked) {
        localStorage.setItem(key, "done");
    } else {
        localStorage.removeItem(key);
    }
    loadDaySchedule(currentDate);
}

function toMinutes(t) {
    let [h, m] = t.split(":").map(Number);
    return h * 60 + m;
}

function getTimeDifference(currentTime, futureTimeStr) {
    let [fh, fm] = futureTimeStr.split(":").map(Number);
    let future = new Date(currentTime);
    future.setHours(fh, fm, 0, 0);
    if (future < currentTime) future.setDate(future.getDate() + 1);
    let diff = future - currentTime;
    let mins = Math.floor(diff / 60000);
    let hours = Math.floor(mins / 60);
    let days = Math.floor(hours / 24);
    mins %= 60;
    hours %= 24;
    let text = `${days ? days + " day " : ""}${hours ? hours + " hour " : ""}${mins} min`.trim();
    return { text };
}

function fetchBackendDateTime() {
    setInterval(() => {
        $.get("/current_datetime", function (data) {
            $("#real-datetime").text(`Date: ${data.date} | Time: ${data.time}`);
        });
    }, 1000);
}

$(document).ready(function () {
    const today = new Date();
    const dateStr = `${pad(today.getDate())}-${pad(today.getMonth() + 1)}-${today.getFullYear()}`;
    loadDaySchedule(dateStr);
    requestNotificationPermission();
    fetchBackendDateTime();
});

function pad(n) {
    return n.toString().padStart(2, '0');
}

function requestNotificationPermission() {
    if (Notification.permission !== "granted") {
        Notification.requestPermission();
    }
}