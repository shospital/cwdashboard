// references
// https://www.createwithdata.com/chartjs-and-csv/
//http://learnjsdata.com/combine_data.html combining data


// *************** UTILITY FUNCTIONS ***************** //
// ****** MODIFY WITH CAUSTION AS IT MAY BE DEPENDENCIES IN THE DATA SECTION *** //
// returns unique indices
function onlyUnique(value, index, array) {
    return array.indexOf(value) === index;
    }


function sortArrays(arrays, comparator = (a, b) => (a > b) ? -1 : (a < b) ? 1 : 0) {
    let arrayKeys = Object.keys(arrays);
    let sortableArray = Object.values(arrays)[0];
    let indexes = Object.keys(sortableArray);
    let sortedIndexes = indexes.sort((a, b) => comparator(sortableArray[a], sortableArray[b]));

    let sortByIndexes = (array, sortedIndexes) => sortedIndexes.map(sortedIndex => array[sortedIndex]);

    if (Array.isArray(arrays)) {
        return arrayKeys.map(arrayIndex => sortByIndexes(arrays[arrayIndex], sortedIndexes));
    } else {
        let sortedArrays = {};
        arrayKeys.forEach((arrayKey) => {
            sortedArrays[arrayKey] = sortByIndexes(arrays[arrayKey], sortedIndexes);
        });
        return sortedArrays;
    }
}



// ******************* COASTWATCH DATA FUNCTIONS ******************//
// ***** DATA FORMATTING FOR TOTAL REQUEST BY ID ***** //

// requests by id sorted desc
// called from getStats
function ReqbyId(data){
    var result = [];
    data.reduce(function(res, value) {
        if(!res[value.dataset_id]) {
            res[value.dataset_id] = {id: value.dataset_id, requests: parseInt(value.requests)};
            result.push(res[value.dataset_id])
        }

        res[value.dataset_id].requests += parseInt(value.requests);
        return res;
    }, {});

    let result_sorted = result.sort((d1, d2) => (parseInt(d1.requests) < parseInt(d2.requests)) ? 1 : (parseInt(d1.requests) > parseInt(d2.requests)) ? -1 : 0);
    return result_sorted;
}


// **** DATA FORMATTING for REQUESTS BY FORMAT ******
// called from getStats
function byFormat(data) {
    let result = [];
    text_reqs = 0;
    nc_reqs =0;
    dods_reqs =0;
    metadata_reqs =0;
    graph_reqs =0;
    json_reqs =0;
    mat_reqs = 0;
    images_reqs=0;
    other_reqs=0;

   data.forEach(d => {

    text_reqs += parseInt(d.text_req);
    nc_reqs += parseInt(d.nc_req);
    dods_reqs += parseInt(d.dods_req);
    metadata_reqs += parseInt(d.metadata_req);
    graph_reqs += parseInt(d.graph_req);
    json_reqs += parseInt(d.json_req);
    mat_reqs += parseInt(d.mat_req);
    images_reqs += parseInt(d.images_req);
    other_reqs += parseInt(d.other_req);
});
  result.push(text_reqs,nc_reqs,dods_reqs, metadata_reqs, graph_reqs, json_reqs, mat_reqs, images_reqs, other_reqs);
  labels = ["Text", "NetCDF", "DoDs", "Metadata", "Graph", "JSON", "MAT", "Images", "Other"];
return sortArrays(Array(result, labels));

}



// **** DATA FORMATTING for REQUESTS BY YEAR ******
// requests by id sorted desc
// called from getStats
function RequestbyYear(data){
    var result = [];
    data.reduce(function(res, value) {
        if(!res[value.year]) {
            res[value.year] = {year: value.year, requests: parseInt(value.requests)};
            result.push(res[value.year])
        }

        res[value.year].requests += parseInt(value.requests);
       // console.log(res);
        return res;
    }, {});

    let result_sorted = result.sort((d1, d2) => (parseInt(d1.year) > parseInt(d2.year)) ? 1 : (parseInt(d1.year) < parseInt(d2.year)) ? -1 : 0);
    return result_sorted;
}

function groupAndSum(arr, groupKeys, sumKeys){
    return Object.values(
      arr.reduce((acc,curr)=>{
        const group = groupKeys.map(k => curr[k]).join('-');
        acc[group] = acc[group] || Object.fromEntries(groupKeys.map(k => [k, curr[k]]).concat(sumKeys.map(k => [k, 0])));
        sumKeys.forEach(k => acc[group][k] += curr[k]);
        return acc;
      }, {})
    );
  }



