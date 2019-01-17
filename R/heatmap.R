library("pheatmap")
library("RColorBrewer")

features_zscore <- read.table("../data/Zscore_file_95_terms.csv", header = T, sep = ";")
# terms <- readLines("../data/Final_list_95_terms_capitalized_single_words.txt")
# colnames(features_zscore) <- terms

c <- c("#67001F", colorRampPalette(brewer.pal(n = 11, name = "RdBu"))(100), "#053061")
b <- c(-100, seq(-5, 5, 0.1), 100)

pheatmap(t(features_zscore),
         cluster_rows = TRUE,
         cluster_cols = TRUE,
         show_rownames = TRUE,
         show_colnames = FALSE,
         color = c,
         breaks = b, width = 20, height = 20, filename = "../plots/heatmap.jpeg")

write.table(t(features_zscore), sep = "\t", row.names = FALSE, col.names = FALSE, file = "vectors.tsv")
