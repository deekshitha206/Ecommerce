$(document).ready(function() {
  if ($('#flash-msg').length) {
    $('#flash-msg').fadeIn().delay(1000).fadeOut();
  }

  $('#checkout-form').on('submit', function(e){
    let name = $('input[name="name"]').val().trim();
    let address = $('textarea[name="address"]').val().trim();
    if (!name || !address) {
      alert('Please fill all required fields');
      e.preventDefault();
    }
  });
});
