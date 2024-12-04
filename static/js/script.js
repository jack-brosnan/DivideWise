document.addEventListener("DOMContentLoaded", function () {
    // Delete modal logic
    const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
    const deleteButtons = document.getElementsByClassName("delete-space");
    const deleteForm = document.getElementById("deleteForm");

    if (deleteButtons.length > 0 && deleteForm) {
        for (let button of deleteButtons) {
            button.addEventListener("click", (e) => {
                e.preventDefault();
                let spaceId = button.getAttribute("data-space-id");
                deleteForm.action = `/delete_space/${spaceId}/`;
                console.log("Form Action:", deleteForm.action);
                deleteModal.show();
            });
        }
    } else {
        console.error("Delete buttons or form not found in the DOM.");
    }

    // Django messages timeout after 3 secons
    setTimeout(function () {
        const messageContainer = document.getElementById('message-container');
        if (messageContainer) {
            messageContainer.style = `transition: opacity 1s ease;
                                      opacity: 0;
                                      `
            setTimeout(() => {
                messageContainer.remove();
            }, 1000);
        }
    }, 3000);
});