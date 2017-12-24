#N <- 12
#ROUND <- 80
Plist <- c("10", "9", "8", "7", "6", "5", "4", "3", "2", "1", "0")
PTlist <- c("9", "8", "7", "6", "5", "4", "3", "2", "1")

for (P in Plist) {
  for (PT in PTlist) {
    rawjson <- rjson::fromJSON(file =
                                 paste("data/TftvsConst_12_5_80/points_",
                                       P,"_",PT,".json", sep=""))
    rawpjson <- rjson::fromJSON(file =
                                  paste("data/TftvsConst_12_5_80/pointsp_",
                                        P,"_",PT,".json", sep=""))
    
    Data <- as.data.frame(rawjson)
    Datap <- as.data.frame(rawpjson)
    
    #print(Data)
    
    p <- ggplot2::ggplot(Datap,
                         ggplot2::aes(x=Round,
                                 y=Points,
                                 group=categ,
                                 color=categ)
                         ) + ggplot2::geom_line(size=1.2)
    
    png(paste("data/TftvsConst_12_5_80/figs/",P,"_",PT,".png",sep=""))
    
    plot(p)
    
    dev.off()
  }
}