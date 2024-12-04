document.addEventListener('DOMContentLoaded', function() {
    console.log("JavaScript file is linked and working!");

    const deleteModal = document.getElementById("deleteModal");
    if (deleteModal) {
        console.log("Delete modal found");
    } else {
        console.error("Delete modal not found");
    }

    const deleteButtons = document.getElementsByClassName("delete-space");
    console.log("Number of delete buttons:", deleteButtons.length);

    const deleteForm = document.getElementById("deleteForm");
    if (deleteForm) {
        console.log("Delete form found");
    } else {
        console.error("Delete form not found");
    }

    // Original delete modal logic here
});