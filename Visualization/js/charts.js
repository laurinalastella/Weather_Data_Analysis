// Deliverable 1: Create a Drop-down City List
function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of city names to populate the select options
  d3.csv("Resources/five_cities.csv").then((data) => {
    console.log(data);

    data.forEach((city) => {
      selector
        .append("option")
        .text(city.city)
        .property("value", city.city);
    });

    // Use the first city from the list to build the initial plots
    var firstCity = data[0].city;
    buildCharts(firstCity);
    buildMetadata(firstCity);
    buildBar(firstCity);
  });
}

// Initialize the dashboard
init();

function optionChanged(newCity) {
  // Fetch new data each time a new city is selected
  buildMetadata(newCity);
  buildCharts(newCity);
  buildBar(newCity);
}

// Deliverable 2: Weather Summary Panel 
function buildMetadata(city) {
 
  d3.json("Resources/five_cities_2010_to_2019.json").then((data) => {
    var summary= data.weatherdata;
    console.log(city);
    var resultArray = summary.filter(sampleObj => sampleObj.city == city);
    var result = resultArray[0];
    console.log(result); 
    var PANEL = d3.select("#summary");
    
    // Use `.html("") to clear any existing metadata
    PANEL.html("");

    // Use `Object.entries` to add each key and value pair to the panel
    Object.entries(result).forEach(([key, value]) => {
      PANEL.append("h6").text(`${key.toUpperCase()}: ${value}`);
    });
  });
}

// Deliverable 3: Create a Temperature Pie Chart
// 1. Create the buildCharts function.
function buildCharts(city) {
  // 2. Use d3.csv to load and retrieve the five_cities.csv file 
  var temp=[]
  var humid=[]
  d3.csv("Resources/five_cities.csv").then((data) => {
  // 3. Retrieve the temperature values for each city 
    data.forEach((cities)=> {
      // console.log(city);
      if(cities.city==city) {
        temp.push(cities.freezing);
        temp.push(cities.cold);
        temp.push(cities.warm);
        temp.push(cities.hot);
        humid.push(cities.low_humidity);
        humid.push(cities.medium_humidity);
        humid.push(cities.high_humidity);
      };
    });
    console.log(temp);
    console.log(humid);

    var pieData = [{
      values: temp,
      labels: ['freezing', 'cold', 'warm','hot'],
      colors: ['blue', 'green', 'orange', 'red'],
      type: 'pie',
    }];
    
    var layout = {
      // title: "Temperature Pie Chart",
      height: 400,
      width: 500
    };
    Plotly.newPlot('tempPie', pieData, layout);
    
// Deliverable 4: Create a Humidity Donut Chart
  var donutData = [{
    values: humid,
    labels: ['low_humidity', 'medium_humidity', 'high_humidity'],
    type: 'pie',
    hole: .4
  }];

    var layout = {
      // title: "Humidity Donut Chart",
      height: 400,
      width: 500,
      annotations: [
        {
          font: {
            size: 12
          },
          showarrow: false,
          text: '<b>Humidity</b>'
        },
      ],
    };
    Plotly.newPlot('humidDonut', donutData, layout);
  });
}

// Deliverable 5: Create a Rainfall Bar Chart
function buildBar(city) {
  // 2. Use d3.csv to load and retrieve the five_cities.csv file 
  var rainfall=[]
  d3.csv("Resources/rainfall_annually.csv").then((data) => {
  // 3. Retrieve the temperature values for each city 
    data.forEach((cities)=> {
      // console.log(city);
      if(cities.city==city) {
        rainfall.push(cities.year_2010);
        rainfall.push(cities.year_2011);
        rainfall.push(cities.year_2012);
        rainfall.push(cities.year_2013);
        rainfall.push(cities.year_2014);
        rainfall.push(cities.year_2015);
        rainfall.push(cities.year_2016);
        rainfall.push(cities.year_2017);
        rainfall.push(cities.year_2018);
        rainfall.push(cities.year_2019);
      };
    });
    console.log(rainfall);

    var barData = [{
    x: ['2010', '2011','2012','2013','2014','2015','2016','2017','2018','2019'],
    y: rainfall,
    type: 'bar'
  }];

    var layout = {
      title: {text: "<b>Annual Cumulative Rainfall (2010-2019)</b>"},
      yaxis: {
        title: 'Rainfall (inches)'},
      height: 500,
      width: 1000,
    };
    Plotly.newPlot('rainBar', barData, layout);
  });
}