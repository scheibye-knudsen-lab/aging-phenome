# install.packages("ape")
# install.packages("RColorBrewer")

library(ape)
library(RColorBrewer)

qual_col_pals = brewer.pal.info[brewer.pal.info$category == 'qual',]
col_vector = unlist(mapply(brewer.pal, qual_col_pals$maxcolors, rownames(qual_col_pals)))

f105 = read.csv("../data/Zscore/Zscore_105.csv", header = T, sep = ";")
f1050 = read.csv("../data/Zscore/Zscore_1050.csv", header = T, sep = ";")

# f105 = read.csv("../data/Tfidf/TFIDF_105.csv", header = T, sep = ";")
# f1050 = read.csv("../data/Tfidf/TFIDF_1050.csv", header = T, sep = ";")

paste(names(f1050), collapse = " ")

f = f1050[,names(f105)]
names(f) = gsub("\\.", " ", names(f))
names(f)[6] = "Decreased serum IGF-1"
names(f)[55] = "Alzheimer's disease"

d = dist(t(f))
h = hclust(d, method = "average")
p = as.phylo(h)
p$edge.length = rep(1, 208)
p$tip.label[h$order]

col_vector[2] = "#800080"
col_vector[3] = "#8B0000"
tipcolors = c(rep(col_vector[1], 13),
              rep(col_vector[2], 5),
              rep(col_vector[3], 11),
              rep(col_vector[15], 10),
              rep(col_vector[5], 13),
              rep(col_vector[6], 13),
              rep(col_vector[7], 2),
              rep(col_vector[8], 3),
              rep(col_vector[9], 5),
              rep(col_vector[10], 3),
              rep(col_vector[11], 7),
              rep(col_vector[12], 3),
              rep(col_vector[13], 13),
              rep(col_vector[14], 4))

tipcolors = cbind.data.frame(tipcolors, p$tip.label[h$order])
row.names(tipcolors) = p$tip.label[h$order]
tips = as.character(tipcolors[names(f),1])

# dev.off()
# png("fan_cladogram.png", width = 1000, height = 1000)
plot(p, cex = 0.72, type = "fan", rotate.tree = 45,
     edge.col = c(rep(col_vector[1], 26),
                  rep(col_vector[2], 10),
                  rep(col_vector[3], 22),
                  rep(col_vector[15], 19),
                  rep(col_vector[5], 26),
                  rep(col_vector[6], 27),
                  rep(col_vector[7], 4),
                  rep(col_vector[8], 5),
                  rep(col_vector[9], 11),
                  rep(col_vector[10], 6),
                  rep(col_vector[11], 13),
                  rep(col_vector[12], 7),
                  rep(col_vector[13], 25),
                  rep(col_vector[14], 7)), tip.color = tips)
# dev.off()
