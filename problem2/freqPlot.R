out<-read.table('/Volumes/HHD/Users/yun-shaosung/HDD_Doc/NYU/heuristic/problem2/out.txt', header = FALSE, sep = "\t")
out<-t(out)

hist(out, breaks=20, main="Breaks=20")

plot(as.matrix(out))
