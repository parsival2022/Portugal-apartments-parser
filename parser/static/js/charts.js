
Chart.defaults.backgroundColor = "#fff";
Chart.defaults.borderColor = "#1b1d1f";

function getDatasets(data, id){
    let datasets;
    if (id === QUANTITY) {
      datasets = [
        {
          label: "Amadora",
          data: data.map((entry) => entry.amadora),
          borderColor: "#d9480f",
          fill: "#d9480f",
        },
        {
          label: "Odivelas",
          data: data.map((entry) => entry.odivelas),
          borderColor: "#0f74d9",
          fill: "#0f74d9",
        },
      ];
    }
    if (id === PRICES) {
      datasets = [
        {
          label: "Amadora property prices",
          data: data.map((entry) => entry.amadora_property_price),
          borderColor: "#d9480f",
          fill: "#d9480f",
        },
        {
          label: "Odivelas property prices",
          data: data.map((entry) => entry.odivelas_property_price),
          borderColor: "#0f74d9",
          fill: "#0f74d9",
        },
      ];
    }
    if (id === PRICES_PER_SQM) {
      datasets = [
        {
          label: "Amadora prices per sqm",
          data: data.map((entry) => entry.amadora_price_per_sqm),
          borderColor: "#d9480f",
          fill: "#d9480f",
        },
        {
          label: "Odivelas prices per sqm",
          data: data.map((entry) => entry.odivelas_price_per_sqm),
          borderColor: "#0f74d9",
          fill: "#0f74d9",
        },
      ];
    }
    return datasets
  }

function createButtons() {
  buttonsContainer = document.createElement("div");
  buttonsContainer.className =
    "chart-buttons-container btn-group btn-group-toggle";
  buttonsContainer.setAttribute("data-toggle", "buttons");
  html = `<button type="button" data="5" class="btn btn-success btn-sm  m-3 active" data-toggle="button" aria-pressed="true">5 days</button>
            <button type="button" data="15" class="btn btn-success btn-sm m-3" data-toggle="button" aria-pressed="false">15 days</button>
            <button type="button" data="30" class="btn btn-success btn-sm m-3" data-toggle="button" aria-pressed="false">30 days</button>
            <button type="button" data="45" class="btn btn-success btn-sm m-3" data-toggle="button" aria-pressed="false">45 days</button>
            <button type="button" data="60" class="btn btn-success btn-sm m-3" data-toggle="button" aria-pressed="false">60 days</button>`;
  buttonsContainer.innerHTML = html;
  buttonsContainer.querySelectorAll(".btn").forEach((button) => {
    const buttonText = button.textContent;
    const days = parseInt(buttonText.match(/\d+/)[0], 10);
    button.addEventListener("click", reRenderChart);
  });
  return buttonsContainer;
}

async function fetchDataForChart(url, days) {
  try {
    const response = await fetch(`${url}${days}/`, { method: "GET" });
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    return await response.json();
  } catch (error) {
    console.error("Error fetching data:", error);
    return null;
  }
}

function renderChart(data, id) {
  const ctx = document.createElement("canvas").getContext("2d");
  const datasets = getDatasets(data, id)
  chart = new Chart(ctx, {
    type: "line",
    data: {
      labels: data.map((entry) => entry.date),
      datasets: datasets,
    },
    options: {
      plugins: {
        title: {
          display: true,
          color: "#343d4d",
          font: {
            size: "25px",
          },
          text: `Ads ${id} chart`,
        },
      },
    },
  });

  return ctx.canvas;
}

function renderContainerAndChart(data, id) {
  const chartContainer = document.createElement("div");
  chartContainer.className = "chart-container";
  chartContainer.id = id;
  const chart = renderChart(data, id);
  const buttonsContainer = createButtons();
  chartContainer.appendChild(chart);
  chartContainer.appendChild(buttonsContainer);
  root.renderHtml(chartContainer);
}

async function reRenderChart(e) {
  let url = getQuantitiesUrl;
  const button = e.target;
  const parent = e.target.parentElement.parentNode;
  const canvas = parent.getElementsByTagName("canvas")[0];
  const days = parseInt(e.target.getAttribute("data"));
  const id = parent.id;
  parent.querySelectorAll(".btn").forEach((button) => {
    button.classList.remove("active");
    button.setAttribute("aria-pressed", "false");
  });
  button.classList.add("active");
  button.setAttribute("aria-pressed", "true");
  if (id === PRICES || id === PRICES_PER_SQM) url = getPricesUrl;
  const data = await fetchDataForChart(url, days);
  const chart = renderChart(data, id);
  canvas.replaceWith(chart);
}