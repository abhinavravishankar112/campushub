// tasks.js - handles toggle and delete with fetch()
document.addEventListener("DOMContentLoaded", () => {
  // toggle
  document.querySelectorAll(".task-toggle").forEach(cb => {
    cb.addEventListener("change", async (e) => {
      const tr = e.target.closest("tr");
      const id = tr.dataset.id;
      try {
        const res = await fetch(`/tasks/toggle/${id}`, { method: "POST" });
        const data = await res.json();
        if (data.success) {
          if (data.completed) {
            tr.classList.add("table-secondary");
          } else {
            tr.classList.remove("table-secondary");
          }
          // Optionally update the progress graph by dispatching an event
          document.dispatchEvent(new CustomEvent("task-changed"));
        } else {
          alert("Could not toggle task.");
        }
      } catch (err) {
        console.error(err);
        alert("Network error.");
      }
    });
  });

  // delete
  document.querySelectorAll(".task-delete").forEach(btn => {
    btn.addEventListener("click", async (e) => {
      const tr = e.target.closest("tr");
      const id = tr.dataset.id;
      if (!confirm("Delete this task?")) return;
      try {
        const res = await fetch(`/tasks/delete/${id}`, { method: "POST" });
        const data = await res.json();
        if (data.success) {
          tr.remove();
          document.dispatchEvent(new CustomEvent("task-changed"));
        } else {
          alert("Could not delete task.");
        }
      } catch (err) {
        console.error(err);
        alert("Network error.");
      }
    });
  });

  // optional: after adding a task via the form, you redirect server-side,
  // so no JS required. But if you want AJAX add, we can add that later.
});
