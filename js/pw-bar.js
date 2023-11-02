// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

let bgcolor5= [
  'rgba(255, 99, 132, 0.2)',
  'rgba(255, 159, 64, 0.2)',
  'rgba(255, 205, 86, 0.2)',
  'rgba(75, 192, 192, 0.2)',
  'rgba(54, 162, 235, 0.2)',
  'rgba(153, 102, 255, 0.2)',
  'rgba(201, 203, 207, 0.2)'
];

let brcolor5=  [
  'rgb(255, 99, 132)',
  'rgb(255, 159, 64)',
  'rgb(255, 205, 86)',
  'rgb(75, 192, 192)',
  'rgb(54, 162, 235)',
  'rgb(153, 102, 255)',
  'rgb(201, 203, 207)'
];



// Bar Chart : Top5 Total requests by Dataset ID
function barchart1(dat) {
    let ds = [];
    let labels = [];

    dat.forEach(d => {
        ds.push(d.requests);
        labels.push(d.id);
       });

    const dataTop10 = {
      labels,
      datasets: [{
        axis: 'y',
        label: 'No. of Requests',
        data: ds,
        fill: false,
        backgroundColor: [
        'rgba(255, 99, 132, 0.2)',
        'rgba(255, 159, 64, 0.2)',
        'rgba(255, 205, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(201, 203, 207, 0.2)',
        'rgba(255, 99, 132, 0.2)',
        'rgba(255, 159, 64, 0.2)',
        'rgba(255, 205, 86, 0.2)'
        ],
        borderColor: [
          'rgb(255, 99, 132)',
          'rgb(255, 159, 64)',
          'rgb(255, 205, 86)',
          'rgb(75, 192, 192)',
          'rgb(54, 162, 235)',
          'rgb(153, 102, 255)',
          'rgb(201, 203, 207)',
          'rgb(255, 99, 132)',
          'rgb(255, 159, 64)',
          'rgb(255, 205, 86)'
        ],

        borderWidth: 1,
        maxBarThickness: 60,
      }]
    };

      const config = {
        type: 'horizontalBar',
        data: dataTop10,
        options: {
          indexAxis:'y',
          layout: {
            padding: {
              left: 10,
              right: 10,
              top: 10,
              bottom: 10
            },
            plugins: {
              legend: {
                hidden: true
              }
            }
          },
        }
      };


    //
    new Chart( document.getElementById('BarChartTop10'), config);

  }


function barchart2(dat) {
  let ds = [];
  let labels = [];

  dat.forEach(d => {
      ds.push(d.requests);
      labels.push(d.year);
     });

  const reqbyyear = {
    labels,
    datasets: [{
      axis: 'y',
      label: 'Total Request',
      data: ds,
      fill: false,
      backgroundColor:
      'rgba(255, 159, 64, 0.2)',
      borderColor:   'rgb(255, 159, 64)',
      borderWidth: 1,
      maxBarThickness: 70,
    }]
  };

    const config = {
      type: 'bar',
      data: reqbyyear,
      options: {
        indexAxis:'y',
        layout: {
          padding: {
            left: 50,
            right: 50,
            top: 25,
            bottom: 50
          }
        },
      }
    };


 // new Chart( document.getElementById('Request5YearID'), config);
}



function barchart3(dat) {



 let labels = [...new Set(dat.map((item) => item.year))].sort();
 let uniqueIds = [...new Set(dat.map((item) => item.id))];

  let datasets = [];
  uniqueIds.forEach(i => {

    let tdata = [];
    labels.forEach(y=>  {
      let req= dat.filter(d=>d.id == i && d.year == y);
      if(req.length>0) tdata.push(req[0].requests)
      else {tdata.push(0);}
    })
    datasets.push({label: i, data: tdata, backgroundColor: bgcolor5.pop(),  borderColor: 'rgba(201,203,207,02)'});
  })




const data = {
  labels,
  datasets,
};


  const config = {
    type: 'bar',
    data,
    options: {
      plugins: {
        title: {
          display: true,
          text: 'Chart.js Bar Chart - Stacked'
        },
      },
      layout: {
        padding: {
          left: 0,
          right: 0,
          top: 25,
          bottom: 40
        },
      },
      responsive: true,
      interaction: {
        intersect: false,
      },
      scales: {
        x: {
          stacked: true,
        },
        y: {
          stacked: true
        }
      }
    }
  };


     new Chart( document.getElementById('Request5YearID'), config);


}
