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
    let liked = localStorage.getItem('liked');
    if (liked) {
        $('.like-button').find('.fa-regular').removeClass('fa-regular').addClass('fa-solid');
    }

    let count = parseInt($('#likes-count').text());

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
                    button.find('.fa-regular').removeClass('fa-regular').addClass('fa-solid');
                    count++;
                    localStorage.setItem('liked', true);
                } else {
                    button.find('.fa-solid').removeClass('fa-solid').addClass('fa-regular');
                    count--;
                    localStorage.removeItem('liked');
                }
                $('#likes-count').text(count);
            }
        });
    });
});