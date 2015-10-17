

setwd("/Volumes/HHD/Users/yun-shaosung/HDD_Doc/NYU/heuristic/problem4/")
locs = read.table("input_points.txt",sep="\t", header=F)

color <-c(1:length(locs[,3]))
color[locs[,3]>100]="gray"
color[locs[,3]>50 & locs[,3]<=100]="#4aaeee"
color[locs[,3]<=50]="#00ff00"

plot(locs[,1], locs[,2], col=color, pch=20)

