document.addEventListener('DOMContentLoaded', function() {
    const datePicker = document.getElementById('date');
    const today = new Date().toISOString().split('T')[0];
    datePicker.min = today;
  });