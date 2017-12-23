#N <- 12
#ROUND <- 80

rawjson <- rjson::fromJSON(file =
                             "data/TftvsConst_12_5_80/points_10_9.json")
rawpjson <- rjson::fromJSON(file =
                              "data/TftvsConst_12_5_80/pointsp_10_9.json")

Data <- as.data.frame(rawjson)
Datap <- as.data.frame(rawpjson)

#print(Data)

ggplot2::ggplot(Datap,
                ggplot2::aes(x=Round,
                             y=Points,
                             group=categ,
                             color=categ)
                ) + ggplot2::geom_line(size=1.2)