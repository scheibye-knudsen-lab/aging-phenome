features_zscore <- read.table("../data/Zscore_file_95_terms.csv", header = T, sep = ";")

library(ape)
library(cluster) 

d <- dist(t(features_zscore))
h <- hclust(d)
# plot(as.phylo(h), type="fan", cex = 1)

library("treeio")
library("ggtree")

my_tree <- as.phylo(h)
write.tree(phy=my_tree, file="exported_tree.newick") # look for the file in your working directory

tree <- read.newick(file = "exported_tree.newick")
png(filename="../plots/cladogram.png", width = 2000, height = 2000)
ggtree(tree, layout="circular", branch.length="none") + geom_tiplab2(color='blue')
dev.off()