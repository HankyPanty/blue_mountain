// The list of prize money per questions. Change the number of values to change number of questions required. Change
// var prize_money_list = [
// 	"Fail", "1", "2", "3"//, "4", "5", "10", "20", "30", "40", "50", "60", "70", "80", "90", "100"
// ]

var is_padav_enabled = false;
// The padav questions.
var padav = [2, 5, 8];

// All the questions on and after this question index will not have options.
// If all the questions need an answer, set this value to infinite.
var no_option_questions_start_index = 8;

// Till this question, timer will be 60 secoonds. After this, timer will be 120 sec.
var timer_change_question_index = 5;

// If mouse selection is enabled.
var mouse = true;

// If keyboard selection is enabled.
var keyboard = false;


///////////////////////////////////////////////////////////////////////////
/////////////////////////////// ACTUAL CODE ///////////////////////////////
////////////////////// CONFIG VALUES ARE SHOWN ABOVE //////////////////////
///////////////////////////////////////////////////////////////////////////

var contestant_index = -1;
// Total number of questions. This is "prize_money_list - 1" because the prize_money_list also contains "0" value.
var total_questions = prize_money_list.length - 1;
var started = false;
var player = false;
var rules = false;
var need_last_ques_without_options = false;

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
function getContestant() {
	return contestants[contestant_index][0];
}
function nextContestant() {
	return contestant_index++;
}
function animateCrorepati() {
	var id = setInterval(animateCrorepatiInternal, 10);
	var width = 0;
	function animateCrorepatiInternal() {
		if (width == 100) {
			clearInterval(id);
		} else {
			width++;
			document.getElementById("logo_text_inner").style.width = width+"%";
		}
	}
}
function showBasicBackground() {
	document.getElementById('game').innerHTML=
	"<center>"
		+"<img src='/templates/kbc/base_logo.png'>"
		+"<div id='logo_text_outer'>"
			+"<div id='logo_text_inner'>CHAMPION</div>"
		+"</div>"
	+"</center>";
	animateCrorepati();
}
function showMainText(val) {
	var element = document.getElementById('game');
	element.innerHTML="";
	element.innerHTML=
		"<div id='fifty_outer'><div id='center_inner'>"
			+"<div style='top: 50%; position: relative;'><img src='/templates/kbc/template_black.png'></div>"
			+"<center><div id='text_big' style='top: 50%; position: absolute;'>" + val + "</div></center>"
		+"</div></div>";	
}

