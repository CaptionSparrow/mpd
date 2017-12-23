N <- 4
ROUND <- 20

rawjson <- rjson::fromJSON(file = "data/points.json")
rawpjson <- rjson::fromJSON(file = "data/pointsp.json")

Data <- as.data.frame(rawjson)
Datap <- as.data.frame(rawpjson)

print(Data)

ggplot2::ggplot(Datap,
                ggplot2::aes(x=Round,
                             y=Points,
                             group=categ,
                             color=categ)
                ) + ggplot2::geom_line(size=1.2)