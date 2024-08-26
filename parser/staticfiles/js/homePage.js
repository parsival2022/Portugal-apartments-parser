const root = document.getElementById('root')
const getQuantitiesUrl = "http://127.0.0.1:8000/parser/get_quantity/"
const getPricesUrl = "http://127.0.0.1:8000/parser/get_prices/"

function placeSpinner(){
    const html = `<div class="spinner-border text-dark mt-5" style="width: 5rem; height: 5rem;" role="status">
                     <span class="visually-hidden">Loading...</span>
                  </div>`
    root.innerHTML = html
}

async function fetchDataForChart(url, days) {
    try {
        const response = await fetch(`${url}${days}/`, { method: 'GET' });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
        return null;
    }
}

function main(){
    placeSpinner()
    const data = fetchDataForChart(getQuantitiesUrl, 4)
    console.log(data)
}

document.addEventListener('DOMContentLoaded', main, false)