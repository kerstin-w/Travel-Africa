// Navbar on scroll
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

//Toggle Heart Icon for Likes
$(document).ready(function () {
    const likeButton = $('.like-button');
    const likesCount = $('#likes-count');
    let count = parseInt(likesCount.text());
    let liked = localStorage.getItem('liked');

    if (liked) {
        likeButton.find('.fa-regular').removeClass('fa-regular').addClass('fa-solid');
    }

    likeButton.click(function (event) {
        event.preventDefault();
        const button = $(this);
        const postSlug = button.data('post-slug');
        const token = $('input[name="csrfmiddlewaretoken"]').val();

        $.ajax({
            url: `/post/${postSlug}/like/`,
            type: 'POST',
            data: {
                csrfmiddlewaretoken: token
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
                likesCount.text(count);
            }
        });
    });
});