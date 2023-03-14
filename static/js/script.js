const $navbar = $("#navbar");

$(window).on("scroll", function () {
    if ($(window).scrollTop() > 0) {
        $navbar.addClass("navbar-after-scroll");
    } else {
        $navbar.removeClass("navbar-after-scroll");
    }
});

// Get full year on the footer
$("#year").text(new Date().getFullYear());

//Set Time Out for alert messages
setTimeout(function () {
    $('#msg').alert('close');
}, 4000);

//Toogle Heart Icon for Likes
$(document).ready(function () {

    $('.like-button').click(function (event) {
        event.preventDefault();
        let button = $(this);
        let postSlug = button.data('post-slug');
        $.ajax({
            url: '/post/' + postSlug + '/like/',
            type: 'POST',
            data: {
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            dataType: 'json',
            success: function (data) {
                if (data.liked) {
                    button.text('Unlike');
                } else {
                    button.text('Like');
                }
                $('#likes-count').text(data.count + ' likes');
            }
        });
    });
});