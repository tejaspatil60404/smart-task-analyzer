let tasks = [];

// Render task list
function renderTaskList() {
    const list = document.getElementById("taskList");
    if (tasks.length === 0) {
        list.className = "placeholder";
        list.innerHTML = "No tasks added.";
        return;
    }
    list.className = "";
    list.innerHTML = "";

    tasks.forEach(t => {
        list.innerHTML += `
            <div class="task-item">
                <div class="task-title">#${t.id} — ${t.title}</div>
                <div class="task-meta">
                    Due: ${t.due_date || "-"} • 
                    Hours: ${t.estimated_hours || "-"} • 
                    Importance: ${t.importance || "-"}
                </div>
            </div>
        `;
    });
}

function addTask() {
    const t = {
        id: tasks.length + 1,
        title: document.getElementById("title").value.trim(),
        due_date: document.getElementById("due_date").value,
        estimated_hours: parseFloat(document.getElementById("hours").value),
        importance: parseInt(document.getElementById("importance").value),
        dependencies: document.getElementById("dependencies").value
            .split(",").map(x => x.trim()).filter(x => x).map(Number)
    };

    if (!t.title) { setStatus("Title is required", true); return; }

    tasks.push(t);
    renderTaskList();
    setStatus("Task added");
}

function setStatus(msg, error=false) {
    const el = document.getElementById("status");
    el.style.color = error ? "#dc2626" : "#6b7280";
    el.innerText = msg;
}

function getTasksFromUser() {
    const jsonText = document.getElementById("jsonInput").value.trim();
    if (jsonText) {
        try { return JSON.parse(jsonText); }
        catch { setStatus("Invalid JSON", true); return null; }
    }
    return tasks;
}

function analyzeTasks() {
    const data = getTasksFromUser();
    if (!data) return;

    setStatus("Analyzing...");
    fetch("http://127.0.0.1:8000/api/tasks/analyze/", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    })
    .then(r => r.json())
    .then(showResults)
    .catch(() => setStatus("Error", true));
}

function suggestTasks() {
    const data = getTasksFromUser();
    if (!data) return;

    setStatus("Suggesting...");
    fetch("http://127.0.0.1:8000/api/tasks/suggest/", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    })
    .then(r => r.json())
    .then(showResults)
    .catch(() => setStatus("Error", true));
}

function resetAll() {
    tasks = [];
    document.getElementById("taskList").innerHTML = "";
    document.getElementById("results").innerHTML = "";
    setStatus("Reset");
}

function showResults(data) {
    const box = document.getElementById("results");
    box.innerHTML = "";
    box.className = "";

    data.forEach(task => {
        let priority =
            task.score >= 25 ? "high" :
            task.score >= 15 ? "medium" : "low";

        box.innerHTML += `
            <div class="result-card ${priority}">
                <strong>${task.title}</strong>
                <p>Score: ${task.score}</p>
                <p>${task.reason}</p>
                ${task.suggest_reason ? `<p><em>${task.suggest_reason}</em></p>` : ""}
            </div>
        `;
    });

    // Smooth scroll
    box.scrollIntoView({ behavior: "smooth" });
}

renderTaskList();
