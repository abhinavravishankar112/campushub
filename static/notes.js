document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".note-delete").forEach(btn => {
    btn.addEventListener("click", async (e) => {
      const card = e.target.closest(".card");
      const id = card.dataset.id;

      if (!confirm("Delete this note?")) return;

      try {
        const res = await fetch(`/notes/delete/${id}`, { method: "POST" });
        const data = await res.json();
        if (data.success) {
          card.remove();
        } else {
          alert("Could not delete note.");
        }
      } catch (err) {
        console.error(err);
        alert("Network error.");
      }
    });
  });
});
