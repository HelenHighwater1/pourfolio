'use strict';

const varietalFilter = document.querySelector('#varietal');
const countryFilter = document.querySelector('#country');
const regionFilter = document.querySelector('#region');
const vineyardFilter = document.querySelector('#vineyard');
const celebrationFilter = document.querySelector('#celebration');
const vintageFilter = document.querySelector('#vintage');

function apply_filters(evt) {
    evt.preventDefault();
    const filterItm = evt.target.id
    const filterVal = evt.target.value
    console.log('XXXXXXXXXXXXXX')
    console.log(filterItm)
    console.log(filterVal)
    const url = `/filter_cellar?filter_on=${filterItm}&filter_val=${filterVal}`

    fetch(url)
        .then(response => response.json())
        .then(res => {
            console.log('#########')
            console.log(res)
            document.querySelector('#cellar_lots').innerHTML = '';
            document.querySelector('#cellar_lots').classList.add("card-columns");
            document.querySelector('#filtered-by').innerHTML = `${filterItm}: ${filterVal}`;
            
            res.forEach(lot => {
                document.querySelector('#cellar_lots').insertAdjacentHTML(
                    'beforeend', 
                    `<div class="card" >
                        <a href='/lots/${lot.lot_id }'>
                            <img class="card-img-top" src='${lot.image}' alt="Card image cap">
                            <div class="card-body">
                                <p class="card-title">${lot.wine_name}</p>
                                <p class="card-subtitle">${lot.varietal}</p>
                                <p class="card-text">${new Date(lot.vintage).getFullYear()}</p>
                            </div>
                        </a>
                    </div>`
                )
            })
            document.querySelector(`#${filterItm}`).value=filterItm
        })
}


const filters = [varietalFilter, vintageFilter, celebrationFilter, vineyardFilter, countryFilter, regionFilter];

filters.forEach(filter => {
    filter.addEventListener('change', apply_filters);
});




// --------------------------------------------
// ------------- Search -----------------------
// --------------------------------------------

const searchForm = document.querySelector('#searchForm')
searchForm.addEventListener('submit', searchFilter)


function searchFilter(evt){
    evt.preventDefault()
    const searchTerm = evt.target[0].value
    console.log('XXXXXXXXXXXXXX')
    console.log(searchTerm)
    const url = `/search_cellar?search_term=${searchTerm}`

    fetch(url)  
        .then(response => response.json())
        .then(res => {
            document.querySelector('#cellar_lots').innerHTML = '';
            document.querySelector('#cellar_lots').classList.add("card-columns");
            
            res.forEach(lot => {
                document.querySelector('#cellar_lots').insertAdjacentHTML(
                    'beforeend', 
                    `<div class="card" >
                        <a href='/lots/${lot.lot_id }'>
                            <img class="card-img-top" src='static/imgs/generic_red.png' alt="Card image cap">
                            <div class="card-body">
                                <p class="card-text">${lot.wine_name}</p>
                                <p class="card-text">${new Date(lot.vintage).getFullYear()}</p>
                            </div>
                        </a>
                    </div>`
                )
            })
        })    
}