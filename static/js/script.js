// Tool Tips
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
[...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));

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


// Change Icon for Bucket List
const addToBucketListForm = $('#add-to-bucketlist-form');

addToBucketListForm.submit(function (event) {
    event.preventDefault();
    const bucketListButton = $('#add-to-bucketlist-button');
    const bucketListButtonText = $('#bucket-list-text');

    $.ajax({
        url: $(this).attr('action'),
        method: 'POST',
        data: $(this).serialize(),
        success: function () {
            bucketListButton.removeClass('btn-save').addClass('btn-success');
            bucketListButtonText.html('<i class="fa-solid fa-check"></i>&nbsp;Added');
        },
        error: function () {
            alert('Failed to add post to bucket list');
        }
    });
});


$(document).ready(function () {
    //Toggle Heart Icon for Likes
    const likeButton = $('.like-button');
    const likesCount = $('#likes-count');
    let count = parseInt(likesCount.text());
    let liked = likeButton.attr('data-liked') === 'true';

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

    // Toogle between Posts and Comments on Profile
    $("#collapsePostsButton").click(function () {
        if (!$("#collapsePosts").hasClass("show")) {
            $("#collapsePosts").removeClass("show");
            $("#collapseComments").removeClass("show");
        }
    });

    $("#collapseCommentsButton").click(function () {
        if (!$("#collapseComments").hasClass("show")) {
            $("#collapseComments").removeClass("show");
            $("#collapsePosts").removeClass("show");
        }
    });
});