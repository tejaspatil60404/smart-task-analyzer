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

