var nodes = null;
var edges = null;
var network = null;

// Called when the Visualization API is loaded.
function draw() {
  // create people.
  // value corresponds with the age of the person
  //var flaskimage = JSON.parse($("#mydiv").data("flask_image"));
  nodes = [
    { id: 1, shape: "circularImage", image: {{ url_for('static', filename='img/1.jpg') }} },
    { id: 2, shape: "circularImage", image: "2.png" },
    { id: 3, shape: "circularImage", image: "3.png" }
    ];

  // create connections between people
  // value corresponds with the amount of contact between two people
  edges = [
    { from: 1, to: 2 },
    { from: 2, to: 3 },
    { from: 1, to: 3 }
  ];

  // create a network
  var container = document.getElementById("mynetwork");
  var data = {
    nodes: nodes,
    edges: edges
  };
  var options = {
    nodes: {
      borderWidth: 4,
      size: 30,
      color: {
        border: "#222222",
        background: "#666666"
      },
      font: { color: "#eeeeee" }
    },
    edges: {
      color: "lightgray"
    }
  };
  network = new vis.Network(container, data, options);
}

window.addEventListener("load", () => {
  draw();
});
