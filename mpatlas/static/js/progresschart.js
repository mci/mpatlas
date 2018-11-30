define([
	'jquery',
	'backbone',
	// '/static/js/json/protected_percent.json!',
	'https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.6/d3.min',
	'https://cdnjs.cloudflare.com/ajax/libs/nvd3/1.8.1/nv.d3.min'
],
function ($, Backbone, d3, nvd3) {
    radialdata = [
    {
        value: 0.0261,
        color: "#23acc4",
        label: "Other MPAs 2.6%"
    },
    {
        value: 0.0223,
        color: "#46BFBD",
        label: "Strong Reserves 2.2%"
    },
    {
        value: 0.0127,
        color: "#a1dddc",
        label: "Pending MPAs 1.3%"
    },
    {
        value: 0.0126,
        color: "#bedbda",
        label: "Proposed MPAs 1.3%"
    },
    {
        value: 0.0263,
        color:"#ccc",
        label: "Unprotected 92.6%"
    }
]  
    var _ProgressChart = Backbone.View.extend({
		initialize: function() { },
		makeChart: function() {
			// Chart.js doughnut chart
			// Get context with jQuery - using jQuery's .get() method.
			// var radialctx = $("#radialChart").get(0).getContext("2d");
			// var radial = new Chart(radialctx).Doughnut(radialdata, {animationEasing : "easeOutQuart", animationSteps: 20, responsive: false});
			// var radiallegend = radial.generateLegend();
			// $('#radialLegend').html(radiallegend);
			

			// NVD3 doughnut chart
			nv.addGraph(function() {
			  var chart = nv.models.pieChart()
			    .x(function(d) { return d.label })
			    .y(function(d) { return d.value })
			    .showLabels(false)     //Display pie labels
			    .labelThreshold(.005)  //Configure the minimum slice size for labels to show up
			    .labelType("key") //Configure what type of data to show in the label. Can be "key", "value" or "percent"
			    .donut(true)          //Turn on Donut mode. Makes pie chart look tasty!
			    .donutRatio(0.45)     //Configure how big you want the donut hole size to be.
			    .labelsOutside(true)
			    .showLegend(true)
			    // .labelSunbeamLayout(true)
			    .cornerRadius(0)
			    .title('10% Target')
			    .titleOffset(-7)
			    // .width(200)
			    // .height(200)
			    .valueFormat(d3.format('.1%'))
			    ;

			  chart.pie
			    // make this a semicirlce
			    .startAngle(function(d) { return d.startAngle/3 -Math.PI/3 })
			    .endAngle(function(d) { return d.endAngle/3 -Math.PI/3 });

			  chart.legend
			    .updateState(false);

			  d3.select("#nvradialchart svg")
			    .datum(radialdata)
			    .transition().duration(350)
			    // .attr('width', 200)
			    // .attr('height', 200)
			    .call(chart);

			  /* Replace bullets with blocks */
			  d3.selectAll('#nvradialchart .nv-series').each(function(d,i) {
			    var group = d3.select(this),
			      circle = group.select('circle');
			    var color = circle.style('fill');
			    circle.remove();
			    var symbol = group.append('path')
			      .attr('d', d3.svg.symbol().type('square'))
			      .style('stroke', color)
			      .style('fill', color)
			      // ADJUST SIZE AND POSITION
			      // .attr('transform', 'scale(1.5) translate(-2,0)')
			  });

			  d3.selectAll('#nvradialchart .nv-pieWrap')
			    .attr('transform', 'scale(1.3) translate(-45,-20)');

			  d3.selectAll('#nvradialchart .nv-pie-title').each(function(d,i) {
			    d3.select(this).style('fill', '#000');
			  });

			  d3.selectAll('#nvradialchart .nv-pieWrap');


			  var defs = d3.select("#nvradialchart svg").append("defs");
			  var pattern = defs.append("pattern")
			      .attr({ id:"hash4_4", width:"8", height:"8", patternUnits:"userSpaceOnUse", patternTransform:"rotate(-45)"})
			      .append("rect")
			      .attr({ width:"4", height:"8", transform:"translate(0,0)", fill:"#ccc" });

			  /*
			  <defs xmlns="http://www.w3.org/2000/svg">
			    <pattern id="diagonalHatch" patternUnits="userSpaceOnUse" x="0" y="0" width="105" height="105">
			      <g style="fill:#a1dddc; stroke:#ccc; stroke-width:1">
			        <path d="M0 90 l15,15 M0 75 l30,30 M0 60 l45,45 M0 45 l60,60 M0 30 l75,75 M0 15 l90,90 M0 0 l105,105 M15 0 l90,90 M30 0 l75,75 M45 0 l60,60 M60 0 l45,45 M75 0 l30,30 M90 0 l15,15"/>
			      </g>
			    </pattern>
			  </defs>
			  */

			  return chart;
			});
		}
	});
	
	return {
		ProgressChart: _ProgressChart
	};
    // What we return here will be used by other modules
});
