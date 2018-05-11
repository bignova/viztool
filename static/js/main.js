var chartMap = new Map();

// create a new object that contains 3 objects: userChart object (the one from hub), and generated chart/table,
// and the data.columns field (two dimensional array) in userChart object
function chartWrapper(chartObject, c3chart, dataCol) {
    this.userChartObj = chartObject;
    this.c3chart = c3chart;
    this.dataCol = dataCol;
}

// This function will be called upon page load. It will set a new div section for the current graph object(if it doesn't have one yet) with the same ID it has,
// and geenrate such graph object and store its chart object and data in chartMap.
function setUpDivMap(userChartObj) {
    var mychartID = userChartObj.bindto;    // with '#', use this as KEY in the chartMap
    var mychartHTMLid = (mychartID).slice(1);   //without '#', use this to find element in HTML

    // create a new div with id=mychartHTMLid if it doesnt' exit yet,
    // also add epty space before and after the div
    if (!document.getElementById(mychartHTMLid)) {
        var brr = document.createElement("BR");
        document.body.appendChild(brr);
        document.body.appendChild(brr);
        var ele = document.createElement("div");
        ele.setAttribute("id", mychartHTMLid);
        document.body.appendChild(ele);
        var space = document.createElement("BR");
        document.body.appendChild(space);
        document.body.appendChild(space);
    }

    if (chartMap.get(mychartID) == undefined) {
        // generate chart/table, and store rendered chart/table and aassociated data in the chartMap
        switch (userChartObj.data.type) {
            case "table":
                createTable(userChartObj);
                break;
            case "flow":
                createFlow(userChartObj);
                break;
            case "map":
                createMap(userChartObj);
                break;
            default:
                var mychart = initChartObj(userChartObj);
                chartMap.set(userChartObj.bindto, new chartWrapper(userChartObj, mychart, userChartObj.data.columns));

                // below two lines are magic words that fixes c3 style error. Do not worry.
                d3.selectAll("path").attr("fill", "none");
                d3.selectAll(".tick line, path.domain").attr("stroke", "black");

                // If it is a C3 chart object, we create a transform list at the bottom of the chart
                var transText = document.createTextNode("Transform to ");
                document.getElementById(mychartHTMLid).appendChild(transText);
                var optionArr = ["area", "bar", "line", "pie", "spline"];

                var selectList = document.createElement("select");
                selectList.id = mychartHTMLid + "mySelect";
                document.getElementById(mychartHTMLid).appendChild(selectList);

                //Create and append the options
                for (var i = 0; i < optionArr.length; i++) {
                    var option = document.createElement("option");
                    option.value = optionArr[i];
                    option.text = optionArr[i];
                    selectList.appendChild(option);
                }
                // select on change function
                selectList.onchange = function () {
                    var chartType = selectList.value;
                    var currChart = chartMap.get(mychartID).c3chart;
                    currChart.transform(chartType);
                };
                break;
        };
    }

}

// return the index of such name in the dataColumn array, return -1 upon not found
function indexInDataCol(wrapperObj, dataName) {
    var dataCol = wrapperObj.dataCol;
    for (var i = 0; i < dataCol.length; i++) {
        if (dataCol[i][0] == dataName) {
            return i;
        }
    }
    return -1;
};

// generate c3 chart and return it
function initChartObj(chartObj) {
    var chart = c3.generate(chartObj);
    return chart;
}

function loadCharts(updateGraphArr) {
    // below two lines are magic words that fixes c3 style error. Do not worry.
    d3.selectAll("path").attr("fill", "none");
    d3.selectAll(".tick line, path.domain").attr("stroke", "black");

    var updateGraphObj = JSON.parse(updateGraphArr);

    var chartID = '#' + updateGraphObj.graph_name;
    var dataNameArr = Object.keys(updateGraphObj.data);
    var currChartWrapper = chartMap.get(chartID);


    switch (currChartWrapper.userChartObj.data.type) {
        case "table":
            if ((updateGraphObj.data.table_token == undefined) || match(currChartWrapper, updateGraphObj.data.table_token, updateGraphObj.data.row, updateGraphObj.data.column)) {
                currChartWrapper.dataCol[2].push(updateGraphObj.data);   // store new cell val to its data array in map
                putInCell(currChartWrapper, updateGraphObj.data);
            }
            break;
        case "flow":
            updateFlow(currChartWrapper, updateGraphObj);
            break;
        case "map":
            updateMarker(currChartWrapper, updateGraphObj);
            break;
        default:
            // put data in to wrapper dataCol
            for (var j = 0; j < dataNameArr.length; j++) {
                var dataName = dataNameArr[j];
                var newDataVal = updateGraphObj.data[dataName];
                // find the index of dataName arr in dataCol, then do: wrapper.dataCol[index].push(newDataVal);
                var dataIndex = indexInDataCol(currChartWrapper, dataName);
                if (dataIndex != -1) {
                    if (currChartWrapper.userChartObj.data.type == "gauge") {
                        // if chart is a gauge chart, only keep one value
                        currChartWrapper.dataCol[dataIndex].push(newDataVal);
                        currChartWrapper.dataCol[dataIndex].splice(1, 1);
                    } else {
                        // For other chart push new data in dataArr, keep fresh 10 data points
                        currChartWrapper.dataCol[dataIndex].push(newDataVal);
                        if (currChartWrapper.dataCol[dataIndex].length >= 11) {
                            currChartWrapper.dataCol[dataIndex].splice(1, 1);
                        }
                    }
                }
            }
            // after inner for-loop, all data pushed in, ready to load current chart
            currChartWrapper.c3chart.load({
                columns: currChartWrapper.dataCol
            });
            break;
    }
}