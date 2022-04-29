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
                    // address_select.setAttribute('display', 'none')
                    children[i].style.display = 'none'
                    // children[i].removeAttribute('required')
                    children[i].disabled=true
                }
                else {
                    children[i].disabled=false
                    // children[i].style.required = true
                    children[i].style.display = 'block'
                    // address_select.setAttribute('display', 'block')
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