
function createFlow(flowObj) {
    var flowID = flowObj.bindto; // with #
    //set up svg for rendering
    d3.select(flowID).append("svg").attr("width", 960).attr("height", 600).append("g");

    //initialize the graph object
    var g = new dagre.graphlib.Graph();
    // Set an object for the graph label
    g.setGraph({});
    // Default to assigning a new object as a label for each new edge.
    g.setDefaultEdgeLabel(function () { return {}; });
    g.setDefaultNodeLabel(function () { return {}; });

    var isNode = (flowObj.data.columns[0][0]) == "node";
    var nodeArr = isNode ? flowObj.data.columns[0] : flowObj.data.columns[1];
    var edgeArr = isNode ? flowObj.data.columns[1] : flowObj.data.columns[0];

    //adds the nodes for the graph
    for (var i = 1; i < nodeArr.length; i++) {
        g.setNode(nodeArr[i]);
    }
    //add edges
    for (var j = 1; j < edgeArr.length; j++) {
        var arrowIndex = edgeArr[j].search("->");
        if (arrowIndex != -1) {
            var edgeStart = edgeArr[j].slice(0, arrowIndex);
            var edgeDest = edgeArr[j].slice(arrowIndex + 2);
        }
        g.setEdge(edgeStart, edgeDest);
    }

    dagre.layout(g);
    // Set up zoom support
    var svg = d3.select("svg"),
        inner = d3.select("svg g"),
        zoom = d3.zoom().on("zoom", function () {
            inner.attr("transform", d3.event.transform);
        });
    svg.call(zoom);

    // Set some general styles
    g.nodes().forEach(function (v) {
        var node = g.node(v);
        node.rx = node.ry = 5;
    });

    var render = dagreD3.render();
    // Render the graph into svg g
    d3.select("svg g").call(render, g);

    chartMap.set(flowObj.bindto, new chartWrapper(flowObj, g, flowObj.data.columns));
    return g;
}


function updateFlow(updateWrapper, updateObj) {
    var myg = updateWrapper.c3chart;
    switch (updateObj.data.operation) {
        case "addNode":
            myg.setNode(updateObj.data.target);
            break;
        case "updateNode":
            myg.setNode(updateObj.data.target, { label: updateObj.data.new_value });
            break;
        case "addEdge":
            var edgeTarget = updateObj.data.target;
            var arrowIndex = edgeTarget.search("->");
            if (arrowIndex != -1) {
                var edgeStart = edgeTarget.slice(0, arrowIndex);
                var edgeDest = edgeTarget.slice(arrowIndex + 2);
            }
            myg.setEdge(edgeStart, edgeDest);
            break;
        case "removeNode":
            myg.removeNode(updateObj.data.target);
            break;
        case "removeEdge":
            var edgeTarget = updateObj.data.target;
            var arrowIndex = edgeTarget.search("->");
            if (arrowIndex != -1) {
                var edgeStart = edgeTarget.slice(0, arrowIndex);
                var edgeDest = edgeTarget.slice(arrowIndex + 2);
            }
            myg.removeEdge(edgeStart, edgeDest);
            break;
    }

    // Set some general styles
    myg.nodes().forEach(function (v) {
        var node = myg.node(v);
        node.rx = node.ry = 5;
    });
    // Render the graph into svg g
    var render = dagreD3.render();
    d3.select("svg g").call(render, myg);
}