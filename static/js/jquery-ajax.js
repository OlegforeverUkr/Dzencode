$(document).ready(function () {
    var notification = $('#notification');

    if (notification.length > 0) {
        setTimeout(function () {
            notification.fadeOut('slow', function () {
                $(this).alert('close');
            });
        }, 5000);
    }
});
