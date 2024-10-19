document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.getElementById('search');
    const filterSelect = document.getElementById('filter');
    const shopList = document.getElementById('shop-list');

    function fetchDiveShops(query = '', filter = '') {
        fetch(`/dive-shops?search=${query}&filter=${filter}`)
            .then(response => response.json())
            .then(data => {
                shopList.innerHTML = ''; 
                data.forEach(shop => {
                    const placeholderImage = "{{ url_for('static', filename='images/dsl_placeholder.webp') }}";

                    const imageUrl = shop.image_url ? shop.image_url : placeholderImage;
                    
                    const shopElement = document.createElement('div');
                    shopElement.classList.add('col-md-4', 'mb-4');
                    shopElement.innerHTML = `
                        <div class="card h-100">
                            <img src="${imageUrl}" class="card-img-top" alt="${shop.name}" style="height:200px; object-fit:cover;">
                            <div class="card-body">
                                <h5 class="card-title">${shop.name}</h5>
                                <p class="card-text">${shop.address}</p>
                                <p class="card-text">${shop.activity}</p>
                            </div>
                        </div>
                    `;
                    shopList.appendChild(shopElement);
                });
            });
    }

    searchInput.addEventListener('input', () => {
        fetchDiveShops(searchInput.value, filterSelect.value);
    });

    filterSelect.addEventListener('change', () => {
        fetchDiveShops(searchInput.value, filterSelect.value);
    });

    fetchDiveShops();
});