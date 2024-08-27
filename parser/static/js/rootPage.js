
async function main() {
  root.renderSpinner()
  const QuantityData = await fetchDataForChart(getQuantitiesUrl, 5);
  const PricesData = await fetchDataForChart(getPricesUrl, 5);
  root.clearSelf()
  renderContainerAndChart(QuantityData, QUANTITY);
  renderContainerAndChart(PricesData, PRICES);
  renderContainerAndChart(PricesData, PRICES_PER_SQM);
}

document.addEventListener("DOMContentLoaded", main, false);
