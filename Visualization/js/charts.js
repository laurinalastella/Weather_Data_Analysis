// Deliverable 1: Create a Drop-down City List
function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of city names to populate the select options
  d3.csv("five_cities.csv").then((data) => {
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
  });
}

// Initialize the dashboard
init();

function optionChanged(newCity) {
  // Fetch new data each time a new city is selected
  buildMetadata(newCity);
  buildCharts(newCity);
}

// Deliverable 2: Weather Summary Panel 
function buildMetadata(city) {
  // var summary=[]
  d3.json("five_cities_2010_to_2019.json").then((data) => {
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
  d3.csv("five_cities.csv").then((data) => {
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
          text: 'Humidity'
        },
      ],
    };
    Plotly.newPlot('humidDonut', donutData, layout);
});
};