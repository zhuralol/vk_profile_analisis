// <div id="mynetwork"></div>
// cdnjs https://visjs.github.io/vis-network/standalone/umd/vis-network.min.js

var DIR = "img/soft-scraps-icons/";

var nodes = null;
var edges = null;
var network = null;

// Called when the Visualization API is loaded.
function draw() {
  // create people.
  // value corresponds with the age of the person
  var DIR = "../img/indonesia/";
  nodes = [
    { id: 1, shape: "image", image: "https://sun9-2.userapi.com/c848524/v848524775/8249b/u7czxpksecA.jpg?ava=1", label: "Vladimir Zhuravlev" },
    { id: 2, shape: "image", image: DIR + "2.png" },
    { id: 3, shape: "image", image: DIR + "3.png" },
    { id: 4, shape: "image", image: DIR + "4.png", label: "pictures by this guy!"},
    { id: 5, shape: "image", image: DIR + "5.png" },
    { id: 6, shape: "image", image: DIR + "6.png" },
    { id: 7, shape: "image", image: DIR + "7.png" },
    { id: 8, shape: "image", image: DIR + "8.png" },
    { id: 9, shape: "image", image: DIR + "9.png" },
    { id: 10, shape: "image", image: DIR + "10.png" },
    { id: 11, shape: "image", image: DIR + "11.png" },
    { id: 12, shape: "image", image: DIR + "12.png" },
    { id: 13, shape: "image", image: DIR + "13.png" },
    { id: 14, shape: "image", image: DIR + "14.png" }
  ];

  // create connections between people
  // value corresponds with the amount of contact between two people
  edges = [
    { from: 1, to: 2 },
    { from: 2, to: 3 },
    { from: 2, to: 4 },
    { from: 4, to: 5 },
    { from: 4, to: 10 }.
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
        border: "#406897",
        background: "#6AAFFF"
      },
      font: { color: "#eeeeee" },
      shapeProperties: {
        useBorderWithImage: true
      }
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
