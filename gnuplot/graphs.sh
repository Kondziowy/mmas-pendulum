#!/bin/bash
if [ ! -e '../rower.dat' ] ; then
	echo -en "Run simulation before plotting\n"
	exit 1
fi
gnuplot < improvement > improvement.png
gnuplot < forces > forces.png
gnuplot < avg > avg.png
