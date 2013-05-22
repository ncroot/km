function fixTableHeader() {
	var fakeHead = $('.leftpanel > .fakeheader'),
		tabWrap = $('.leftpanel > .tablewrapper');

	fakeHead.find('th').each(function(i) {
		$(this).width(tabWrap.find('thead th').eq(i).width());
	});

	tabWrap.css({
		top : fakeHead.position().top + fakeHead.height() - 1
	});
}

function fixListwrap() {
	var listWrap = $('.rightpanel > .listholder');

	listWrap.css({
		top : 77
	});
}

function openForm() {
	$('#addEventForm').slideDown('fast', function() {
		$('#addEventButt').prop('disabled', true);
	});

	$('.rightpanel > .listholder').animate({
		top : 364
	}, 'fast');
}

function closeForm() {
	$('#addEventForm').slideUp('fast', function() {
		$('#addEventButt').prop('disabled', false);
	});

	$('.rightpanel > .listholder').animate({
		top : 77
	}, 'fast');
}

$(function() {
	$(window).on('load resize', fixTableHeader);

	$('#addEventButt').prop('disabled', false).click(openForm);

	$('#addEventForm button').click(function(e) {
		e.preventDefault();
		closeForm();
	});

	$('.tablewrapper TBODY > TR').click(function() {
		var el = $(this),
			fadespeed = 400;

		if (el.is('.active')) return false;

		el.siblings().removeClass('active').end().addClass('active');

		setTimeout(function() {
			$('.rightpanel > .listholder LI:first-child').appendTo('.rightpanel > .listholder');
		}, fadespeed / 2);

		closeForm();

		$('.rightpanel > H2').animate({
			opacity : 0.1
		}, fadespeed / 2, function() {
			$(this).animate({
				opacity : 1
			}, fadespeed).text(el.find('TD:first-child').text());
		});

		$('.rightpanel > .listholder LI').animate({
			opacity : 0.1
		}, fadespeed / 2, function() {
			$(this).animate({
				opacity : 1
			}, fadespeed);
		});
	});
});