////
var rules_questions = false;
var rules_lifeline = false;
function showRules() {
	if (!rules_questions) {
		var element = document.getElementById('game');
		var htmlText="<div id='left_sixty'><div id='fifty_inner'><div id='center_inner_questions' style='padding-top:5%; opacity: 0; height: 50%; overflow: hidden'>";
		for (let i = total_questions; i > 0; i--) {
			htmlText+="<div id='question_number'><center><img id='img_question"+i+"' src='/templates/kbc/template_black.png' height='100%' width='70%'><div id='text_small_money'><div id='text_vertical_center'>"+prize_money_list[i]+"</div></div></center></div>";
		}
		htmlText+="</div></div></div>";
		element.innerHTML=htmlText;
		increaseOpacity('center_inner_questions');
		setTimeout(changeQuestionColor, 2000);
		rules_questions = true;
	} else if (!rules_lifeline) {
		var element = document.getElementById('game');
		element.innerHTML = element.innerHTML
			+"<div id='right_fourty'><div id='fifty_inner'><div id='center_inner_lifelines' style='padding-top:5%; opacity: 0; height: 30%; width: 200%; left: -100%; overflow: visible;'>"
				+"<img id='img_5050' onclick='progressGame(49);' src='/templates/kbc/5050.png' width='30%' height='30%'> "
				+"<img id='img_audpoll' onclick='progressGame(50);' src='/templates/kbc/audpoll.png' width='30%' height='30%'><br> "
				+"<img id='img_phone' onclick='progressGame(51);' src='/templates/kbc/flip.png' width='30%' height='30%'> "
				+"<img id='img_timer' src='/templates/kbc/circle.png' width='25%' height='30%'>"
				+"<div id='timer_text'><center><div id='text_large_timer'><div id='text_vertical_center'><div id='text_timer_main'>60s</div></div></div></center></div>"
				+"<br><img id='question_img' width='100%' style='position:relative; left:-40%; display: none'>"
			+"</div></div></div>";
		increaseOpacity('center_inner_lifelines');
		document.getElementById('center_inner_questions').style.opacity = 1;
		document.getElementById('timer_text').style.top=document.getElementById('img_timer').offsetTop;
		document.getElementById('timer_text').style.left=document.getElementById('img_timer').offsetLeft;
		document.getElementById('timer_text').style.height=document.getElementById('img_timer').height;
		document.getElementById('timer_text').style.width=document.getElementById('img_timer').width;
		
		rules_lifeline = true;
	} else {
		var element = document.getElementById('game');
		element.innerHTML = element.innerHTML
			+"<div id='bottom_fifty'>"
				+"<div id='top_fourty'><center style='position:relative;'><img src='/templates/kbc/template_black.png' width='75%' height = '100%'><div id='text_question'><div id='text_vertical_center'><div id='question'></div></div></div></center></div>"
				+"<div id='bottom_sixty'>"
					+"<center><br>"
						+"<div id='text_options'><div id='text_option_a'>A</div></div>"
						+"<div id='text_options'><div id='text_option_b'>B</div></div>"
						+"<div id='text_options'><div id='text_option_c'>C</div></div>"
						+"<div id='text_options'><div id='text_option_d'>D</div></div>"
						+"<img src='/templates/kbc/template_black.png' width='70%' id='img_option_a'><br>"
						+"<img src='/templates/kbc/template_black.png' width='70%' id='img_option_b'><br>"
						+"<img src='/templates/kbc/template_black.png' width='70%' id='img_option_c'><br>"
						+"<img src='/templates/kbc/template_black.png' width='70%' id='img_option_d'><br>"
					+"</center>"
				+"</div>"
			+"</div>";
		/* Hacky */
		var img_option_a = document.getElementById('img_option_a');
		var img_option_b = document.getElementById('img_option_b');
		var img_option_c = document.getElementById('img_option_c');
		var img_option_d = document.getElementById('img_option_d');
		var text_option_a = document.getElementById('text_option_a');
		var text_option_b = document.getElementById('text_option_b');
		var text_option_c = document.getElementById('text_option_c');
		var text_option_d = document.getElementById('text_option_d');
		text_option_a.style.left = img_option_a.offsetLeft;
		text_option_a.style.top = img_option_a.offsetTop;
		text_option_b.style.left = img_option_b.offsetLeft;
		text_option_b.style.top = img_option_b.offsetTop;
		text_option_c.style.left = img_option_c.offsetLeft;
		text_option_c.style.top = img_option_c.offsetTop;
		text_option_d.style.left = img_option_d.offsetLeft;
		text_option_d.style.top = img_option_d.offsetTop;
		text_option_a.style.paddingLeft = "3%";
		text_option_b.style.paddingLeft = "3%";
		text_option_c.style.paddingLeft = "3%";
		text_option_d.style.paddingLeft = "3%";
		text_option_a.style.paddingTop = "2%";
		text_option_b.style.paddingTop = "2%";
		text_option_c.style.paddingTop = "2%";
		text_option_d.style.paddingTop = "2%";
		text_option_a.style.width = "65%";
		text_option_b.style.width = "65%";
		text_option_c.style.width = "65%";
		text_option_d.style.width = "65%";
		text_option_a.style.zIndex = "1";
		text_option_b.style.zIndex = "1";
		text_option_c.style.zIndex = "1";
		text_option_d.style.zIndex = "1";
		text_option_a.onclick = function(){progressGame(97);};
		text_option_b.onclick = function(){progressGame(98);};
		text_option_c.onclick = function(){progressGame(99);};
		text_option_d.onclick = function(){progressGame(100);};
		text_option_a.style.position = "absolute";
		text_option_b.style.position = "absolute";
		text_option_c.style.position = "absolute";
		text_option_d.style.position = "absolute";
		
		document.getElementById('center_inner_lifelines').style.opacity = 1;
		rules = true;
	}
}
function changeQuestionColor() {
	for (let i = total_questions; i > 0; i--) {
		if (isPadav(i)) {
			document.getElementById('img_question'+i).parentElement.getElementsByTagName('div')[0].style.color = "#ffe0a0";
		}
	}
}

