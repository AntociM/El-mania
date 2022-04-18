window.onload=()=>{


    var sorting_element = document.getElementById("product-sorting");

    function sortingEventListener(event) {
        var sort = document.getElementById("product-sorting-select").value;
        var order = document.getElementById("product-order-select").value;
        
        var url = new URL(document.URL);

        if (sort == 'none') {
            // Remove sorting from URL
            url.searchParams.delete('sort');
            url.searchParams.delete('order');
        }
        else {
            // Add sorting to the URL
            url.searchParams.set('sort', sort);
            url.searchParams.set('order', order);
        }
        window.location.href = url;
    }

    sorting_element.addEventListener("change", sortingEventListener);


};