function getHistStats(data) {
    var filtered_ds = data.filter(function(d) { return d.dataset_id !== "all_datsets" && d.dataset_id !== ''; });
    const sumByYearAndDataset = filtered_ds.reduce((acc, curr) => {
        const year = new Date(curr.time).getFullYear();
        if (!acc[year]) {
          acc[year] = {};
        }
        if (!acc[year][curr.dataset_id]) {
          acc[year][curr.dataset_id] = 0;
        }
        acc[year][curr.dataset_id] += curr.value;
        return acc;
      }, {});

//      barchart2(sumByYearAndDataset);
}

// creates table with the data and populates table with documentId
function requestTable(dat, header, documentId) {


    var table = '<table "table-bordered" id="dataTable" width="100%" cellspacing="0"><thead><tr>';

    header.forEach(h => table +='<th>'+h+'</th>');
    table+="</tr></thead>";

    table+="<tbody>";
    dat.forEach(d => {
        table+="<tr><td><a href='https://polarwatch.noaa.gov/erddap/info/"+d.id+"/index.html'>"+d.id+"</a></td><td>"+d.requests.toLocaleString()+"</td></tr>";
    })
    table += "</tbody></table>";
    document.getElementById(documentId).innerHTML = table;

}

function byFormatTable(dat, header,documentId) {

    var table = '<table "table-bordered" id="dataTable" width="100%" cellspacing="0"><thead><tr>';

    header.forEach(h => table +='<th>'+h+'</th>');
    table+="</tr></thead>";
    table+="<tbody>";
    for(let i = 0; i < dat[0].length; i++) {
        table+="<tr><td>"+dat[1][i]+"</a></td><td>"+dat[0][i].toLocaleString()+"</td></tr>";
    }
    table += "</tbody></table>";
    // document.getElementById(documentId).innerHTML = table;
    return table;
}

function getStats(data) {
    var filtered_ds = data.filter(function(d) { return d.dataset_id !== "all_datsets" && d.dataset_id !== ''; });
    var tot_requests = filtered_ds.reduce(function(sum, d) {return sum + parseInt(d.requests);}, 0);
    var active_ds = filtered_ds.filter(onlyUnique).length;
    var tot_downloads = filtered_ds.reduce(function(sum, d) {return sum + parseInt(d.data_volume);}, 0);

    // populating dashboard
    document.getElementById("no_ds").innerHTML= parseInt(active_ds).toLocaleString("en-US");
    document.getElementById("total_request").innerHTML= tot_requests.toLocaleString("en-US");
    document.getElementById("unique_users").innerHTML= parseInt(data[1].unique_visitors).toLocaleString("en-US");
    document.getElementById("total_fsize").innerHTML= parseFloat((tot_downloads / 976562).toFixed(2)).toLocaleString("en-US") + " GB";  // converting KiB to GB


    // charts

    // Top 10 datasets by datasetId
    let temp = ReqbyId(filtered_ds);
    let tot_req_id = temp.slice(0,10);
    let top5datIds = [];
    tot_req_id.forEach(temp => top5datIds.push(temp.dataset_id));
    barchart1(tot_req_id);
    requestTable(tot_req_id, ['Dataset ID', 'No of Requests'], 'byrequestTB');

    //request byFormat
    piechart1(byFormat(filtered_ds));
    console.log(byFormat(filtered_ds));
    byFormatTable(byFormat(filtered_ds), ['Requested Format', 'No of Requests'], 'byFormatTB');





// const start = Date.now();
// await functionToBeMeasured();
// const end = Date.now();
// console.log(`Execution time: ${end - start} msf`);
let filterto5 = filtered_ds.filter(x => {return top5datIds.includes(x.id)});
let reqbyYrTop5 = groupAndSum(filterto5, ['year', 'id'], ['requests']);


//barchart3(reqbyYrTop5);

}


d3.csv("polarwatch_erddap_output.csv").then(getStats);
//d3.csv("https://polarwatch.noaa.gov/erddap/tabledap/polarwatch_erddap_stats_monthly.csv?dataset_id%2Cdata_volume%2Crequests%2Cnc_req%2Cdods_req%2Ctext_req%2Cmetadata_req%2Cgraph_req%2Cjson_req%2Cmat_req%2Cimages_req%2Cother_req%2Cnc_size%2Cdods_size%2Ctext_size%2Cmetadata_size%2Cgraph_size%2Cjson_size%2Cmat_size%2Cimages_size%2Cother_size%2Cunique_visitors%2Ctime_epoch%2Ctime&time%3E=2023-02-08T00%3A00%3A00Z&time%3C=2023-02-15T12%3A00%3A00Z").then(getStats);
d3.csv("polarwatch_erddap_3yr.csv").then(getHistStats);
