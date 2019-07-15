library(pvclust)
library(rjson)

labels = c('Hutchinson Gilford','Bloom syndrome','Cockayne syndrome','Fanconi anemia','Rothmund-Thomson','Werner syndrome','Ataxia-telangiectasia','Trichothiodystrophy','Nijmegen breakage syndrome','Aging','Dyskeratosis congenita','XPA','ADOA','MELAS','MERRF','Alkaptonuria', 'Marfan syndrome', 'Ehlers Danlos syndrome', 'Seckel syndrome')

result <- fromJSON(file = "../data/figure_4a.json")
json_data_frame <- as.data.frame(result)
names(json_data_frame) = labels
aging = t(json_data_frame)

result <- pvclust(t(aging), method.dist="uncentered", method.hclust="average", nboot=1000)

dev.off()
png("../plots/pvclust_figure_4A.png", width = 2000, height = 2000)
plot(result)
dev.off()
