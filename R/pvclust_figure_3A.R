library(pvclust)

f105 = read.csv("../data/Zscore/Zscore_105.csv", header = T, sep = ";")
f1050 = read.csv("../data/Zscore/Zscore_1050.csv", header = T, sep = ";")

paste(names(f1050), collapse = " ")

f = f1050[,names(f105)]
names(f) = gsub("\\.", " ", names(f))
names(f)[6] = "Decreased serum IGF-1"
names(f)[55] = "Alzheimer's disease"

aging = f

result <- pvclust(aging, method.dist="euclidean", method.hclust="average", nboot=100)
dev.off()
png("../plots/pvclust_figure_3A.png", width = 2000, height = 2000)
plot(result)
dev.off()

