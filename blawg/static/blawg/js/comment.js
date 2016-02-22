var original_comment;
function cancel_typing() {
    $('.cancelreply').children().text(reply);
    $('.cancelreply').attr('class', 'reply');
    $('.canceledit').children().text(edit);
    $('.canceledit').attr('class', 'edit');
    $('.replyform').hide(400, function () {
        $(this).remove();
    });
    var edit_form = $('.editform');
    if (edit_form.length) {
        var div = $('<div>');
        div.attr('class', 'commentcontent');
        div.html(original_comment);
        var header = edit_form.prev();
        edit_form.hide(400, function () {
            $(this).remove();
            header.after(div);
        });
    }
}
function create_item(comment_div, label, style) {
    var a = $('<a>');
    a.attr('href', '');
    a.text(label);
    var action_p = $('<p>');
    action_p.attr('class', style);
    action_p.append(a);
    comment_div.append(action_p);
}
$(function () {
    var name_span = null;
    var stored_name = '';
    $('#blawg').on('click', '.reply', function () {
        cancel_typing();
        $(this).attr('class', 'cancel cancelreply');
        $(this).children().text(cancel);
        var text_area = $('<textarea>');
        var comment_button = $('<button>');
        comment_button.text(reply);
        var form_div = $('<div>');
        form_div.attr('class', 'form replyform');
        if (guest) {
            var label = $('<label>');
            label.attr('for', 'replyname');
            label.text(name_word);
            var input = $('<input>');
            input.attr('type', 'text');
            input.attr('id', 'replyname');
            input.attr('class', 'replyname');
            input.val(stored_name);
            var p = $('<p>');
            p.attr('class', 'name');
            p.append(label);
            p.append(input);
            form_div.append(p);
        }
        form_div.append(text_area);
        form_div.append(comment_button);
        form_div.hide();
        $(this).after(form_div);
        form_div.show(400);
        return false;
    });
    $('#blawg').on('click', '.commentform button, .replyform button', function () {
        var form_div = $(this).parent();
        var name = form_div.find('input').val();
        var content_area = form_div.find('textarea');
        var content = content_area.val();
        if (guest && name.length > max_length) {
            return alert(max_length_warning);
        }
        if (!content) {
            return alert(empty_content_warning);
        }
        var parent = null;
        var ancestor = form_div.parent();
        if (ancestor.attr('class') == 'comment') {
            parent = ancestor.find('[type="hidden"]').val();
        }
        $.ajax({
            method: 'post',
            url: create_url,
            data: {
                entry: entry,
                parent: parent,
                guest_name: name,
                content: content
            },
            headers: {
                'X-CSRFToken': Cookies.get('csrftoken')
            },
            success: function (data) {
                cancel_typing();
                if (!name_span) {
                    name_span = $('<span>');
                    if (guest) {
                        if (name) {
                            name_span.attr('class', 'commentname');
                            name_span.text(name);
                        }
                        else {
                            name_span.attr('class', 'anonymous');
                            name_span.text(anonymous);
                        }
                    }
                    else {
                        var a = $('<a>');
                        a.attr('href', user_url);
                        a.text(user);
                        name_span.attr('class', 'commentname');
                        name_span.append(a);
                    }
                }
                var date_span = $('<span>');
                date_span.attr('class', 'commentdate');
                date_span.text(data['created']);
                var p = $('<p>');
                p.attr('class', 'header');
                p.append(name_span);
                p.append(date_span);
                var div = $('<div>');
                div.attr('class', 'commentcontent');
                div.html(content.replace(/(?:\r\n|\r|\n)/g, '<br />'));
                var a = $('<a>');
                a.attr('href', '');
                a.text(reply);
                var action_p = $('<p>');
                action_p.attr('class', 'reply');
                action_p.append(a);
                var input = $('<input>');
                input.attr('type', 'hidden');
                input.val(data['pk']);
                var comment_div = $('<div>');
                comment_div.attr('class', 'comment');
                comment_div.append(p);
                comment_div.append(div);
                comment_div.append(action_p);
                if (!guest) {
                    create_item(comment_div, edit, 'edit');
                    create_item(comment_div, del, 'delete');
                }
                comment_div.append(input);
                comment_div.hide();
                if (ancestor.attr('class') == 'comment') {
                    var children_div = ancestor.find('[class="children"]');
                    if (!children_div.length) {
                        children_div = $('<div>');
                        children_div.attr('class', 'children');
                        ancestor.after(children_div);
                    }
                    children_div.prepend(comment_div);
                }
                else {
                    $('h3').after(comment_div);
                }
                comment_div.show(400);
                content_area.val('');
                stored_name = name;
            },
            error: function () {
                alert(comment_creation_failed);
            }
        });
    });
    $('#blawg').on('click', '.edit', function () {
        cancel_typing();
        $(this).attr('class', 'cancel canceledit');
        $(this).children().text(cancel);
        var par = $(this).parent();
        var content_div = par.find('.commentcontent');
        original_comment = content_div.html();
        var content = original_comment.replace(/<br>/g, '\n');
        var text_area = $('<textarea>');
        text_area.text(content);
        var save_button = $('<button>');
        save_button.text(save);
        var form_div = $('<div>');
        form_div.attr('class', 'form editform');
        form_div.append(text_area);
        form_div.append(save_button);
        form_div.hide();
        par.find(':first').after(form_div);
        content_div.remove();
        form_div.show(400);
        return false;
    });
    $('#blawg').on('click', '.editform button', function () {
        var form_div = $(this).parent();
        var comment_div = form_div.parent();
        var content = form_div.find('textarea').val();
        if (!content) {
            return alert(empty_content_warning);
        }
        $.ajax({
            method: 'post',
            url: update_url,
            data: {
                pk: comment_div.find('[type="hidden"]').val(),
                content: content
            },
            headers: {
                'X-CSRFToken': Cookies.get('csrftoken')
            },
            success: function (data) {
                comment_div.find('.edited').remove();
                var div = $('<div>');
                div.attr('class', 'commentcontent');
                div.html(content.replace(/(?:\r\n|\r|\n)/g, '<br />'));
                div.hide();
                var p = $('<p>');
                p.attr('class', 'edited');
                p.text(edited + ' ' + data['modified']);
                p.hide();
                form_div.after(div);
                div.after(p);
                var cancel = comment_div.find('.cancel');
                form_div.hide(400, function () {
                    div.show();
                    p.show();
                    cancel.attr('class', 'edit');
                    cancel.find('a').text(edit);
                    $(this).remove();
                });
            },
            error: function () {
                alert(comment_update_failed);
            }
        });
    });
    $('#blawg').on('click', '.cancel', function () {
        cancel_typing();
        return false;
    });
    $('#blawg').on('click', '.delete', function () {
        if (confirm(delete_confirmation)) {
            var parent_div = $(this).parent();
            $.ajax({
                method: 'post',
                url: delete_url,
                data: {
                    pk: parent_div.find('[type="hidden"]').val()
                },
                headers: {
                    'X-CSRFToken': Cookies.get('csrftoken')
                },
                success: function () {
                    var grand_div = parent_div.parent();
                    grand_div.hide(400, function () {
                        grand_div.remove();
                    });
                },
                error: function () {
                    alert(comment_delete_failed);
                }
            });
        }
        return false;
    });
});
