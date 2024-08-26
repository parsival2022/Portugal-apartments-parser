
async function main() {
  root.innerHTML = getSpinner();
  const QuantityData = await fetchDataForChart(getQuantitiesUrl, 5);
  const PricesData = await fetchDataForChart(getPricesUrl, 5);
  root.innerHTML = "";
  renderContainerAndChart(QuantityData, QUANTITY);
  renderContainerAndChart(PricesData, PRICES);
  renderContainerAndChart(PricesData, PRICES_PER_SQM);
}

document.addEventListener("DOMContentLoaded", main, false);
