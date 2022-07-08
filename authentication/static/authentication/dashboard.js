/* globals Chart:false, feather:false */

function loadJson(selector) {
  return JSON.parse(document.querySelector(selector).getAttribute('data-json'))
}

(() => {
  'use strict'

  feather.replace({ 'aria-hidden': 'true' })

  const timeFormat = 'DD/MM/YYYY'
  const jsonData = loadJson('#jsonData')
  const dataVals = jsonData.map(item => ({
    y: item.bench_max,
    x: (new Date(item.end_date)).toLocaleDateString('en-US')
  }))

  console.log(dataVals)

  // Graphs
  const ctx = document.getElementById('myChart')
  // eslint-disable-next-line no-unused-vars
  Chart.defaults.global.defaultFontColor = "#fff";
  const myChart = new Chart(ctx, {
    type: 'line',
    data: {
      datasets: [{
        data: dataVals,
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff'
      }]
    },
    options: {
      scales: {
        x: {
          type: 'time',
          displayFormats: {
            'millisecond': 'MMM DD',
            'second': 'MMM DD',
            'minute': 'MMM DD',
            'hour': 'MMM DD',
            'day': 'MMM DD',
            'week': 'MMM DD',
            'month': 'MMM DD',
            'quarter': 'MMM DD',
            'year': 'MMM DD',
          },
          time: {
            format: timeFormat,
          }
        },
      },
      legend: {
        display: false
      }
    }
  })
})()
