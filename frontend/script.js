let tasks = [];

// Adding Task from Form code
function addTask() {
    const title = document.getElementById("title").value;
    const due = document.getElementById("due_date").value;
    const hours = parseFloat(document.getElementById("hours").value);
    const importance = parseInt(document.getElementById("importance").value);
    const deps = document.getElementById("dependencies").value
        .split(",")
        .map(d => d.trim())
        .filter(d => d !== "")
        .map(d => parseInt(d));

    const newTask = {
        id: tasks.length + 1,
        title: title,
        due_date: due,
        estimated_hours: hours,
        importance: importance,
        dependencies: deps
    };

    tasks.push(newTask);
    alert("Task added!");
}

//Analyze tasks
function analyzeTasks() {
    // if user pasted custom JSON
    let jsonText = document.getElementById("jsonInput").value;
    if (jsonText.trim() !== "") {
        try {
            tasks = JSON.parse(jsonText);
        } catch {
            alert("Invalid JSON!");
            return;
        }
    }

    fetch("http://127.0.0.1:8000/api/tasks/analyze/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(tasks)
    })
    .then(res => res.json())
    .then(data => displayResults(data))
    .catch(err => alert("Error: " + err));
}

// suggest tasks
function suggestTasks() {
    let jsonText = document.getElementById("jsonInput").value;
    if (jsonText.trim() !== "") {
        try {
            tasks = JSON.parse(jsonText);
        } catch {
            alert("Invalid JSON!");
            return;
        }
    }

    fetch("http://127.0.0.1:8000/api/tasks/suggest/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(tasks)
    })
    .then(res => res.json())
    .then(data => displayResults(data))
    .catch(err => alert("Error: " + err));
}

//displaying results functions
function displayResults(data) {
    const container = document.getElementById("results");
    container.innerHTML = "";

    data.forEach(task => {
        let priorityClass =
            task.score >= 25 ? "high" :
            task.score >= 15 ? "medium" : "low";

        container.innerHTML += `
            <div class="task-card ${priorityClass}">
                <h3>${task.title}</h3>
                <p><strong>Score:</strong> ${task.score}</p>
                <p><strong>Reason:</strong> ${task.reason}</p>
                ${task.suggest_reason ? `<p><strong>Suggest:</strong> ${task.suggest_reason}</p>` : ""}
            </div>
        `;
    });
    document.getElementById("results").scrollIntoView({ behavior: "smooth" });
}