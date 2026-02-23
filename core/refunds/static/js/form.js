document.addEventListener("DOMContentLoaded", () => {

    const sections = document.querySelectorAll(".card[id]");
    const sidebarLinks = document.querySelectorAll(".nav-link-section");

    function isFilled(field) {
        if (field.type === "checkbox" || field.type === "radio") {
            return field.checked;
        }
        return field.value && field.value.trim() !== "";
    }

    function validateSection(section) {
        const requiredFields = section.querySelectorAll(
            "input[required], select[required], textarea[required]"
        );

        if (requiredFields.length === 0) return true;

        return Array.from(requiredFields).every(isFilled);
    }

    function updateUI() {
        sections.forEach(section => {
            const sectionId = section.id;
            const sidebarLink = document.querySelector(
                `.nav-link-section[data-section="${sectionId}"]`
            );

            if (!sidebarLink) return;

            const completed = validateSection(section);

            section.classList.toggle("section-complete", completed);
            sidebarLink.classList.toggle("completed", completed);
        });
    }

    function showSection(sectionId) {
        sections.forEach(section => {
            section.style.display = section.id === sectionId ? "block" : "none";
        });
    }

    // Add click handlers for sidebar links
    sidebarLinks.forEach(link => {
        link.addEventListener("click", (e) => {
            e.preventDefault();
            const targetSectionId = link.getAttribute("data-section");
            showSection(targetSectionId);
        });
    });

    // Initial check and show first section
    updateUI();
    if (sections.length > 0) {
        showSection(sections[0].id);
    }

    // Live updates
    document.addEventListener("input", updateUI);
    document.addEventListener("change", updateUI);
});