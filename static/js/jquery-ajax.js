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


function openCommentModal(postId, commentId = '', formAction = '') {
    document.getElementById('parentId').value = commentId;
    var form = document.getElementById('commentForm');
    
    if (formAction) {
        form.action = formAction;
    } else {
        form.action = commentId ? 
            document.querySelector(`.open-comment-comment-modal[data-post-id="${postId}"][data-comment-id="${commentId}"]`).getAttribute('data-url') :
            document.querySelector(`.open-post-comment-modal[data-post-id="${postId}"]`).getAttribute('data-url');
    }

    var commentModal = new bootstrap.Modal(document.getElementById('commentModal'));
    commentModal.show();
}


document.querySelectorAll('.open-post-comment-modal').forEach(button => {
    button.addEventListener('click', function() {
        const postId = this.getAttribute('data-post-id');
        openCommentModal(postId, '', this.getAttribute('data-url'));
    });
});


document.querySelectorAll('.open-comment-comment-modal').forEach(button => {
    button.addEventListener('click', function() {
        const postId = this.getAttribute('data-post-id');
        const commentId = this.getAttribute('data-comment-id');
        openCommentModal(postId, commentId, this.getAttribute('data-url'));
    });
});
