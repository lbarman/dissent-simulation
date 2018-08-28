.PHONY: all
all:
	echo "Please manually fill datapoints.json"
	node plot.js > dissent.gnudata
	gnuplot script.gnuplot 
	epstopdf prifi-dissent.eps