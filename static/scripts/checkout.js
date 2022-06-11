window.onload=()=>{

    function UpdateCardStateListner(event) {
        var cards = document.querySelectorAll('[id^="address-cards-"]');
        card = event.target.closest('div.card')


        // Card clicked again and user wants to deselect it
        if (card.classList.contains('border-success')) {
            card.classList.remove('border-success')
            card.children[0].removeChild(card.children[0].lastChild)
            card.classList.add('border-dark')
        }
        else {
            // Check if there are any other cards selected, then deselect them
            for(var i=0; i < cards.length; i++) {
                if (cards[i].classList.contains('border-success')) {
                    cards[i].classList.remove('border-success')
                    cards[i].children[0].removeChild(cards[i].children[0].lastChild)
                    cards[i].classList.add('border-dark')
                }
            }

            const success_span = document.createElement("span");
            success_span.classList.add("badge" ,"rounded-pill", "bg-success", "bi", "bi-check")
            success_span.innerHTML=" "
            card.classList.remove('border-dark')
            card.classList.add('border-success')
            card.children[0].appendChild(success_span)
        }

        // Disable the address for if one card is selected
        var address_select = document.getElementById('address-select')
        var one_card_selected = 0
        for(var i=0; i < cards.length; i++) {
            if (cards[i].classList.contains('border-success')) {
                one_card_selected = 1
                address_id = cards[i].id.split('-').slice(-1)
                address_select.setAttribute('value', address_id)
                break
            }
        }

        // Disable form fields
        var form = document.getElementById('address-form-fields')
        var fields_to_waive = ["redirect-url", "address-select", "id_notes"]
        var children = form.querySelectorAll('input,select,textarea')
        for (var i = 0; i < children.length; i++) {
            if (!(fields_to_waive.includes(children[i].id))) {
                if (one_card_selected) {
                    children[i].style.display = 'none'
                    children[i].disabled=true
                }
                else {
                    children[i].disabled=false
                    children[i].style.display = 'block'
                    address_select.setAttribute('value', 'create')
                }
            }

        }
    }

    var cards = document.querySelectorAll('[id^="address-cards-"]');
    for (var i=0; i< cards.length; i++) {
        cards[i].addEventListener("click", UpdateCardStateListner)
    }

}


    // This is a public sample test API key.
      // Don’t submit any personally identifiable information in requests made with this key.
      // Sign in to see your own test API key embedded in code samples.
      const stripe = Stripe("pk_test_51KsBIRF2IHJE5BFc3EzFIykgZbmrCnWMev3eHz8pAqARSweVT2E9RZHlfUvLKDwixnPOHyslq4R9zjjeURTalsNW00Tdv8iIls");

      // The items the customer wants to buy
      const items = [{
          id: "xl-tshirt"
      }];

      let elements;

      initialize();
      checkStatus();

      document
          .querySelector("#payment-form")
          .addEventListener("submit", handleSubmit);

      // Fetches a payment intent and captures the client secret
      async function initialize() {
          const response = await fetch("create-payment-intent/", {
              method: "POST",
              headers: {
                  "Content-Type": "application/json"
              },
              body: JSON.stringify({
                  items
              }),
          });
          const {
              clientSecret
          } = await response.json();

          const appearance = {
              theme: 'stripe',
          };
          elements = stripe.elements({
              appearance,
              clientSecret
          });

          const paymentElement = elements.create("payment");
          paymentElement.mount("#payment-element");
      }

      async function handleSubmit(e) {
          e.preventDefault();
          setLoading(true);

          const {
              error
          } = await stripe.confirmPayment({
              elements,
              confirmParams: {
                  // Make sure to change this to your payment completion page
                  return_url: "https://el-mania.herokuapp.com//checkout/success",
                  receipt_email: document.getElementById("id_email").value,
                //   description : document.getElementById("id_notes").value,
                  shipping : {
                    name: document.getElementById("id_full_name").value,
                    phone: document.getElementById("id_phone_number").value,
                    address: {
                        city: document.getElementById("id_city").value,
                        line1:  document.getElementById("id_address").value,
                        postal_code: document.getElementById("id_postcode").value,
                        country: document.getElementById("id_country").value,
                        state: document.getElementById("id_county").value,
                    }
                  }
              },
          });

          // This point will only be reached if there is an immediate error when
          // confirming the payment. Otherwise, your customer will be redirected to
          // your `return_url`. For some payment methods like iDEAL, your customer will
          // be redirected to an intermediate site first to authorize the payment, then
          // redirected to the `return_url`.
          if (error.type === "card_error" || error.type === "validation_error") {
              showMessage(error.message);
          } else {
              showMessage("An unexpected error occurred.");
          }

          setLoading(false);
      }

      // Fetches the payment intent status after payment submission
      async function checkStatus() {
          const clientSecret = new URLSearchParams(window.location.search).get(
              "payment_intent_client_secret"
          );

          if (!clientSecret) {
              return;
          }

          const {
              paymentIntent
          } = await stripe.retrievePaymentIntent(clientSecret);

          switch (paymentIntent.status) {
              case "succeeded":
                  showMessage("Payment succeeded!");
                  break;
              case "processing":
                  showMessage("Your payment is processing.");
                  break;
              case "requires_payment_method":
                  showMessage("Your payment was not successful, please try again.");
                  break;
              default:
                  showMessage("Something went wrong.");
                  break;
          }
      }

      // ------- UI helpers -------

      function showMessage(messageText) {
          const messageContainer = document.querySelector("#payment-message");

          messageContainer.classList.remove("hidden");
          messageContainer.textContent = messageText;

          setTimeout(function () {
              messageContainer.classList.add("hidden");
              messageText.textContent = "";
          }, 4000);
      }

      // Show a spinner on payment submission
      function setLoading(isLoading) {
          if (isLoading) {
              // Disable the button and show a spinner
              document.querySelector("#submit").disabled = true;
              document.querySelector("#spinner").classList.remove("hidden");
              document.querySelector("#button-text").classList.add("hidden");
          } else {
              document.querySelector("#submit").disabled = false;
              document.querySelector("#spinner").classList.add("hidden");
              document.querySelector("#button-text").classList.remove("hidden");
          }
      }