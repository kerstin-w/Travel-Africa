const $navbar = $("#navbar");

$(window).on("scroll", function () {
    if ($(window).scrollTop() > 0) {
        $navbar.addClass("navbar-after-scroll");
    } else {
        $navbar.removeClass("navbar-after-scroll");
    }
});

// Get fully year on the footer
$("#year").text(new Date().getFullYear());