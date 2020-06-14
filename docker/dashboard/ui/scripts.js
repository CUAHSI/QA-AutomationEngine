
function setLastUpdated(name, index) {
    return $.ajax({
        url:`/${name}/timestamp.txt`,
    }).then(data => {
        document.getElementsByClassName('last-updated')[index].innerHTML = `Last updated: ${data.trim()}&nbsp;UTC`;
    });
}

function compileData(name, index) {
    setLastUpdated(name, index);
    let run = $.ajax(`/${name}/run.txt`);
    let result = $.ajax(`/${name}/result.txt`);
    Promise.all([run, result]).then((values) => {
        setChart(
            index,
            {
                count: parseInt(values[0].match(/Ran ([0-9]*) tests/)[1]),
                failures: parseInt(values[1].match(/failures=([0-9]*)/)[1]),
                errors: parseInt(values[1].match(/errors=([0-9]*)/)[1])
            }
        )
    });
}

function setChart(index, results) {
    const chart = echarts.init(document.getElementsByClassName('results-stateless')[index]);
    let passRate = (100*(1-(results['failures']+results['errors'])/results['count'])).toPrecision(3)
    let data = [
        {name: "SUCCESS", value: results['count']-results['failures']-results['errors']},
        {name: "FAILURE", value: results['failures']},
        {name: "ERROR", value: results['errors']}
    ];

    (function renderChart() {
        chart.setOption(getChartOptions());
    })();

    function getChartOptions() {
        return {
            tooltip: {
                trigger: 'item',
                formatter: '{b}: {c}'
            },
            title: {
                text: passRate + `%\nPass Rate`,
                textStyle: {
                    fontSize: 'min(1.3rem)',
                    fontWeight: 'bold',
                },
                show: true,
                left: '32%',
                top: '37%',
                textAlign: 'center'
            },
            legend: {
                show: true,
                type: 'scroll',
                orient: 'vertical',
                top: 'middle',
                left: '65%',
                height: '85%',
                align: 'left',
                icon: 'circle',
                textStyle: {
                    fontSize: '12'
                }
            },
            series: [
                {
                    label: {
                        show: false,
                    },
                    minAngle: 3,
                    type: 'pie',
                    radius: ['55%', '85%'],
                    avoidLabelOverlap: true,
                    labelLine: {
                        show: false
                    },
                    width: '65%',
                    data: data,
                }
            ],
            color: ['#2f4554', '#c23531', '#d48265', '#91c7ae','#749f83',  '#ca8622', '#bda29a','#6e7074', '#546570', '#61a0a8', '#c4ccd3']
        };
    }

    window.addEventListener('resize', () => {
        chart.resize();
    });
}

window.addEventListener('DOMContentLoaded', function () {
    compileData("beta", 0);
})
