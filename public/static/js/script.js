$(function() {
	$.hiddenElems = $('.body .leftpanel > *, .body .rightpanel > *').not('.body .rightpanel > .btn').css({
		opacity : 0,
		visibility : 'hidden'
	});
	
	$(window).on('load resize', function() {
		fixHeight();
	});
	
	$(document).on('click', 'A[href=#]', false);

	$('#addEventButt').prop('disabled', false).click(openForm);

	$('#addEventForm button').click(function(e) {
		e.preventDefault();
		closeForm();
	});
	
	$.getCompanyList(drawList);
	
	myTitle('.mytitle');
	
	var cInfo = $('#cInfo');
		cPersons = $('#cPersons'),
		cPP = $('#cPP'),
		cEv = $('#cevents');
	
	cInfo.off('click').on('click', 'BUTTON', function() {
		var el = $('DL.hidden', cInfo),
			direction = $(this).is('.dropup') ? -1 : 1;
		if ( el.is(':animated') ) return false;
		fixHeight( el.height() * direction );
		el.slideToggle();
		$(this).toggleClass('dropup');
	});
	
	cPersons.off('click').on('click', 'BUTTON', function() {
		var el = $('.pInfo', cPersons),
			direction = $(this).is('.dropup') ? -1 : 1;
		if ( el.is(':animated') ) return false;
		fixHeight( el.height() * direction );
		el.slideToggle();
		$(this).toggleClass('dropup');
	});
	
	cPP.off('click').on('click', 'DT .btn', function() {
		var el = $(this),
			cLass = el.attr('rel');
		
		cEv.fadeOut('fast', function() {
			cEv.fadeIn('fast').find('LI').hide().removeClass('selected').filter('LI.' + cLass).addClass('selected').show();
			cEv.next().fadeIn('fast');
			el.closest('LI').addClass('selected');
		});
		
		cPP.find('LI').removeClass('selected');
	});
	
	cEv.next().click(function() {
		cEv.fadeOut('fast', function(){
			cEv.fadeIn('fast').find('LI').removeClass('selected').show();
			cEv.next().fadeOut('fast');
			cPP.find('LI').removeClass('selected');
		});
	});
});

$.companyList = null;
$.propersList = null;

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

$.getPropersList = function(id, callback) {
	$.ajax({
		//url: '/core/pp_' + id + '.json',
		url: '/static/pp.json',
		dataType: 'json',
		cache: false,
		success: function(data) {
			$.propersList = data;
			if ($.type(callback) == 'function') callback();
		},
		error: function() {
			$.propersList = null;
			if ($.type(callback) == 'function') callback(true);
		}
	});
};

function setHash(id) {
	if (id) window.location.hash = 'id:' + id;
}

function drawList() {
	if ($.companyList) {
		var aside = $('#aside > UL'),
			cList = [];
		
		aside.empty();
		
		for (k in $.companyList) {
			var c = $.companyList[k].fields,
				pk = $.companyList[k].pk;
			
			aside.append('<li data-rel="bar_' + pk + '" class="mytitle" title="' + c.branch_description + '">' + c.name + '</li>');
			
			cList.push({
				"id" : pk,
				"name" : c.name,
				"size" : c.company_size,
				"description" : c.branch_description,
				"value" : [c.name],
				"tokens" : [c.name, c.name_lat]
			});
		}
		
		$('#cList').typeahead({
			name: 'cList',
			local: cList,
			template: [
				'<p class="c-size">размер: {{size}}</p>',
				'<p class="c-name">{{name}}</p>',
				'<p class="c-description">{{description}}</p>'
			].join(''),
			engine: Hogan,
			limit: 100
		}).on('typeahead:opened', function($e) {
			
		}).on('typeahead:selected', function($e, datum) {
			setHash( datum.id );
		}).on('typeahead:autocompleted', function($e, datum) {
			setHash( datum.id );
		}).on('typeahead:suggestionRendered', function($e, datum) {
			/*$('.tt-dropdown-menu .c-name').each(function() {
				var fword = $(this).text().split(' ')[0],
					lword = $(this).text().split(fword)[1];
				$(this).html( highlight(fword) + lword );
			});*/
		});
		
		aside.off('click').on('click', 'LI', function() {
			if ( $('.blink').length ) return false;
			setHash( $(this).data('rel').split('bar_')[1] );
		});
		
		$.router(/^id:(\d+)$/, function(m, id) {
			//console.log( id );
			panelOperation( getCompany(id) );
		});
		
		if (!window.location.hash) setHash( 63 );
	}
}

