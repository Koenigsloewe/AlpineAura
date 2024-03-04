$(document).ready(function() {
  $('input[type=radio][name=delivery_option]').on('change', function(e) {
    e.preventDefault();
    const csrfToken = $(this).attr('data-csrf-token');
    const url = $(this).attr('data-url');
    $.ajax({
      type: "POST",
      url: url, // Use the URL from the radio button's data attribute
      data: {
        delivery_option: $(this).val(),
        csrfmiddlewaretoken: csrfToken,
        action: "post",
      },
      success: function(json) {
        document.getElementById("totalCost").innerHTML = json.total + " €";
        document.getElementById("deliveryCost").innerHTML = json.delivery_price + " €";
      },
      error: function(xhr, errmsg, err) {
        console.log('Error updating delivery option: ' + errmsg);
      },
    });
  });
});
