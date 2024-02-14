var stripe = Stripe('pk_test_51OjR38HrB7JipLatt8OXGLjGJS3Cb0n8o6j3qT40CHOUwxFLkPYLMVawcdHa9KeBsnGOUSloYjeC6B5pdEEcWkKf00K0eevy5D');

var elements = stripe.elements();
var style = {
    base: {
        color: "#000", // Make sure the color value is correctly formatted
        lineHeight: '2.4',
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

form.addEventListener('submit', function (ev) { // Corrected 'submet' to 'submit'
    ev.preventDefault();
    document.getElementById('submit').disabled = true; // Disable the button to prevent multiple submissions

    var firstName = document.getElementById('first-name').value;
    var lastName = document.getElementById('last-name').value;
    var email = document.getElementById('email').value;
    var phone = document.getElementById('phone').value;
    var address = document.getElementById('address').value;
    var city = document.getElementById('city').value;
    var region = document.getElementById('region').value;
    var clientSecret = document.getElementById('submit').getAttribute('data-secret'); // Ensure you have the clientSecret

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
                    // Add country and postal_code if needed
                }
            }
        }
    }).then(function(result) {
        if (result.error) {
            // Show error in #card-errors element
            var errorElement = document.getElementById('card-errors');
            errorElement.textContent = result.error.message;

            // Re-enable the submit button
            document.getElementById('submit').disabled = false;
        } else {
            // The payment has been processed!
            if (result.paymentIntent.status === 'succeeded') {
                // Payment succeeded, show a confirmation message
                console.log("Payment succeeded!");
                // Redirect to success page or update UI accordingly
            }
        }
    });
});
