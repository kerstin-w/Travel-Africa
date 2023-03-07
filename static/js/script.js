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
    let messages = $('#msg');
    let alert = new bootstrap.Alert(messages);
    alert.close();
}, 2000);