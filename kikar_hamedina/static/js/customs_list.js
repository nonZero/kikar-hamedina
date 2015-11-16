$(document).ready(function () {

    // Event: click save query button to open modal-dialog form
    $('.delete-query-btn').click(function () {
        $('#delete-query-form-title').attr('value', $(this).data('title'));

    });


    // event: submit save query modal-dialog form
    $('#delete-query-submit-form-btn').click(function () {
        var titleInput = $('#delete-query-form-title');
        titleInput.removeAttr('disabled');
        $.ajax({
            url: '/custom/delete/',
            type: 'post',
            dataType: 'json',
            data: $('form#delete-query-form').serialize(),
            success: function (data) {
                console.log(data);
                $('#delete-query-status-message').html('Query Saved Successfuly!');
                $('#query-row-' + titleInput.val()).hide();
                $('#delete-query-submit-form-btn').attr('disabled', 'disabled');
                titleInput.attr('disabled', 'disabled');
            },
            error: function (data) {
                console.log(data)
            }
        });

    });
});