function drawProPerEv(error) {
	var per = $('#cPersons .pInfo'),
		pro = $('#cPP .listholder'),
		cEv = $('#cevents');
	
	per.empty();
	pro.empty();
	cEv.empty();
	
	if (error) {
		per.append('<dt>что-то не так</dt>');
		pro.append('<li>что-то не так</li>');
		cEv.append('<li>что-то не так</li>');
	}
	
	if ($.propersList) {
		for (k in $.propersList.persons) {
			per.append('<DT>' + $.propersList.persons[k].name + '</DT>');
			
			var DL = $('<DL class="cInfo" />').appendTo( $('<DD />').appendTo(per) );
			
			for (n in $.propersList.persons[k]) {
				var n1, nx = ($.propersList.persons[k][n] == null || $.propersList.persons[k][n] == ""),
					n2 = nx ? '—' : $.propersList.persons[k][n];
				
				switch(n) {
					case 'position':
						n1 = 'Должность';
					break;
					
					case 'tel':
						n1 = 'Телефон';
					break;
					
					default :
						n1 = n;
					break;
				}
				
				if ( n != "name" ) {
					DL.append('<dt>' + n1 + ':</dt><dd>' + n2 + '</dd>');
				}
			}
		}
		
		for (k in $.propersList.projects) {
			var DL_1 = $('<DL />').appendTo( $('<LI />').appendTo(pro) ).append('<DT><SPAN>' + $.propersList.projects[k].name + '</SPAN> <A href="#" class="btn btn-mini" rel="ce_' + k + '">КC</A></DT>'),
				DL_2 = $('<DL class="leftrightlist" />').appendTo( DL_1 );
			
			for (n in $.propersList.projects[k]) {
				var n1, nx = ($.propersList.projects[k][n] == null || $.propersList.projects[k][n] == ""),
					n2 = nx ? '—' : $.propersList.projects[k][n];
				
				switch(n) {
					case 'status':
						n1 = 'Статус';
					break;
					
					case 'info':
						n1 = 'Описание';
					break;
					
					case 'system':
						n1 = 'ИС';
					break;
					
					case 'local_url':
						n1 = 'Ссылка';
						n2 = n2 == "—" ? n2 : '<A href="' + n2 + '">' + n2 + '</A>';
					break;
					
					default :
						n1 = n;
					break;
				}
				
				if ( n != "name" && n != "events" ) {
					DL_2.append('<dt>' + n1 + ':</dt><dd>' + n2 + '</dd>');
				}
				
				if ( n == "events" ) {
					drawEvents($.propersList.projects[k][n], cEv, 'ce_' + k);
				}
			}
		}
		
		drawEvents($.propersList.unlinked_events, cEv, 'ce_unlinked');
	}
	
	fixHeight();
}

function drawEvents(o, el, cLass) {
	for (k in o) {
		var DL = $('<DL class="leftrightlist" />').appendTo( $('<LI class="' + cLass + '" />').appendTo(el) );
		
		for (n in o[k]) {
			var n1, nx = (o[k][n] == null || o[k][n] == ""),
				n2 = nx ? '—' : o[k][n];
			
			switch(n) {
				case 'date':
					n1 = 'Дата';
					n2 = '<var>' + n2 + '</var>';
				break;
				
				case 'effect':
					n1 = 'Результат';
				break;
				
				case 'person':
					n1 = 'Персона';
				break;
				
				case 'position':
					n1 = 'Должность';
				break;
				
				case 'comment':
					n1 = 'Комментарий';
				break;
				
				default :
					n1 = n;
				break;
			}
			
			DL.append('<dt>' + n1 + ':</dt><dd>' + n2 + '</dd>');
		}
	}
}

