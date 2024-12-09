document.addEventListener("DOMContentLoaded", function () {
    const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
    const deleteButtons = document.getElementsByClassName("delete-space");
    const deleteForm = document.getElementById("deleteForm");

    for (let button of deleteButtons) {
        button.addEventListener("click", (e) => {
            let spaceId = button.getAttribute("data-space-id");
            console.log("Space ID:", spaceId);
            deleteForm.action = `/delete_space/${spaceId}/`;
            console.log("Form Action:", deleteForm.action);
            deleteModal.show();
        });
    }

    // Set django messages to fade out after 3 seconds

    const messages = document.querySelectorAll('#message-container .alert');
    messages.forEach((message) => {
        setTimeout(() => {
            message.classList.remove('show');
            message.style = `transition: opacity 1s ease;
                                      opacity: 0;
                                      `
            setTimeout(() => message.remove(), 500); 
        }, 3000); 
    });

    // Toggle expense line accordion dropdown

    const toggleButton = document.getElementById('toggleButton');
    const panels = document.querySelectorAll('.accordion-panel');

    let status = false;

    toggleButton.addEventListener('click', function () {
        panels.forEach(panel => {
            if (status) {
                panel.classList.remove('show');
            } else {
                panel.classList.add('show');
            }
        });

        status = !status;
        toggleButton.textContent = status ? 'Collapse All' : 'Show All';
    });

});