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

    // Contributor filter
    
    const contributorCheckboxes = document.querySelectorAll('.contributor-filter input[type="checkbox"]');
    const expenseLines = document.querySelectorAll('.accordion-item');

    contributorCheckboxes.forEach(checkbox =>
        checkbox.addEventListener('change', () => filterExpenses())
    );

    function filterExpenses() {
        
        const selectedContributorIds = Array.from(contributorCheckboxes)
            .filter(checkbox => checkbox.checked)
            .map(checkbox => checkbox.id.replace('filter-checkbox-', ''));

        expenseLines.forEach(expenseLine => {
            
            const contributorsInLine = (expenseLine.dataset.contributors || '').split(',').map(id => id.trim());
            const matchesFilter = selectedContributorIds.length === 0 ||
                contributorsInLine.some(id => selectedContributorIds.includes(id));

            expenseLine.style.display = matchesFilter ? '' : 'none';

            if (matchesFilter) filterContributionRows(expenseLine, selectedContributorIds);
        });
    }

    function filterContributionRows(expenseLine, selectedContributorIds) {
        const contributionRows = expenseLine.querySelectorAll('tbody tr[data-contributor-id]');

        contributionRows.forEach(row => {
            const contributorId = row.dataset.contributorId;
            const rowMatches = selectedContributorIds.length === 0 || selectedContributorIds.includes(contributorId);
            row.style.display = rowMatches ? '' : 'none';
        });
    }

});