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
	
	$('#companylist TBODY').on('click', 'A', function(e) {
		e.stopPropagation();
	});

	$('#companylist TBODY').on('click', '> TR', function(e) {
		var el = $(this),
			fadespeed = 200;

		if (el.is('.active')) return false;
		
		el.siblings().removeClass('active').end().addClass('active');

		setTimeout(function() {
			$('.rightpanel > .listholder LI:first-child').appendTo('.rightpanel > .listholder');
		}, fadespeed / 2);

		closeForm();

		$('.rightpanel > H2').animate({
			opacity : 0.3
		}, fadespeed / 2, function() {
			$(this).animate({
				opacity : 1
			}, fadespeed).text(el.find('TD:first-child').text());
		});

		$('.rightpanel > .listholder LI').animate({
			opacity : 0.3
		}, fadespeed / 2, function() {
			$(this).animate({
				opacity : 1
			}, fadespeed);
		});
	});
	
	$.hiddenElems = $('.leftpanel > .fakeheader, .leftpanel > .tablewrapper, .rightpanel > H2, .rightpanel > .listholder').css({ opacity : 0 });
	
	$.getCompanyList(drawList);
	
	myTitle('#companylist');
});

$.companyList = null;
$.hiddenElems = null;

$.getCompanyList = function(callback) {
	$.ajax({
		url: '/core/customer-list-json',
		dataType: 'json',
		cache: false,
		success: function(data) {
			$.companyList = data.object_list;
			if ($.type(callback) == 'function') callback();
		}
	});
};

function drawList() {
	if ($.companyList) {
		var tbody  = $('#companylist > TBODY');
		
		tbody.empty();
		
		for (k in $.companyList) {
			var c = $.companyList[k].fields,
				c_city,
				c_url = c.url ? '<a href="http://'+c.url+'" title="'+c.url+'" target="_blank">url</a>' : '—';
			
			switch(c.city) {
				case 1:
					c_city = 'Москва';
				break;
				
				case null:
					c_city = '—';
				break;
				
				default:
					c_city = c.city;
				break;
			}
			
			tbody.append('<tr><td title="'+c.branch_description+'">'+c.name+'</td><td>'+c_city+'</td><td>'+c.company_size+'</td><td>'+c_url+'</td></tr>');
			
			console.log(c);
		}
		
		tbody.find('> TR:first-child').trigger('click');
		
		fixTableHeader();
		
		$.hiddenElems.animate({ opacity : 1 });
	}
}

function myTitle(el) {
	$.label = $('<div class="myLabel" />').appendTo('body');
	
	$(el).hoverIntent({
		over: showTitle,
		out : hideTitle,
		selector: 'TD'
	});
	
	$(window).mousemove(function(e) {
		$.label.css({
			left : e.clientX + 12,
			top  : e.clientY + 14
		});
	});
}

function showTitle() {
	var el = $(this);
	if (el.prop('title')) {
		el.attr( 'data-title', el.attr('title') ).attr('title', '');
		$.label.text( el.attr( 'data-title') ).fadeIn('fast');
	}
}

function hideTitle() {
	var el = $(this);
	el.attr( 'title', el.attr('data-title') ).attr('data-title', '');
	$.label.fadeOut('fast');
}






























