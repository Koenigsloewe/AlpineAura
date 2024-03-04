$(document).ready(function () {
    $('#decrease-qty').click(function (e) {
        e.preventDefault();
        var qtyInput = $('#product-qty');
        var currentQty = parseInt(qtyInput.val());
        if (currentQty > 1) {
            qtyInput.val(currentQty - 1);
        }
    });

    $('#increase-qty').click(function (e) {
        e.preventDefault();
        var qtyInput = $('#product-qty');
        var currentQty = parseInt(qtyInput.val());
        qtyInput.val(currentQty + 1);
    });

    $('#add-button').click(function (e) {
        e.preventDefault();
        var button = $(this);
        var infoIconUrl = button.data('info-icon');
        var closeIconUrl = button.data('close-icon');

        $.ajax({
            type: 'POST',
            url: button.data('url'),
            data: {
                productid: button.val(),
                productqty: $('#product-qty').val(),
                csrfmiddlewaretoken: button.data('csrf-token'),
                action: 'post'
            },
            success: function (json) {
                document.getElementById('cart-qty').innerHTML = json.qty
                console.log(json.message)
                console.log(json)

                let messagesContainer = document.getElementById('messages-container');
                messagesContainer.innerHTML = `<div class="flex items-center justify-between bg-blue-100 border-t-4 border-blue-500 rounded-b text-blue-900 px-4 py-3 shadow-md" role="alert">
                                    <div class="flex items-center">
                                        <img class="h-6 w-6 mr-2" src="${infoIconUrl}" alt="Info">
                                        <p class="font-bold mr-4">Notification</p>
                                        <p class="text-sm">${json.message}</p>
                                    </div>
                                    <button class="close-button text-sm text-blue-500 focus:outline-none" onclick="this.parentElement.style.display='none';">
                                        <img src="${closeIconUrl}" alt="Close" class="h-6 w-6">
                                    </button>
                               </div>`;
                messagesContainer.style.display = 'block';
            },
            error: function (xhr, errmsg, err) {
                console.log(errmsg);
            }
        });
    });

    $(document).on('click', '.delete-button', function (e) {
        e.preventDefault();
        var prodId = $(this).data('index');
        var button = $(this);
        $.ajax({
            type: 'POST',
            url: button.data('url'),
            data: {
                productid: $(this).data('index'),
                csrfmiddlewaretoken: button.data('csrf-token'),
                action: 'post'
            },
            success: function (json) {
                $('.product-item[data-index="' + prodId + '"]').remove();
                document.getElementById("items-count").innerHTML = json.qty + ' Items';
                document.getElementById("cart-qty").innerHTML = json.qty;
            },
            error: function (xhr, errmsg, err) {
                console.log(errmsg);
            }
        });
    });

    $(document).on('click', '.update-button', function (e) {
        e.preventDefault();
        const button = $(this);
        const prodId = button.data('index');
        const csrfToken = button.data('csrf-token');
        const url = button.data('url');
        const qtyInput = button.siblings('input[type="number"]'); // Assuming the input is a sibling of the button
        let productQty = parseInt(qtyInput.val(), 10);

        // Determine if the button is for increase or decrease
        if (button.hasClass('decrease-qty') && productQty > 1) {
            productQty -= 1; // Decrease quantity
        } else if (button.hasClass('increase-qty')) {
            productQty += 1; // Increase quantity
        }

        // Update the quantity in the input field
        qtyInput.val(productQty);

        // Perform the AJAX request to update the cart
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                productid: prodId,
                productqty: productQty,
                csrfmiddlewaretoken: csrfToken,
                action: 'post'
            },
            success: function (json) {
                document.getElementById("items-count").innerHTML = json.qty + ' Items';
                document.getElementById("cart-qty").innerHTML = json.qty;
                document.getElementById("total_price").innerHTML = '€' + json.subtotal;
                $('.product-item[data-index="' + prodId + '"] .item-total-price').html('€' + json.totalItemPrice);

            },
            error: function (xhr, errmsg, err) {
                console.error('Error updating basket:', errmsg);
            }
        });
    });
});
