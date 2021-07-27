function postMarkAsRead(e, postId) {
    $.ajax({
        url: postId + '/mark_as_read/',
        type: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        data: {
            'post_id': postId,
        },
        dataType: 'json',
        traditional: true,
        success: function (data, textStatus, xhr) {
            if (xhr.status == 200) {
                window.location.reload()
            }
        }
    });
}