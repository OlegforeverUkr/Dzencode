$(document).ready(function () {
    var notification = $('#notification');
    if (notification.length > 0) {
        setTimeout(function () {
            notification.fadeOut('slow', function () {
                $(this).alert('close');
            });
        }, 5000);
    }

    // Открытие модального окна для комментариев или ответов
    function openCommentModal(postId, commentId = '', formAction = '') {
        document.getElementById('parentId').value = commentId;
        var form = document.getElementById('commentForm');
        
        // Устанавливаем action для формы
        if (formAction) {
            form.action = formAction;
        } else {
            form.action = commentId ? 
                document.querySelector(`.open-comment-comment-modal[data-post-id="${postId}"][data-comment-id="${commentId}"]`).getAttribute('data-url') :
                document.querySelector(`.open-post-comment-modal[data-post-id="${postId}"]`).getAttribute('data-url');
        }

        // Показываем модальное окно
        var commentModal = new bootstrap.Modal(document.getElementById('commentModal'));
        commentModal.show();
    }

    // Обработчики для открытия модального окна для постов
    document.querySelectorAll('.open-post-comment-modal').forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.getAttribute('data-post-id');
            openCommentModal(postId, '', this.getAttribute('data-url'));
        });
    });

    // Обработчики для открытия модального окна для комментариев
    document.querySelectorAll('.open-comment-comment-modal').forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.getAttribute('data-post-id');
            const commentId = this.getAttribute('data-comment-id');
            openCommentModal(postId, commentId, this.getAttribute('data-url'));
        });
    });

    // Обработчики для превью
    $('#preview-comment').on('click', function() {
        let userName = $('#id_user_name').val();
        let email = $('#id_email').val();
        let commentText = $('#id_body').val();

        $('#preview-username').text(userName);
        $('#preview-email').text(email);
        $('#preview-comment-body').html(commentText);

        const imageInput = $('#id_image')[0];
        const fileInput = $('#id_file')[0];
        const imagePreview = $('#preview-image');
        const filePreview = $('#preview-file');

        if (imageInput.files.length > 0) {
            const imageFile = imageInput.files[0];
            const reader = new FileReader();
            reader.onload = function(e) {
                imagePreview.attr('src', e.target.result).show();
            };
            reader.readAsDataURL(imageFile);
        } else {
            imagePreview.hide();
        }

        if (fileInput.files.length > 0) {
            const file = fileInput.files[0];
            filePreview.attr('href', URL.createObjectURL(file)).show();
        } else {
            filePreview.hide();
        }

        $('#previewModal').modal('show');
    });


    // Валидация полей перед отправкой формы
    function validateForm() {
        let isValid = true;
        let errorMessages = '';

        let userName = $('#id_user_name').val();
        if (!userName) {
            isValid = false;
            errorMessages += 'Имя пользователя не должно быть пустым.\n';
        } else if (userName.length < 3) {
            isValid = false;
            errorMessages += 'Имя пользователя должно быть длиннее 3 символов.\n';
        }

        let email = $('#id_email').val();
        if (!email || !validateEmail(email)) {
            isValid = false;
            errorMessages += 'Введите корректный email.\n';
        }

        let commentText = $('#id_body').val();
        if (!commentText) {
            isValid = false;
            errorMessages += 'Текст комментария не должен быть пустым.\n';
        }

        if (!isValid) {
            alert(errorMessages);
        }

        return isValid;
    }

    // Валидация email
    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(String(email).toLowerCase());
    }

    // AJAX отправка формы комментария
    $('#commentForm').on('submit', function(event) {
        event.preventDefault();

        if (!validateForm()) {
            return;
        }

        let formData = new FormData(this);

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                if (response.success) {
                    window.location.reload();
                }
            },
            error: function(xhr) {
                if (xhr.responseJSON && xhr.responseJSON.errors) {
                    let errorMessages = 'Ошибки:\n';
                    for (let field in xhr.responseJSON.errors) {
                        errorMessages += `${xhr.responseJSON.errors[field].join(', ')}\n`;
                    }
                    alert(errorMessages);
            
                    // Обновляем капчу
                    $.get('/captcha/refresh/', function(data) {
                        $('.captcha').attr('src', data.image_url + '?t=' + new Date().getTime());
                        $('#id_captcha_0').val(data.key);
                        $('#id_captcha_1').val('');
                    });
                } else {
                    alert('Произошла ошибка при отправке формы. Пожалуйста, попробуйте еще раз.');
                }
            }
        });
    });


    // Галерея изображений для модального окна
    $('#openGalleryButton').on('click', function () {
        $('#imageGalleryModal').modal('show');

        setTimeout(function () {
            var firstImageLink = $('#lightbox-gallery a').first();
            if (firstImageLink.length) {
                firstImageLink.trigger('click');
            }
        }, 200);
    });

    // Вставка тегов в текст
    function insertTag(tag, isLink = false) {
        var textarea = document.getElementById('id_body');
        var start = textarea.selectionStart;
        var end = textarea.selectionEnd;
        var text = textarea.value;

        if (isLink) {
            var url = prompt("Введите URL ссылки:", "https://");
            var title = prompt("Введите Title для ссылки:", "");
            if (url) {
                var tagContent = `<a href="${url}" title="${title}">${title}</a>`;
                textarea.value = text.substring(0, start) + tagContent + text.substring(end);
            }
        } else {
            textarea.value = text.substring(0, start) + `<${tag}>` + text.substring(start, end) + `</${tag}>` + text.substring(end);
        }

        textarea.focus();
    }

    // Привязываем событие к кнопкам
    $('.btn-group button').on('click', function() {
        var tag = $(this).text().replace(/\[(.*?)\]/, '$1');
        var isLink = tag === 'a';
        insertTag(tag, isLink);
    });
});
