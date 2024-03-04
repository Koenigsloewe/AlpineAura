document.addEventListener('DOMContentLoaded', function () {
    var stripe = Stripe(STRIPE_PUBLISHABLE_KEY);

    var elements = stripe.elements();
    var style = {
        base: {
            color: "#000", lineHeight: '2', fontSize: '16px'
        }
    };

    var card = elements.create("card", {style: style});
    card.mount("#card-element");

    card.on('change', function (event) {
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

    document.getElementById('stripe-payment-button').addEventListener('click', function (ev) {
        ev.preventDefault();

        var csrfToken = getCookie('csrftoken');
        var clientSecret = document.getElementById('stripe-payment-button').getAttribute('data-secret');

        this.disabled = true;
        console.log(country)

        $.ajax({
            type: "POST", url: 'http://127.0.0.1:8000/orders/add/', data: {
                order_key: clientSecret, csrfmiddlewaretoken: csrfToken, action: "post"
            }, success: function (json) {
                console.log(json.success);

                stripe.confirmCardPayment(clientSecret, {
                    payment_method: {
                        card: card, billing_details: {
                            name: fullName, address: {
                                line1: address1, line2: address2, postal_code: postCode, country: country
                            }
                        }
                    }
                }).then(function (result) {
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
            }, error: function (xhr, status, error) {
                // Handle the error here
                console.error("Error in AJAX request: " + status + " - " + error);
                var errorElement = document.getElementById('card-errors');
                errorElement.textContent = "Error processing your order. Please try again.";
                $('#card-errors').addClass('alert alert-danger');

                document.getElementById('stripe-payment-button').disabled = false;
            }
        });
    });

});