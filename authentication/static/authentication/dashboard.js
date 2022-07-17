/* globals Chart:false, feather:false */

function loadJson(selector) {
  return JSON.parse(document.querySelector(selector).getAttribute('data-json'))
}

function newDate(days) {
  return moment().add(days, 'd');
}

(() => {
  'use strict'

  feather.replace({ 'aria-hidden': 'true' })

  const user = document.querySelector('#userData').getAttribute('data-json')
  const jsonData = loadJson('#jsonData')

  const filteredData = jsonData.filter(item => item.user == user)
  const dataVals = filteredData.map(item => ({x: new Date(item.end_date).getTime(), y: item.bench_max}))

  // Graphs
  const ctx = document.getElementById('myChart')
  // eslint-disable-next-line no-unused-vars
  Chart.defaults.global.defaultFontColor = "#fff"
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
        xAxes: [{
          type: 'time',
          time: {
            displayFormats: {
               'millisecond': 'MMM dd',
              'second': 'MMM dd',
              'minute': 'MMM dd',
              'hour': 'MMM dd',
              'day': 'MMM dd',
              'week': 'MMM dd',
              'month': 'MMM dd',
              'quarter': 'MMM dd',
              'year': 'MMM dd',
            }
          }
        }],
      },
      legend: {
        display: false
      }
    }
  })
})()
