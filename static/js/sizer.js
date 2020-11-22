let button = $('.mobile-nav-button');
let nav_mobile = $('.navigation-mobile');
let nav_mobile_list = $('.navigation-mobile .navigation-list');
let nav = $('.navigation');

button.click( function(e) {
    console.log(e)
    nav_mobile.slideToggle()
})

window.onresize = function(e) {
    check_width()
}

window.onload = function(e) {
    check_width()
}

function check_width() {
    if ( window.innerWidth < 1650 ) {
        console.log(window.innerWidth)
        button.removeClass('d-none');
        nav.removeClass('d-inline-block');
        nav.addClass('d-none');
        nav_mobile.removeClass('d-none');
        nav_mobile.css('display', 'none');
    } else {
        button.addClass('d-none');
        nav.addClass('d-inline-block');
        nav.removeClass('d-none');
        nav_mobile.addClass('d-none');
    }
}