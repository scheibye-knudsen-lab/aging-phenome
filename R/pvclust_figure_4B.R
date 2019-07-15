library(pvclust)

hallmarks = read.table("../data/Hallmark_Percentage_matrix_final.txt", h=T, sep = '\t', row.names = 1, stringsAsFactors = F)

aging = t(hallmarks)

result <- pvclust(aging, method.dist="uncentered", method.hclust="average", nboot=100)
dev.off()
png("../plots/pvclust_figure_4B.png", width = 2000, height = 2000)
plot(result)
dev.off()
