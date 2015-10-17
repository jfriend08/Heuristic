

setwd("/Volumes/HHD/Users/yun-shaosung/HDD_Doc/NYU/heuristic/problem4/")
locs = read.table("input_points.txt",sep="\t", header=F)
locs = read.table("/Volumes/HHD/Users/yun-shaosung/HDD_Downloads/ambusamp2010.txt",sep=",", header=F)

color <-c(1:length(locs[,3]))
color[locs[,3]>100]="#5bb300"
color[locs[,3]>50 & locs[,3]<=100]="#ffc04c"
color[locs[,3]<=50]="#ff0000"

filename<- sprintf("Scattered_%sPoints.pdf", nrow(locs)) 
pdf(filename, width = 5, height = 5)
plot(locs[,1], locs[,2], col=color, pch=20)
points(12,36, col="red", pch="*", cex=2)
points(83,27, col="red", pch="*", cex=2)
points(45,27, col="red", pch="*", cex=2)
points(77,77, col="red", pch="*", cex=2)
points(26,78, col="red", pch="*", cex=2)

#points(5.103190, 6.505942, col="#00e600", pch="*", cex=2)
#points(19.646614, 16.090233, col="#00e600", pch="*", cex=2)
#points(10.642010, 21.195509, col="#00e600", pch="*", cex=2)
#points(0.792619, 1.949866, col="#00e600", pch="*", cex=2)
#points(11.437430, 2.638066, col="#00e600", pch="*", cex=2)
dev.off()
