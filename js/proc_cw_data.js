const dpath = 'js/data.json'

async function fetchData(url) {
    try {
        const response = await fetch(url);
        if(!response.ok) {
            throw new Error(`Error Status: ${response.status}`);
        }
        return await response.json()
    } catch(error) {
        console.error("Could not fetch data: ", error);
    }
}



fetchData(dpath).then(data => {
    if (data) {

        console.log(data.stats.active_ds)
        document.getElementById("total_request").innerHTML= data.stats.tot_req.toLocaleString("en-US");
        document.getElementById("unique_users").innerHTML= data.stats.tot_users.toLocaleString("en-US");
        document.getElementById("no_ds").innerHTML= data.stats.active_ds.toLocaleString("en-US");
        document.getElementById("byrequestTB").innerHTML = get_requestTable(data.stats.top10_reqs, ['Dataset Name', 'No of Requests']);

        // requestTable(tot_req_id, ['Dataset ID', 'No of Requests'], 'byrequestTB');
       // var ctx = document.getElementById('BarChartTop101').getContext('2d');
        //barchart1(ctx, data.stats.top10_reqs);
        var ctx1 = document.getElementById('BarChartTop10').getContext('2d');
        var ctx2 = document.getElementById('PieChart_Ftype').getContext('2d');
        var ctx3 = document.getElementById('PieChart_Ftype_size').getContext('2d');
        // Add barchart of top 10 requests

        barchart1(ctx1, data.stats.top10_reqs);
        piechart1(ctx2, data.stats.file_by_req);
        piechart2(ctx3, data.stats.file_by_size);
    }
});


function get_requestTable(dat, header) {

  var table = '<table "table-bordered" id="dataTable" width="100%" cellspacing="0"><thead><tr>';

  header.forEach(h => table +='<th>'+h+'</th>');
  table+="</tr></thead>";

  // console.log(dat);
  table+="<tbody>";
  dat.labels.forEach((label, index) => {
    console.log('Label:', label, 'Data:', dat.data[index]);
    table+="<tr><td><a href='https://coastwatch.pfeg.noaa.gov/erddap/info/"+label+"/index.html'>"+dat.titles[index]+"</a></td><td>"+dat.data[index].toLocaleString()+"</td></tr>";
  });

  table += "</tbody></table>";

  return table;




}



function piechart1(ctx, dat) {
  var chart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: dat.labels,
      datasets: [{
        label: 'No of Requests',
        data: dat.data,
        backgroundColor: [
          'rgb(255, 99, 132)',
          'rgb(54, 162, 235)',
          'rgb(255, 205, 86)'
        ],
        hoverOffset: 4
      }]
    }
  })
}

function piechart2(ctx, dat) {
  var chart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: dat.labels,
      datasets: [{
        label: 'Download Size',
        data: dat.data,
        backgroundColor: [
          'rgb(255, 99, 132)',
          'rgb(54, 162, 235)',
          'rgb(255, 205, 86)'
        ],
        hoverOffset: 4
      }]
    }
  })
}

// Barchart on the main page
function barchart1(ctx, dat) {
  var chart = new Chart(ctx, {
  type: 'bar',
  data: {
      labels: dat.titles,

  datasets: [{
    axis: 'y',
    label: 'No. of Requests',
    data: dat.data,
    borderWidth: 1,
    maxBarThickness: 60,
    backgroundColor: [
      'rgba(126, 87, 194, 1)', // Opaque purple
      'rgba(92, 107, 192, 1)',  // Opaque indigo
      'rgba(66, 165, 245, 1)',  // Opaque blue
      'rgba(41, 182, 246, 1)',  // Opaque light blue
      'rgba(38, 198, 218, 1)',  // Opaque cyan
      'rgba(38, 166, 154, 1)',  // Opaque teal
      'rgba(102, 187, 106, 1)', // Opaque green
      'rgba(156, 204, 101, 1)', // Opaque light green
      'rgba(212, 225, 87, 1)',  // Opaque lime
      'rgba(255, 238, 88, 1)'   // Opaque yellow
    ]
  }]
  },
  options: {
    indexAxis: 'y'
    }
  });
      }


// function barchart1(ctx, data) {


//     var chart = new Chart(ctx, {
//   type: 'bar',
//   data: {
//     labels: data.labels
//     datasets: [1, 2, 3].map(function(i) {
//       return {
//         label: 'Dataset ' + i,
//         data: [0, 0, 0, 0, 0, 0, 0].map(Math.random),
//         fill: false
//       };
//     })
//   },
//   options: {
// plugins: {
//   colorschemes: {
//     scheme: 'brewer.SetOne4'
//   }
// }
// }
// });
//     }



//     labels = data.labels;

//     dataset = {
//         labels,
//         datasets: [{
//             axis: 'y',
//             label: 'No of requests',
//             data,
//             fill: false,
//             backgroundColor: ,
//             borderColor:,
//             borderWidth: 1,
//             maxBarThickness: 60,
//         }]
//     }
// }

// const dataTop10 = {
//     labels,
//     datasets: [{
//       axis: 'y',
//       label: 'No. of Requests',
//       data: ds,
//       fill: false,
//       backgroundColor: [
//       'rgba(255, 99, 132, 0.2)',
//       'rgba(255, 159, 64, 0.2)',
//       'rgba(255, 205, 86, 0.2)',
//       'rgba(75, 192, 192, 0.2)',
//       'rgba(54, 162, 235, 0.2)',
//       'rgba(153, 102, 255, 0.2)',
//       'rgba(201, 203, 207, 0.2)',
//       'rgba(255, 99, 132, 0.2)',
//       'rgba(255, 159, 64, 0.2)',
//       'rgba(255, 205, 86, 0.2)'
//       ],
//       borderColor: [
//         'rgb(255, 99, 132)',
//         'rgb(255, 159, 64)',
//         'rgb(255, 205, 86)',
//         'rgb(75, 192, 192)',
//         'rgb(54, 162, 235)',
//         'rgb(153, 102, 255)',
//         'rgb(201, 203, 207)',
//         'rgb(255, 99, 132)',
//         'rgb(255, 159, 64)',
//         'rgb(255, 205, 86)'
//       ],

//       borderWidth: 1,
//       maxBarThickness: 60,
//     }]
//   };
