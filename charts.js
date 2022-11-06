function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of "geo" names to populate the select options
  d3.csv("dummy5cities_daily.csv").then((data) => {
    var cityNames = data.city;
    console.log(cityNames);


    cityNames.forEach((city) => {
      selector
        .append("option")
        .text(city)
        .property("value", city);
    });

    // Use the first city from the list to build the initial plots
    var firstCity = cityNames[0];
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

// Demographics Panel 
function buildMetadata(city) {
  d3.csv("dummy5cities_daily.csv").then((data) => {
    var metadata = data.metadata;
    // Filter the data for the object with the desired "city" name
    var resultArray = metadata.filter(sampleObj => sampleObj.id == sample);
    var result = resultArray[0];
    // Use d3 to select the panel with id of `#sample-metadata`
    var PANEL = d3.select("#sample-metadata");

    // Use `.html("") to clear any existing metadata
    PANEL.html("");

    // Use `Object.entries` to add each key and value pair to the panel
    // Hint: Inside the loop, you will need to use d3 to append new
    // tags for each key-value in the metadata.
    Object.entries(result).forEach(([key, value]) => {
      PANEL.append("h6").text(`${key.toUpperCase()}: ${value}`);
    });

  });
}

// 1. Create the buildCharts function.
function buildCharts(sample) {
  // 2. Use d3.json to load and retrieve the samples.json file 
  d3.json("samples.json").then((data) => {
    // 3. Create a variable that holds the samples array. 
    var samples = data.samples;
    // 4. Create a variable that filters the samples for the object with the desired sample number.
    var resultArray = samples.filter(sampleObj => sampleObj.id == sample);
    var metadataArray = data.metadata.filter(sampleObj => sampleObj.id == sample);
    //  5. Create a variable that holds the first sample in the array.
    var result = resultArray[0];
    var metadata = metadataArray[0];
    var frequency = parseFloat(metadata.wfreq);

    // 6. Create variables that hold the otu_ids, otu_labels, and sample_values.
    var otu_ids = result.otu_ids;
    var otu_labels = result.otu_labels;
    var sample_values = result.sample_values;

    // 7. Create the yticks for the bar chart.
    // Hint: Get the the top 10 otu_ids and map them in descending order  
    //  so the otu_ids with the most bacteria are last. 
    var yticks = otu_ids.slice(0, 10).map(otuID => `OTU ${otuID}`).reverse();

    // 8. Create the trace for the bar chart. 
    var trace = [{
      y: yticks,
      x: sample_values.slice(0, 10).reverse(),
      text: otu_labels.slice(0, 10).reverse(),
      type: "bar",
      orientation: "h",
    }];

    // 9. Create the layout for the bar chart. 
    var barLayout = {
      title: "Top 10 Bacteria Cultures Found",
      margin: {t: 30, l: 150}
    
    };
    // 10. Use Plotly to plot the data with the layout. 
    Plotly.newPlot("bar", trace, barLayout);

    // 1. Create the trace for the bubble chart.
    var bubbleData = [{
      x: otu_ids,
      y: sample_values,
      text: otu_labels,
      mode: "markers",
      marker: {
        size: sample_values,
        color: otu_ids,
        colorscale: "Earth"
    }
  }]
   
    var data = [trace];

    // 2. Create the layout for the bubble chart.
    var bubbleLayout = {
      title: "Bacteria Cultures Per Sample",
      margin: { t: 0 },
      hovermode: "closest",
      xaxis: { title: "OTU ID" },
      margin: { t: 30}
    };
    // 3. Use Plotly to plot the data with the layout.
    Plotly.newPlot("bubble", bubbleData, bubbleLayout);
   // 4. Create the trace for the gauge chart.
   var gaugeData = [{
    domain: { x: [0, 1], y: [0, 1] }, 
    title: { text: "<b>Belly Button Washing Frequency</b> <br> Scrubs per Week"},
    value: frequency,
    type: "indicator",
    mode: "gauge+number",
    gauge: {
       
      axis: {range: [null, 10]},
      bar: {color: "black"},
      steps: [
        {range: [0,2], color: "red"},
        {range: [2,4], color: "orange"},
        {range: [4,6], color: "yellow"},
        {range: [6,8], color: "limegreen"},
        {range: [8,10], color: "green"}
      ]
  }}];
   
  
  // 5. Create the layout for the gauge chart.
  var gaugeLayout = {
    width: 500,
    height: 400,
    margin: {t: 25, r: 25, l: 25, b: 25},
    paper_bgcolor: "White",
    font: {color: "black", family: "Helvetica"}
  };

// 6. Use Plotly to plot the gauge data and layout.
Plotly.newPlot("gauge", gaugeData, gaugeLayout);     
  });

 
};