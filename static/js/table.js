// Return true if the object is a table, false otherwise
function isTable(tableObj) {
    return (tableObj.data.type == "table");
};

function match(tableWrapper, token, row, col) {
    var range = tableWrapper.dataCol[3].get(token);
    if (range != undefined) {
        var rowFlag = false;
        var colFlag = false;
        if (range[0][0] == "All" || range[0].indexOf(row) != -1) {
            rowFlag = true;
        }

        if (range[1][0] == "All" || range[1].indexOf(col) != -1) {
            colFlag = true;
        }

        if (rowFlag && colFlag) {
            return true;
        }
    }

    return false;
}
// Put values in the specific cell (both defined by dataObj); tableWrapper contains the taget table object.
function putInCell(tableWrapper, dataObj) {
    var myTable = tableWrapper.c3chart;
    var cellVal = dataObj.value;
    var cellColor = dataObj.color;
    var rowName = dataObj.row;
    var colName = dataObj.column;
    var rowIndex, colIndex;
    // get the index of these tagert row and column
    if (tableWrapper.dataCol[0].indexOf(rowName) != -1) {
        rowIndex = tableWrapper.dataCol[0].indexOf(rowName);
        colIndex = tableWrapper.dataCol[1].indexOf(colName);
    } else {
        rowIndex = tableWrapper.dataCol[1].indexOf(rowName);
        colIndex = tableWrapper.dataCol[0].indexOf(colName);
    }
    // assign value to the cell
    if (cellVal != "") {
        myTable.rows[1 + rowIndex].cells[colIndex].innerHTML = cellVal;
    }
    // assign background color to the cell
    if (cellColor != "") {
        myTable.rows[1 + rowIndex].cells[colIndex].bgColor = cellColor;
    }
};

// render HTML table based on the table object
function createTable(tableObj) {
    var tableID = tableObj.bindto.slice(1); // without #
    var myDiv = document.getElementById(tableID);
    var myTable = document.createElement('table');
    myTable.id = tableID + "table";
    var headerRow = myTable.insertRow(0);

    // below was to find the header array index
    var headerIndex = -1;
    var dataCol = tableObj.data.columns;
    var headerArrX = tableObj.data.x;
    for (var i = 0; i < dataCol.length; i++) {
        if (dataCol[i][0] == headerArrX) {
            headerIndex = i;
        }
    }
    // get column and row header arrays, and total row number
    if (headerIndex != -1) {
        var colHeaderArr = tableObj.data.columns[headerIndex];
        var rowHeaderArr = tableObj.data.columns[1 - headerIndex];
        var totalRows = rowHeaderArr.length + 1;
    }

    // set up table column header content
    for (var i = 0; i < colHeaderArr.length; i++) {
        var th = document.createElement('th');
        th.innerHTML = colHeaderArr[i];
        headerRow.appendChild(th);
    }

    // set up rows header content and fill up table eith empty cells
    for (var j = 1; j < totalRows; j++) {
        var row = myTable.insertRow(j);
        var cell = row.insertCell(0);
        cell.innerHTML = rowHeaderArr[j - 1];
        for (var m = 1; m < colHeaderArr.length; m++) {
            var cell = row.insertCell(m);
        }
    }
    // add it to HTML div section
    myDiv.appendChild(myTable);

    // add token validation
    if (tableObj.match != undefined) {
        var tokenMap = new Map();
        for (var i = 0; i < tableObj.match.table_token.length; i++) {
            var teamTokenObj = tableObj.match.table_token[i];
            var teamToken = (Object.keys(teamTokenObj))[0];
            tokenMap.set(teamToken, teamTokenObj[teamToken]);
        }
    }
    chartMap.set(tableObj.bindto, new chartWrapper(tableObj, document.getElementById(myTable.id), tableObj.data.columns));
    // add a new empty array(3rd arr) at the end of data columns for future new cell values
    chartMap.get(tableObj.bindto).dataCol.push([]);
    chartMap.get(tableObj.bindto).dataCol.push(tokenMap);     //4 th stuff in arr
    return myTable;
};