/*global $, document, Chart, LINECHART, data, options, window, setTimeout*/
$(document).ready(function () {
nextSlide(slideOrder)
    'use strict';

    // ------------------------------------------------------- //
    // For demo purposes only
    // ------------------------------------------------------ //

    var stylesheet = $('link#theme-stylesheet');
    $( "<link id='new-stylesheet' rel='stylesheet'>" ).insertAfter(stylesheet);
    var alternateColour = $('link#new-stylesheet');

    if ($.cookie("theme_csspath")) {
        alternateColour.attr("href", $.cookie("theme_csspath"));
    }

    $("#colour").change(function () {

        if ($(this).val() !== '') {

            var theme_csspath = 'css/style.' + $(this).val() + '.css';

            alternateColour.attr("href", theme_csspath);

            $.cookie("theme_csspath", theme_csspath, { expires: 365, path: document.URL.substr(0, document.URL.lastIndexOf('/')) });

        }

        return false;
    });


    // ------------------------------------------------------- //
    // Equalixe height
    // ------------------------------------------------------ //
    function equalizeHeight(x, y) {
        var textHeight = $(x).height();
        $(y).css('min-height', textHeight);
    }
    equalizeHeight('.featured-posts .text', '.featured-posts .image');

    $(window).resize(function () {
        equalizeHeight('.featured-posts .text', '.featured-posts .image');
    });


    // ---------------------------------------------- //
    // Preventing URL update on navigation link click
    // ---------------------------------------------- //
    $('.link-scroll').bind('click', function (e) {
        var anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $(anchor.attr('href')).offset().top + 2
        }, 700);
        e.preventDefault();
    });


    // ---------------------------------------------- //
    // FancyBox
    // ---------------------------------------------- //
    $("[data-fancybox]").fancybox();


    // ---------------------------------------------- //
    // Divider Section Parallax Background
    // ---------------------------------------------- //
    $(window).on('scroll', function () {

        var scroll = $(this).scrollTop();

        if ($(window).width() > 1250) {
            $('section.divider').css({
                'background-position': 'left -' + scroll / 8 + 'px'
            });
        } else {
            $('section.divider').css({
                'background-position': 'center bottom'
            });
        }
    });


    // ---------------------------------------------- //
    // Search Bar
    // ---------------------------------------------- //
    $('.search-btn').on('click', function (e) {
        e.preventDefault();
        $('.search-area').fadeIn();
    });
    $('.search-area .close-btn').on('click', function () {
        $('.search-area').fadeOut();
    });



    // ---------------------------------------------- //
    // Navbar Toggle Button
    // ---------------------------------------------- //
    $('.navbar-toggler').on('click', function () {
        $('.navbar-toggler').toggleClass('active');
    });

});

// The current slide
var slideOrder = 0;

// Pause between slides in miliseconds
var slidePause = 8000;

// The slides array
var slides = $(".card-decks .card-deck");

// $(document).ready(function(){
//
// })

function autoSlide(){
	autoSlideTimeout = setTimeout(function() {

		// Check if the slideOrder is not bigger
		// than the available amount of slides
		if(slides.length <= slideOrder){
			slideOrder = 0;
		}

		// Give us the next slide
		nextSlide(slideOrder);


		slideOrder++;
	}, slidePause);
}

function theDelay(index){
	// Maybe a bit dirty but we need to get the exact
	// pause between all the slides and we dont want a
	// point in the variable because of css
	var delay = (0.2 * index)
	var delayClass = parseInt(delay.toString().replace(".", ""));

	return "0" + delayClass
}

function nextSlide(deck){
	//	Find the current active deck
	var currentDeck = slides.closest(".deck-active")
	var currentCards = currentDeck.find(".card");

	// Find the target deck we want to load in
	var nextDeck = slides.eq(deck);

	currentCards.each(function(index){
		var delay = theDelay(index);
		var card =$(this)
		// Remove all the animate.css classess
		card.removeClass().attr('class', 'card');



		card.addClass("animated flipOutY fast delay-" + delay + "s");
		setTimeout(function(){
			card.find(".card-img-overlay").fadeOut();
			card.find(".card-img").removeAttr('style');
		}, ((delay + 8) * 50))


	});

	//	Animate.css class "fast" is timed for 0.8s
	//	we delay each CARD (not card-deck) intro by 0.2s
	// so 0.8 + 0.2 = 1s
	//
	// 1 times each card without the first one * 1000
	// = the amount of seconds we have to wait before the new
	// we end this function
	//
	// I didn't remove the 1 because of the explanation
	var timeout = ((1 * (currentCards.length - 1)) * 1000)

	setTimeout(function(){
		if(nextDeck.length){
			// Hide the current deck so the new deck
			// gets the right position then clean the
			// current deck
			currentDeck.removeClass("deck-active");
			currentDeck.find(".card").each(function(){
				$(this).removeClass().attr('class', 'card');
			})

			nextDeck.find(".card").each(function(index){
				var delay = theDelay(index);

				var card = $(this);
				setTimeout(function(){
					card.find(".card-img-overlay").stop().fadeIn();
					card.find(".card-img").animate({height: '110%', width: '110%'}, {duration:(slidePause / 2), easing: 'swing', queue: false });

				}, ((delay + 8) * 10))
				card.addClass("animated flipInY fast delay-" + delay + "s");




			})
			nextDeck.addClass("deck-active");
			autoSlide();
		}else{
			// Try to reset the process
			console.error("Card flipper, did not find the target deck. Did you remove it?")
			slideOrder = 0;
			autoSlide();
		}

	}, timeout)
}
