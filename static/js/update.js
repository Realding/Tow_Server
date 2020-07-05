
	var $progress = $('.progress'), $bar = $('.progress__bar'), $text = $('.progress__text'), percent = 0, update, resetColors, speed = 1000, orange = 20, yellow = 40, green = 60, blue = 80, timer;
	resetColors = function (bar) {
	    bar.removeClass('progress__bar--green').removeClass('progress__bar--yellow').removeClass('progress__bar--orange').removeClass('progress__bar--blue');
	};
	update = function () {
	    timer = setTimeout(function () {
            $.getJSON('/ajax_get_data/', function (ret) {
                //返回值 ret
                $.each(ret, function(key, value){
                    // key 为字典的 key，value 为对应的值
                    percent = value;
                    $text = $('#'+key).find('.progress__text');
                    $bar = $('#'+key).find('.progress__bar');
                    percent = parseFloat(percent.toFixed(1));
                    $text.find('em').text(percent + '%');
                    if (percent >= 100) {
                        percent = 100;
                        // {#$progress.addClass('progress--complete');#}
                        // {#$bar.addClass('progress__bar--blue');#}
                        // {#$text.find('em').text('Complete');#}
                    } else {
                        resetColors($bar);
                        if (percent >= blue) {
                            $bar.addClass('progress__bar--blue');
                        } else if (percent >= green) {
                            $bar.addClass('progress__bar--green');
                        } else if (percent >= yellow) {
                            $bar.addClass('progress__bar--yellow');
                        } else if (percent >= orange) {
                            $bar.addClass('progress__bar--orange');
                        }
                    }
                    $bar.css({ width: percent + '%' });
                    $('#'+key+"_bar").css({ width: percent + '%' });
                });
            });
            // {#speed = Math.floor(Math.random() * 900);#}
            speed = 1000;
            update();
	    }, speed);
	};
	setTimeout(function () {
	    $progress.addClass('progress--active');
	    update();
	}, 1000);
	/*$(document).on('click', function (e) {
	    percent = 0;
	    clearTimeout(timer);
	    resetColors();
	    update();
	});*/
