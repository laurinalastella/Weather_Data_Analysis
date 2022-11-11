// getting references
var country_field = d3.select("#country");
var location_field = d3.select("#location");
var start_date_field = d3.select("#start_date");
var end_date_field = d3.select("#end_date");
var the_button = d3.select("#get_links");
var history_link_thing = d3.select("#history-link");
var seasons_link_thing = d3.select("#seasons-link");

// global variables to hold 4 inputs - i'm sure this is kludge
var country_val = "";
var location_val = "";
var start_date_val = "";
var end_date_val = "";

// functions linking input fields to their variables
country_field.on("change", function() {
    country_val = d3.event.target.value;
    console.log("country", country_val);
  });

  location_field.on("change", function() {
    location_val = d3.event.target.value;
    console.log("location", location_val);
  });

  start_date_field.on("change", function() {
    start_date_val = d3.event.target.value;
    console.log("start date", start_date_val);
  });

  end_date_field.on("change", function() {
    end_date_val = d3.event.target.value;
    console.log("end date", end_date_val);
  });

// the function that fills urls
the_button.on("click", function() {
    var urrl = country_val + "/" + location_val + "/" + start_date_val + "/" + end_date_val;
    history_link_thing.attr("href", "history/"+urrl );
    seasons_link_thing.attr("href", "seasons/"+urrl );
});










