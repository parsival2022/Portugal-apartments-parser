
const getQuantitiesUrl = "http://127.0.0.1:8000/parser/get_quantity/";
const getPricesUrl = "http://127.0.0.1:8000/parser/get_prices/";
const QUANTITY = "quantity";
const PRICES = "prices";
const PRICES_PER_SQM = "prices per sqm";
const currentPage = document.getElementById("current-page")


class Root {
    static #instance = null
    static spinner = `<div class="spinner-border text-dark mt-5" style="width: 5rem; height: 5rem;" role="status">
                           <span class="visually-hidden">Loading...</span>
                      </div>`

    constructor(){
        if (Root.#instance) {
            return Root.#instance;
        } else {
            this.root = document.getElementById("root")
            Root.#instance = this;
        }
    }

    renderSpinner(){
        this.root.innerHtml = this.spinner
    }
    clearSelf(){
        this.root.innerHtml = ""
    }
    renderHtml(html){
        this.root.appendChild(html)
    }
    reRenderSelf(html){
        this.clearSelf()
        this.renderHtml(html)
    }
}

const root = new Root()

async function renderHomePage() {
    root.renderSpinner()
    const QuantityData = await fetchDataForChart(getQuantitiesUrl, 5);
    const PricesData = await fetchDataForChart(getPricesUrl, 5);
    root.clearSelf()
    renderContainerAndChart(QuantityData, QUANTITY);
    renderContainerAndChart(PricesData, PRICES);
    renderContainerAndChart(PricesData, PRICES_PER_SQM);
    currentPage.innerHTML = "Home"
  }

function renderFiltersPage() {
    root.renderSpinner()
    const filtersContainer = `<div class="buttons-wrapper">
                                <h3 class="text-center">Select type of the apartment:</h3>
                                <div class="button-container">
                                    <button name="filter-btn" type="button">T0 </button>
                                    <button name="filter-btn" type="button">T1 </button>
                                    <button name="filter-btn" type="button">T2 </button>
                                    <button name="filter-btn" type="button">T3 </button>
                                    <button name="filter-btn" type="button">T4 </button>
                                </div>
                            </div>`
    root.reRenderSelf(filtersContainer)
    currentPage.innerHTML = "Filters"
}