
paydiv.ongood = function (purchased, content) {
  $('#video_holder').hide();
  if(purchased) {
    $('#buy').hide();
    $('#notice').hide();
    $('#video_holder').show();
  } else {
    $('#buy').show();
    $('#notice').show();
  }

  // footer should be dealt with now, but need to alter the button
  if(purchased && content) {
    $('#video_holder').show();
  } else {
    $('#video_holder').hide();
  }

}

paydiv.onerror = function (req) {
  $('#buy').show();
  $('#notice').show();
}

$boot(paydiv);
