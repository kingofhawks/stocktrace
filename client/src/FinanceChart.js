import React, {Component} from "react";
import Highcharts from 'highcharts';

export default class FinanceChart extends Component {
      constructor(props) {
        super(props);
        this.state = {
          options: null,
        };
        console.log("init***");
      }
  componentDidMount() {
          console.log("componentDidMount***");
          //remember the outer "this"
      var that = this;
      //only works for CH and FF
      let url = new URL(this.props.url);
        let params = new URLSearchParams(url.search.slice(1));
      console.log(params);
      //Iterate the search parameters.
    for (let p of params) {
      console.log(p);
    }
    let code = params.get('code');

      fetch(this.props.url).then(function(response){
          return response.json();
      }).then(function (data) {
          console.log(data);
        var averagePB = data['PB_avg'];
        var averagePE = data['PE_avg'];
        var options2 = {
            chart: {
                zoomType: 'x'
            },
            title: {
                text: 'Finance chart over time '+code
            },
            subtitle: {
                text: document.ontouchstart === undefined ?
                        'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
            },
            xAxis: {
                type: 'datetime'
            },
            yAxis: [
                {
                    title: {
                        text: 'PB'
                    },
                    plotLines: [{
                    color: '#000',
                    dashStyle: 'Solid', //Dash,Dot,Solid,默认Solid
                    width: 1.5,
                    value: averagePB,
                    zIndex: 5,
                    label: {
                        text: 'PB:'+averagePB,
                        align: 'center',
                        style: {
                            color: 'blue'
                        }
                    }
                }]
                },
                {
                    title: {
                        text: 'PE'
                    },
                    plotLines: [{
                    color: 'black',
                    dashStyle: 'Dash', //Dash,Dot,Solid,默认Solid
                    width: 1.5,
                    value: averagePE,
                    zIndex: 5,
                    label: {
                        text: 'PE:'+averagePE,
                        align: 'center',
                        style: {
                            color: 'black'
                        }
                    }
                }],
                    opposite: true //right-side y-axis
                }],
            legend: {
                layout: 'vertical',
                align: 'left',
                x: 80,
                verticalAlign: 'top',
                y: 55,
                floating: true,
                backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'
            },
            plotOptions: {
                area: {
                    fillColor: {
                        linearGradient: {
                            x1: 0,
                            y1: 0,
                            x2: 0,
                            y2: 1
                        },
                        stops: [
                            [0, Highcharts.getOptions().colors[0]],
                            [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                        ]
                    },
                    marker: {
                        radius: 2
                    },
                    lineWidth: 1,
                    states: {
                        hover: {
                            lineWidth: 1
                        }
                    },
                    threshold: null
                },
                series:{
                    turboThreshold:5000//set it to a larger threshold, it is by default to render 1000 points
                }
            },
            series: [{
                type: 'line',
                name: 'PB',
                data: data['PB']
            },{
                type: 'line',
                name: 'PE',
                yAxis: 1,
                data: data['PE']
            }]
        }
        that.setState({options: options2});
        console.log(that.state.options);
        that.chart = new Highcharts[that.props.type || 'Chart'](
          that.chartEl,
          that.state.options
    );
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  componentWillUnmount() {
    this.chart.destroy();
  }

  render() {
    return <div ref={el => (this.chartEl = el)} />;
  }
}