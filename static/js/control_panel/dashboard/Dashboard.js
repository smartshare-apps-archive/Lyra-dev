$(document).ready(function(){
	scalePlots();
});

function scalePlots(){
	
    var plot = Bokeh.Collections("Plot").models[0];
	    plot.set("plot_width", $(window).width());
	    plot.set("plot_height", $(window).height());

}