function increaseOpacity(id) {
	var element = document.getElementById(id);
	var val = 0;
	var v = setInterval(increaseOpacityInternal, 10);
	function increaseOpacityInternal() {
		if (val >= 1) {
			clearInterval(v);
		} else {
			val += .01;
			element.style.opacity = val;
		}
	}
}

////
var question_index = 0;
var num_flips = 0;
var correct_option;
var selected_option;
var min_prize = 0;
var current_prize = 0;
var timer_id = -1;
function showTimer() {
	clearInterval(timer_id);
	var time = 60;
	if (question_index >= timer_change_question_index) {
		time = 120;
	}
	document.getElementById('text_timer_main').innerHTML = time + "s";
	timer_id = setInterval(showTimerInternal, 1000);
	function showTimerInternal () {
		time--;
		if (time <= 0) {
			clearInterval(timer_id);
			timer_id = -1;
			quit();
		}
		document.getElementById('text_timer_main').innerHTML = time + "s";
	}
	
}
function displayQuestion() {
	document.getElementById('question').innerHTML=contestants[contestant_index][1][question_index+num_flips][0];
	document.getElementById('text_option_a').innerHTML="A. "+contestants[contestant_index][1][question_index+num_flips][1];
	document.getElementById('text_option_b').innerHTML="B. "+contestants[contestant_index][1][question_index+num_flips][2];
	document.getElementById('text_option_c').innerHTML="C. "+contestants[contestant_index][1][question_index+num_flips][3];
	document.getElementById('text_option_d').innerHTML="D. "+contestants[contestant_index][1][question_index+num_flips][4];
	correct_option = contestants[contestant_index][1][question_index+num_flips][5];
	var img = document.getElementById('question_img');
	if (contestants[contestant_index][1][question_index+num_flips][6] === "") {
		img.src = "";
		img.style.display = 'none';
	} else {
		img.src = "/" + contestants[contestant_index][1][question_index+num_flips][6];
		img.style.display = '';
	}
	document.getElementById('img_question' + (question_index + 1)).src = '/templates/kbc/template_gray.png';
	showTimer();
}
function displayQuestion2() {
	document.getElementById('question').innerHTML=contestants[contestant_index][1][question_index+num_flips][0];
	document.getElementById('text_option_a').innerHTML="";//+contestants[contestant_index][1][question_index+num_flips][1];
	document.getElementById('text_option_b').innerHTML="";//"B. "+contestants[contestant_index][1][question_index+num_flips][2];
	document.getElementById('text_option_c').innerHTML="";//"C. "+contestants[contestant_index][1][question_index+num_flips][3];
	document.getElementById('text_option_d').innerHTML="";//"D. "+contestants[contestant_index][1][question_index+num_flips][4];
	// correct_option = contestants[contestant_index][1][question_index+num_flips][5];
	var img = document.getElementById('question_img');
	// if (contestants[contestant_index][1][question_index+num_flips][6] === "") {
		img.src = "";
		img.style.display = 'none';
	// } else {
	// 	img.src = contestants[contestant_index][1][question_index+num_flips][6];
	// 	img.style.display = '';
	// }
	document.getElementById('img_question' + (question_index + 1)).src = '/templates/kbc/template_gray.png';
	showTimer();
}
////
var animateOptionInternalId = -1;
function animateOption(id) {
	var option = document.getElementById(id);
	var src = "/templates/kbc/template_black.png";
	var num = 5;
	animateOptionInternalId = setInterval(animateOptionInternal, 100);
	function animateOptionInternal() {
		if (src === "/templates/kbc/template_black.png") {
			src = "/templates/kbc/template_green.png";
			option.src = src;
		} else {
			src = "/templates/kbc/template_black.png";
			option.src = src;
		}
		num--;
		if (num <= 0) {
			clearInterval(animateOptionInternalId);
			animateOptionInternalId = -1;
		}
	}
}
function showAnswer() {
	if (correct_option === "A") {
		animateOption('img_option_a');
	} else if (correct_option === "B") {
		animateOption('img_option_b');
	} else if (correct_option === "C") {
		animateOption('img_option_c');
	} else if (correct_option === "D") {
		animateOption('img_option_d');
	}
}

