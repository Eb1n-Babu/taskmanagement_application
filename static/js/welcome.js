document.addEventListener('DOMContentLoaded', function() {
    var modal = new bootstrap.Modal(document.getElementById('devNoteModal'), {
        backdrop: 'static',
        keyboard: false
    });
    modal.show();

    // Auto-close after 15 seconds
    setTimeout(function() {
        modal.hide();
    }, 20000);
});