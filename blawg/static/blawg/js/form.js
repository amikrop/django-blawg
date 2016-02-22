$(function () {
    $('#public').change(function () {
        if (!$(this).prop('checked')) {
            $('#allow_comments').prop('checked', false);
        }
    });
    $('#allow_comments').change(function () {
        if ($(this).prop('checked')) {
            $('#public').prop('checked', true);
        }
        else {
            $('#allow_anonymous_comments').prop('checked', false);
        }
    })
    $('#allow_anonymous_comments').change(function () {
        if ($(this).prop('checked')) {
            $('#allow_comments').prop('checked', true);
        }
    })
});
