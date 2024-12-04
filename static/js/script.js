document.addEventListener('DOMContentLoaded', function() {
    console.log("JavaScript file is linked and working!");

    // Initialize the delete modal only when DOM is ready
    const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
    const deleteButtons = document.getElementsByClassName("delete-space");
    const deleteForm = document.getElementById("deleteForm");

    if (deleteButtons.length > 0 && deleteForm) {
        for (let button of deleteButtons) {
            button.addEventListener("click", (e) => {
                e.preventDefault(); // Prevent default link behavior
                let spaceId = button.getAttribute("data-space-id");
                console.log("Space ID:", spaceId); 
                deleteForm.action = `/delete_space/${spaceId}/`; 
                console.log("Form Action:", deleteForm.action); 
                deleteModal.show();
            });
        }
    } else {
        console.error("Delete buttons or form not found in the DOM.");
    }
});