/* globals Chart:false, feather:false */

(() => {
  'use strict'

  feather.replace({ 'aria-hidden': 'true' })

  // Graphs
  const ctx = document.getElementById('myChart')
  // eslint-disable-next-line no-unused-vars
  Chart.defaults.global.defaultFontColor = "#fff";
  const myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [
        '5/22-5/28',
        '5/29-6/4',
        '6/5-6/11',
        '6/12-6/18',
        '6/19-6/25',
        '6/26-7/2',
        '7/3-7/9'
      ],
      datasets: [{
        data: [
          225,
          225,
          230,
          235,
          235,
          235,
          245
        ],
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff'
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: false
          }
        }]
      },
      legend: {
        display: false
      }
    }
  })
})()
