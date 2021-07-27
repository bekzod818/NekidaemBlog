function userFollowing(e, blogId, status) {
    if (status == 'following') {
        $.ajax({
            url: blogId + '/follow/',
            type: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            dataType: 'json',
            traditional: true,
            success: function (data, textStatus, xhr) {
                if (xhr.status == 200) {
                    window.location.reload();
                }
            }
        });
    } else if (status == 'unfollowing') {
        $.ajax({
            url: blogId + '/unfollow/',
            type: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            dataType: 'json',
            traditional: true,
            success: function (data, textStatus, xhr) {
                if (xhr.status == 200) {
                    window.location.reload()
                }
            }
        });
    }
}