function isPadav(question_index) {
	if (!is_padav_enabled || padav.includes(question_index)) {
		return true;
	}
	return false;
}

function checkAnswer() {
	if (correct_option === selected_option) {
		question_index++;
		current_prize = prize_money_list[question_index];
		if (isPadav(question_index)) {
			min_prize = current_prize;
		}
		document.getElementById('img_question' + question_index).src = '/templates/kbc/template_black_complete.png';
	} else {
		current_prize = min_prize;
		playing_complete = true;
	}
	if (question_index == total_questions) {
		playing_complete = true;
	}
	checked = true;
}

function lockAnswer(answer) {
	playAudio("lock.mp3");
	selected_option = answer;
	if (selected_option === "A") {
		document.getElementById('img_option_a').src = '/templates/kbc/template_yellow.png';
	} else if (selected_option === "B") {
		document.getElementById('img_option_b').src = '/templates/kbc/template_yellow.png';
	} else if (selected_option === "C") {
		document.getElementById('img_option_c').src = '/templates/kbc/template_yellow.png';
	} else if (selected_option === "D") {
		document.getElementById('img_option_d').src = '/templates/kbc/template_yellow.png';
	}
	locked = true;
	if (timer_id == -1) {
		//
	} else {
		clearInterval(timer_id);
		timer_id = -1;
	}
}
function displayAppropriateQuestion() {
	playAudio("question.mp3");
	if (question_index == prize_money_list.length - 2 && need_last_ques_without_options) {
		displayQuestion2();
		question_displayed = true;
	} else {
		displayQuestion();
		question_displayed = true;
	}
}
function flip() {
	num_flips++;
	displayAppropriateQuestion();
}
function removeTwoOptions() {
	var incorrect_options = [];
	if (correct_option === "A") {
		//
	} else {
		incorrect_options.push("a");
	}
	if (correct_option === "B") {
		//
	} else {
		incorrect_options.push("b");
	}
	if (correct_option === "C") {
		//
	} else {
		incorrect_options.push("c");
	}
	if (correct_option === "D") {
		//
	} else {
		incorrect_options.push("d");
	}
	var random_index = Math.floor(Math.random() * incorrect_options.length);
	
	for (var i=0; i<incorrect_options.length; i++) {
		if (i == random_index) {
			continue;
		}
		document.getElementById('text_option_' + incorrect_options[i]).innerHTML = "";
	}
}
function blackout() {
	if (animateOptionInternalId != -1) {
		clearInterval(animateOptionInternalId);
		animateOptionInternalId = -1;
	}
	document.getElementById('img_option_a').src = '/templates/kbc/template_black.png';
	document.getElementById('img_option_b').src = '/templates/kbc/template_black.png';
	document.getElementById('img_option_c').src = '/templates/kbc/template_black.png';
	document.getElementById('img_option_d').src = '/templates/kbc/template_black.png';
	document.getElementById('question').innerHTML="";
	document.getElementById('text_option_a').innerHTML="A. ";
	document.getElementById('text_option_b').innerHTML="B. ";
	document.getElementById('text_option_c').innerHTML="C. ";
	document.getElementById('text_option_d').innerHTML="D. ";
	question_displayed = false;
	locked = false;
	checked = false;
}
////
var prev_key = 0;
var playing_complete = false;
var question_displayed = false;
var locked = false;
var checked = false;
var used_5050 = false;
var used_flip = false;

