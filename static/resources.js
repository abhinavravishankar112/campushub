document.addEventListener("DOMContentLoaded", () => {

  // Handle status change
  document.querySelectorAll(".resource-status").forEach(select => {
    select.addEventListener("change", async (e) => {
      const tr = e.target.closest("tr");
      const id = tr.dataset.id;
      const status = e.target.value;

      try {
        const res = await fetch(`/resources/update/${id}`, {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: `status=${encodeURIComponent(status)}`
        });

        const data = await res.json();
        if (!data.success) alert("Failed to update status.");
      } catch (err) {
        console.error(err);
        alert("Network error.");
      }
    });
  });

  // Handle delete
  document.querySelectorAll(".resource-delete").forEach(btn => {
    btn.addEventListener("click", async (e) => {
      const tr = e.target.closest("tr");
      const id = tr.dataset.id;

      if (!confirm("Delete this resource?")) return;

      try {
        const res = await fetch(`/resources/delete/${id}`, { method: "POST" });
        const data = await res.json();

        if (data.success) tr.remove();
      } catch (err) {
        console.error(err);
        alert("Network error.");
      }
    });
  });
});
