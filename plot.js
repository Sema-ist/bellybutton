function loadSelector() {  
  Plotly.d3.json("/names", function(error, response) {
    
    for (var i=0; i<response.length; i++) {
      var selector = document.getElementById("selDataset");
      var option = document.createElement("option");
      var name = response[i];
        
      option.append(name);
      selector.append(option, {value : name});
    }
  });
}