function resetForNextPlayer() {
	prev_key = 0;
	playing_complete = false;
	question_displayed = false;
	locked = false;
	checked = false;
	used_5050 = false;
	used_flip = false;
	question_index = 0;
	num_flips = 0;
	correct_option = "";
	selected_option = "";
	min_prize = 0;
	current_prize = 0;
	rules_questions = false;
	rules_lifeline = false;
	started = false;
	player = false;
	rules = false;
	animateOptionInternalId = -1;
	contestant_index++;
}
function playAudio(v) {
	var audio = new Audio('/templates/kbc/' + v);
	audio.play();
}
function quit() {
	playing_complete = true;
	showAnswer();
}

/*
enter : 13
1: 49
a: 97
n: 110
*/
document.onkeypress = function(key) {
	if (keyboard) {
		progressGame(key.which);
	}
}
function progressGame(key) {
	if (mouse) {
		prev_key = key;
		key = 13;
	}
	if (!started) {
		if (prev_key == 110 && key == 13) {
			resetForNextPlayer();
			showBasicBackground();
			playAudio("start.mp3");
			started = true;
		}
	} else if (!player) {
		if (prev_key == 110 && key == 13) {
			var contestant = getContestant();
			if (contestant == 'end') {
				return;
			}
			showMainText(getContestant());
			player = true;
		}
	} else if (!rules) {
		if (prev_key == 110 && key == 13) {
			showRules();
		}
	} else if (!playing_complete) {
		if (!question_displayed) {
			if (prev_key == 110 && key == 13) {
				displayAppropriateQuestion();
			}
		} else {
			if (key == 13) { // enter pressed, check if previous key was valid.
				if (!locked) {
					if (need_last_ques_without_options && question_index == total_questions - 1) {
						correct_option='C';
						if (prev_key == 99) {
							selected_option = 'C';
							locked = true;
							if (timer_id == -1) {
								//
							} else {
								clearInterval(timer_id);
								timer_id = -1;
							}
						} else if (prev_key == 119) {
							selected_option = 'W';
							locked = true;
							if (timer_id == -1) {
								//
							} else {
								clearInterval(timer_id);
								timer_id = -1;
							}
						} else if (prev_key == 113) {
							// Q
							playing_complete = true;
							if (timer_id == -1) {
								//
							} else {
								clearInterval(timer_id);
								timer_id = -1;
							}
						}
					} else {
						if (prev_key == 97) {
							lockAnswer("A");
						} else if (prev_key == 98) {
							lockAnswer("B");
						} else if (prev_key == 99) {
							lockAnswer("C");
						} else if (prev_key == 100) {
							lockAnswer("D");
						} else if (prev_key == 49) {
							if (!used_5050) {
								used_5050 = true;
								document.getElementById("img_5050").style.opacity = '.1';
								removeTwoOptions();
							}
						} else if (prev_key == 50) {
							document.getElementById("img_audpoll").style.opacity = '.1';
						} else if (prev_key == 51) {
							if (!used_flip) {
								used_flip = true;
								document.getElementById("img_phone").style.opacity = '.1';
								flip();
							}
						} else if (prev_key == 113) {
							quit();
						}
					}
				} else if (!checked && prev_key == 110) {
					checkAnswer();
					if (!need_last_ques_without_options || question_index < total_questions) {
						showAnswer();
					}
				} else if (prev_key == 110) {
					blackout();
				}
			}
		}
	} else if (prev_key == 110 && key == 13) {
		playAudio("finish.mp3");
		showMainText(current_prize);
		started = false;
	}
	prev_key = key;
};