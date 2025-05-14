document.addEventListener('DOMContentLoaded', () => {
    const checkboxes = document.querySelectorAll('.character-select');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            const characterId = parseInt(checkbox.getAttribute('data-id'));
            const toggleUrl = checkbox.getAttribute('data-toggle-url').replace('0', characterId);
            fetch(toggleUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    console.log(`Character ${characterId} selection updated: ${data.selected}`);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});