

function get_requestTable(dat, header) {

  var table = '<table "table-bordered" id="dataTable" width="100%" cellspacing="0"><thead><tr>';

  header.forEach(h => table +='<th>'+h+'</th>');
  table+="</tr></thead>";

  // console.log(dat);
  table+="<tbody>";
  dat.titles.forEach((title, index) => {
    console.log('Label:', title, 'Data:', dat.data[index]);
    table+="<tr><td>"+dat.titles[index]+"</a></td><td>"+dat.data[index].toLocaleString()+"</td></tr>";
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
        hoverOffset: 4
      }]
    },
    options: {
      plugins: {
        colorschemes: {
          scheme: 'brewer.Paired12'
        }

      }

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
        hoverOffset: 4
      }]
    },
    options: {
      plugins: {
        colorschemes: {
          scheme: 'brewer.Paired12'
        }

      }

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
    indexAxis: 'y',
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
    plugins: {
      colorschemes: {
        scheme: 'brewer.Paired12'
      }

    }

  }

  });
      }
