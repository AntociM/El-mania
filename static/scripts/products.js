window.onload=()=>{

    // Sorting
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


    // Filtering

    function activateFilterEventListener(event) {
        var url = new URL(document.URL);

        // Get price
        var price_accordion =  document.getElementById("panelStayOpen-price");
        var min_price = price_accordion.children[0].children[0].children[1].value;
        var max_price = price_accordion.children[0].children[0].children[3].value;

        if (min_price) {
            url.searchParams.set('min_price', min_price);
        }
        else {
            url.searchParams.delete('min_price');
        }

        if (max_price) {
            url.searchParams.set('max_price', max_price);
        }
        else {
            url.searchParams.delete('max_price');
        }
        
        window.location.href = url;

    }
    document.getElementById("activate-product-filter").addEventListener("click", activateFilterEventListener);




    function clearFilterEventListener(event) {
        var url = new URL(document.URL);

        // Get price
        var price_accordion =  document.getElementById("panelStayOpen-price");
        url.searchParams.delete('min_price');
        url.searchParams.delete('max_price');

        window.location.href = url;
    }
    document.getElementById("clear-product-filter").addEventListener("click", clearFilterEventListener);


};
