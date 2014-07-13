$(function () {
    var slide = $(".header__slide");
    var slideSize = slide.size();
    var slideNavItem = $("<li></li>");
    var slideNav = $(".header__slider__nav");
    var $slider = $(".header__slider"),
        $window = $(window);
    var time = 10000; // промежуток времени,через которое меняются слайды
    if (slideSize > 1) {
        for (var i = 0; i < slideSize; i++) {
            slideNavItem.clone(true).appendTo(slideNav);
        }
        slideNav.find("li").eq(0).addClass("active");
    }

    
    $(".gallery").each(function (index, v) {
        $(this).find('.gal__item').colorbox({rel: 'gallery' + index });
    });
        
    

    function rotate() {
        var parent = $(".header__slider-wrp"),
            slideActive = parent.find(".header__slide.active"),
            index = 0;
        if (!slideActive.next().length == 0) {
            index = slideActive.index() + 1;
        }
        else {
            index = 0;
        }
        var pos = slide.eq(index).position().left;
        parent.find(".header__slide").eq(index).addClass("active");
        slideActive.removeClass("active");
        $slider.animate({
            left: -pos
        });
        $(".header__slider__nav li").removeClass("active").eq(index).addClass("active");

    }

    var autoplay = setInterval(rotate, time);

    $window.resize(function () {
        if ($window.width() > 1000) {
            var slideActive = $(".header__slide.active"),
                index = slideActive.index(),
                width = $(window).width(),
                newPos = width * index;
            $slider.css('left', -newPos)
        }
    });
    $(document).on('click', '.header__slider__nav li', function () {
        var parent = $(this).parents(".header__slider-wrp"),
            slideActive = parent.find(".header__slide.active"),
            index = $(this).index(),
            pos = slide.eq(index).position().left;
        if (!$slider.is(":animated")) {
            if (!$(this).hasClass("active")) {
                clearInterval(autoplay)
                slideActive.removeClass("active");
                parent.find(".header__slide").eq(index).addClass("active");
                $slider.animate({
                    left: -pos
                });
                $(".header__slider__nav li").removeClass("active");
                $(this).addClass("active");
                autoplay = setInterval(rotate, time);
            }
        }
    });


    var navHover = $(".header__nav__hover");
    var navItem = $(".header__nav").find("a");
    var nav = $(".header__nav");
    navItem.on({'mouseover': function () {
        var index = $(this).index();
        setHover(index);
    },
        'click': function () {
            var index = $(this).index();
            navItem.removeClass("active").eq(index).addClass("active");
            setHover(index);
        }});
    nav.on('mouseleave',
        function () {
            var navAct = $(".header__nav a.active");
            var width = navAct.outerWidth();
            var pos = navAct.position().left;
            navHover.animate({
                left: pos
            }).css('width', width);
        });

    function setHover(ind) {
        var width = navItem.eq(ind).outerWidth();
        var pos = navItem.eq(ind).position().left;
        navHover.dequeue().animate({
            left: pos
        }).css('width', width);
    }

    $(".header__search input").on({
        focusin: function () {
            $(".header__search__icon").animate({right: -40})
        },
        focusout: function () {
            $(".header__search__icon").animate({right: -16})
        }
    });


    var $page = $(".container:visible").find(".page");
    $page.eq(0).show();
    var pageSize = $page.size();
    var pageNav = $(".page__nav");
    var pageNavItem = $("<li></li>");
    if (pageSize > 1) {
        for (var i = 0; i < pageSize; i++) {
            pageNavItem.clone(true).appendTo(pageNav);
        }
        pageNav.find("li").eq(0).addClass("active");
    }

    $(document).on('click', '.page__nav li', function () {
        var index = $(this).index();
        $(".page__nav li").removeClass("active").eq(index).addClass("active");
        $page.hide().eq(index).show();
    });

    $(".sidebar a").click(function () {
        $(".sidebar a").removeClass("active");
         $(this).addClass("active");
    })
});