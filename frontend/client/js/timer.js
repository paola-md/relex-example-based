var timer_write = "0:03";
var timer_edit = "0:03";

var interval = setInterval(function() {


  var timer = timer_write.split(':');
  //by parsing integer, I avoid all extra string processing
  var minutes = parseInt(timer[0], 10);
  var seconds = parseInt(timer[1], 10);
  --seconds;
  minutes = (seconds < 0) ? --minutes : minutes;
  if (minutes < 0) {
    $("#submit-button").prop("disabled",false);
    $('.writing-timer').fadeTo(2500, 0);
    $('.countdown').fadeTo(2500, 0);
    clearInterval(interval);

  }
  seconds = (seconds < 0) ? 59 : seconds;
  seconds = (seconds < 10) ? '0' + seconds : seconds;
  //minutes = (minutes < 10) ?  minutes : minutes;
  $('.countdown').html(minutes + ':' + seconds);
  timer_write = minutes + ':' + seconds;
}, 1000);






function startTimer() {
setInterval(function(){
    var timer = timer_edit.split(':');
    //by parsing integer, I avoid all extra string processing
    var minutes = parseInt(timer[0], 10);
    var seconds = parseInt(timer[1], 10);
    --seconds;
    minutes = (seconds < 0) ? --minutes : minutes;
    if (minutes < 0) {
      $("#save-button").prop("disabled",false);
      $('.save-timer').fadeTo(2500, 0);
      $('.save-countdown').fadeTo(2500, 0);
      clearInterval(interval);
  
    }
    seconds = (seconds < 0) ? 59 : seconds;
    seconds = (seconds < 10) ? '0' + seconds : seconds;
    //minutes = (minutes < 10) ?  minutes : minutes;
    $('.save-countdown').html(minutes + ':' + seconds);
    timer_edit = minutes + ':' + seconds;
  }, 1000);
}
