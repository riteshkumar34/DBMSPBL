// Ensure the form is submitted correctly
document.querySelector('form').addEventListener('submit', function(event) {
    const name = document.querySelector('input[name="name"]').value;
    const amount = document.querySelector('input[name="amount"]').value;
    const category = document.querySelector('select[name="category"]').value;

    // Validate fields to ensure that user inputs are not empty or invalid
    if (!name || !amount || isNaN(amount) || amount <= 0) {
        alert("Please enter a valid expense name and amount.");
        event.preventDefault(); // Prevent form submission if validation fails
    }
});
