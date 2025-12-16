// dashboard.js
let taskChart = null;

async function fetchProgressData() {
  const res = await fetch("/progress-data");
  if (!res.ok) throw new Error("Failed to load progress data");
  return res.json();
}

function renderChart(labels, values) {
  const ctx = document.getElementById("taskProgressChart").getContext("2d");

  if (taskChart) {
    taskChart.data.labels = labels;
    taskChart.data.datasets[0].data = values;
    taskChart.update();
    return;
  }

  taskChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [{
        label: "Tasks completed",
        data: values,
        fill: true,
        tension: 0.3,
        borderWidth: 2,
        pointRadius: 3
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
          ticks: { stepSize: 1 }
        }
      },
      plugins: {
        legend: { display: false }
      }
    }
  });
}

async function refreshDashboard() {
  try {
    const d = await fetchProgressData();
    renderChart(d.labels, d.values);

    // optional quick stats
    const total = d.values.reduce((a,b)=>a+b,0);
    document.getElementById("quick-stats").textContent = `Tasks completed in 14 days: ${total}`;
  } catch (err) {
    console.error(err);
  }
}

// initial load
document.addEventListener("DOMContentLoaded", refreshDashboard);

// update whenever tasks change (tasks.js dispatches 'task-changed')
document.addEventListener("task-changed", refreshDashboard);