function panelOperation(o) {
	var fadespeed = 200;
	//var time1 = new Date().getTime();
	
	$.hiddenElems.animate({
		opacity : 0.1
	}, fadespeed / 2, function() {
		var el = $(this);
		
		if (el.is('H1')) {
			el.text(o.name);
		}
		
		if (el.is('#cInfo')) {
			el.find('DL').empty().eq(1).hide();
			el.find('BUTTON').removeClass('dropup');
			getCompanyInfo(o, el);
		}
		
		if (el.is('#cPersons')) {
			$.getPropersList(o.id, drawProPerEv);
		}
		
		el.animate({
			opacity : 1
		}, fadespeed);
	}).css({
		visibility : 'visible'
	});
	
	var highlightLeftElement = $('[data-rel = "bar_' + o.id + '"]');
	$('#aside LI').removeClass('active');
	highlightLeftElement.addClass('active');
	/*
	highlightLeftElement.addClass($.clk ? 'active' : 'active blink');
	setTimeout(function() {
		$('#aside LI.blink').removeClass('blink');
	}, 600);
	*/
	if ( highlightLeftElement.position().top < 0 || highlightLeftElement.position().top > $('#aside UL').height() ) {
		$('#aside UL').scrollTop( $('#aside UL').scrollTop() + highlightLeftElement.position().top + 1 );
	}
	
	$('#cList').typeahead('setQuery', '').blur();
	
	//console.log(new Date().getTime() - time1);
}

function getCompanyInfo(o, el) {
	var dl_1 = el.find('DL:first-child'),
		dl_2 = dl_1.next();
	
	for (k in o) {
		if ( o[k] && k != "name" && k != "id" ) {
			switch(k) {
				case 'city':
					dl_1.append( '<DT>Город:</DT><DD>' + getCity( o[k] ) + '</DD>' );
				break;
				
				case 'address':
					dl_1.append( '<DT>Адрес:</DT><DD>' + o[k] + '</DD>' );
				break;
				
				case 'branch_description':
					dl_1.append( '<DT>Деятельность:</DT><DD>' + o[k] + '</DD>' );
				break;
				
				case 'url':
					dl_1.append( '<DT>Ссылка:</DT><DD><a href="http://' + o[k] + '" target="_blank">' + o[k] + '</a></DD>' );
				break;
				
				default :
					dl_2.append( '<DT>' + k + ':</DT><DD>' + o[k] + '</DD>' );
				break;
			}
		}
	}
}

function getCompany(id) {
	if ($.companyList) {
		var c;
		for (k in $.companyList) {
			var aidi = $.companyList[k].pk;
			
			if (id == aidi) {
				c = $.companyList[k].fields;
			}
		}
		c.id = id;
		return c;
	}
}

function getCity(num) {
	var cities = {
		"11" : "Альметьевск",
		"10" : "Барнаул",
		"5"  : "Воронеж",
		"3"  : "Екатеринбург",
		"9"  : "Иркутск",
		"12" : "Казань",
		"8"  : "Краснодар",
		"1"  : "Москва",
		"7"  : "Набережные Челны",
		"6"  : "Пермь",
		"2"  : "Санкт-Петербург"
	};
	
	return cities[num];
}

function highlight(match) {
	return match.replace(new RegExp('(' + $.myquery + ')', 'ig'), function ($1, match) {
		return '<span>' + match + '</span>';
	});
}

function myTitle(el) {
	$.label = $('<div class="myLabel" />').appendTo('BODY');
	
	$('BODY').on('hover', el, function(e) {
		if (e.type == 'mouseenter') {
			showTitle($(this));
		} else {
			hideTitle($(this));
		}
	});
	
	$(window).mousemove(function(e) {
		var posX = e.clientX + 12,
			posY = e.clientY + 14;
		
		if (posY + 24 >= $(document).height()) posY = e.clientY - 14;
		
		$.label.css({
			left : posX,
			top  : posY
		});
	});
}

function showTitle(el) {
	if (el.prop('title')) {
		el.attr( 'data-title', el.attr('title') ).attr('title', '');
		$.toID = setTimeout(function() {
			$.label.text( el.attr( 'data-title') ).fadeIn('fast');
		}, 444);
	}
}

function hideTitle(el) {
	clearTimeout($.toID);
	el.attr( 'title', el.attr('data-title') ).attr('data-title', '');
	$.label.hide();
}

function fixHeight(delta) {
	if (delta) {
		$('#cPP').animate({
			height : $('#cPP').height() - delta + 'px'
		});
		console.log( delta );
	} else {
		$('#cPP').height( $('BODY > .body').height() - 10 - $('#cPP').position().top );
	}
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
































