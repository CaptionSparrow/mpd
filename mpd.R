N <- 4
ROUND <- 5

rawjson <- rjson::fromJSON(file = "data/points.json")
rawpjson <- rjson::fromJSON(file = "data/pointsp.json")

Data <- as.data.frame(rawjson)
Datap <- as.data.frame(rawpjson)

print(Data)

ggplot2::ggplot(Datap[1:N*ROUND,],
                ggplot2::aes(x=x.label[1:N*ROUND],
                             y=Data[1:N*ROUND],
                             group=categ[1:N*ROUND],
                             color=categ[1:N*ROUND])
                ) + ggplot2::geom_line(size=1.2)