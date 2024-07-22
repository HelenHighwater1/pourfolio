'use strict';


console.log('in js')

const varietalFilter = document.getElementById('varietal-filter');
const countryFilter = document.getElementById('country-filter');
const regionFilter = document.getElementById('region-filter');
const vineyardFilter = document.getElementById('vineyard-filter');
const celebrationFilter = document.getElementById('celebration-filter');
const vintage = document.getElementById('vintage-filter');

function apply_filters(evt) {
    evt.preventDefault();
    const filterItm = evt.target.id
    const filterVal = evt.target.value
    const url = `/filter_cellar?filter_on=${filterItm}&filter_val=${filterVal}`

    fetch(url)
        .then(response => response.json())
        .then(res => {
            console.log(res)
            document.querySelector('#cellar-lots')
        })
}


     const forecast = responseJson.forecast;
      const temp = responseJson.temp;
      document.querySelector('#weather-info').innerHTML = `Temperature: ${temp}, Forecast: ${forecast}`

document.querySelector('#varietal').addEventListener('change', apply_filters)


