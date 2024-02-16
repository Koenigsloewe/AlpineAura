var stripe = Stripe('pk_test_51OjR38HrB7JipLatt8OXGLjGJS3Cb0n8o6j3qT40CHOUwxFLkPYLMVawcdHa9KeBsnGOUSloYjeC6B5pdEEcWkKf00K0eevy5D');

var elements = stripe.elements();
var style = {
    base: {
        color: "#000",
        lineHeight: '2',
        fontSize: '16px'
    }
};

var card = elements.create("card", { style: style });
card.mount("#card-element");

card.on('change', function(event) {
    var displayError = document.getElementById('card-errors');
    if (event.error) {
        displayError.textContent = event.error.message;
        $('#card-errors').addClass('alert alert-info');
    } else {
        displayError.textContent = '';
        $('#card-errors').removeClass('alert alert-info');
    }
});

var form = document.getElementById('payment-form');

form.addEventListener('submit', function (ev) {
    ev.preventDefault();

    document.getElementById('submit').disabled = true;

    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    var firstName = document.getElementById('first-name').value;
    var lastName = document.getElementById('last-name').value;
    var email = document.getElementById('email').value;
    var phone = document.getElementById('phone').value;
    var address = document.getElementById('address').value;
    var city = document.getElementById('city').value;
    var region = document.getElementById('region').value;
    var clientSecret = document.getElementById('submit').getAttribute('data-secret');

    $.ajax({
        type: "POST",
        url: 'http://127.0.0.1:8000/orders/add/',
        data: {
            order_key: clientSecret,
            csrfmiddlewaretoken: csrfToken,
            action: "post"
        },
        success: function (json) {
            console.log(json.success);

            stripe.confirmCardPayment(clientSecret, {
                payment_method: {
                    card: card,
                    billing_details: {
                        name: firstName + ' ' + lastName,
                        email: email,
                        phone: phone,
                        address: {
                            line1: address,
                            city: city,
                            state: region,
                        }
                    }
                }
            }).then(function(result) {
                if (result.error) {

                    var errorElement = document.getElementById('card-errors');
                    errorElement.textContent = result.error.message;

                    document.getElementById('submit').disabled = false;
                } else {

                    if (result.paymentIntent.status === 'succeeded') {

                        console.log("Payment succeeded!");
                        window.location.replace("http://127.0.0.1:8000/payment/orderplaced/");

                    }
                }
            });
        },
        error: function (xhr, status, error) {
            // Handle the error here
            console.error("Error in AJAX request: " + status + " - " + error);
            var errorElement = document.getElementById('card-errors');
            errorElement.textContent = "Error processing your order. Please try again.";
            $('#card-errors').addClass('alert alert-danger');

            document.getElementById('submit').disabled = false;
        }
    });
});
