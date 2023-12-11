// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// DOUNUT CHART FOR REQUEST BY FORMAT
//
function piechart1(dat) {
    const data = {
      labels: dat[1],
      datasets: [{
        axis: 'y',
        label: 'Total Request',
        data: dat[0],
        fill: false,
        backgroundColor: [
          'rgba(255, 99, 132, 0.2)',
          'rgba(255, 159, 64, 0.2)',
          'rgba(255, 205, 86, 0.2)',
          'rgba(75, 192, 192, 0.2)',
          'rgba(54, 162, 235, 0.2)',
          'rgba(153, 102, 255, 0.2)',
          'rgba(201, 203, 207, 0.2)'
        ],
        borderColor: [
          'rgb(255, 99, 132)',
          'rgb(255, 159, 64)',
          'rgb(255, 205, 86)',
          'rgb(75, 192, 192)',
          'rgb(54, 162, 235)',
          'rgb(153, 102, 255)',
          'rgb(201, 203, 207)'
        ],
        borderWidth: 1,
        maxBarThickness: 40,
      }]
    };

      const config = {
        type: 'doughnut',
        data,
        options: {
          indexAxis:'y',
          layout: {
            padding: {
              left: 10,
              right: 25,
              top: 25,
              bottom: 50
            }
          },
        }
      };


    new Chart( document.getElementById('ChartByFormat'), config);
}
