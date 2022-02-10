library(ggplot2)
library(lemon)

ext = 'png' # could also be eps

visualize <- function(filename, target, w, h) {
    data = read.csv(filename)
    data$Score = (data$High + data$Low) / 2
    data$Magnitude = as.factor(data$Magnitude)
    p = ggplot(data, aes(x = Horizon, y = Score, color = Magnitude, group = Position, fill = "transparent"))
    p = p + geom_hline(yintercept = 0.8, color = "green")
    p = p + geom_hline(yintercept = 0.6, color = "blue", linetype="dashed")
    p = p + geom_errorbar(aes(ymin = Low, ymax = High), position = "dodge", width = 0.5, size = 0.5)
    p = p + scale_x_continuous("Horizon (trading days)", breaks = 1:7, labels = c("1" = "1", "2" = "2", "3" = "3", "4" = "4", "5" = "5", "6" = "10", "7" ="15"))
    p = p + scale_y_continuous("F score (minimum to maximum)", limits = c(0, 1))
    p = p + scale_color_manual("Threshold", breaks = 1:3, labels = c("Small", "Medium", "Large"), values = c("#ff6362", "#bc5090", "#58508d"))
    p = p + facet_rep_wrap(~ Pair, ncol = 3, repeat.tick.labels = 'all')
    p = p + theme(panel.background = element_rect(fill = "transparent", colour = NA),
                  plot.background = element_rect(fill = "transparent", colour = NA),
                  legend.key = element_rect(fill = "transparent", colour = NA),                   
                  legend.background = element_rect(fill = "transparent"), 
                  legend.box.background = element_rect(fill = "transparent"))
    outputname = paste(target, '.', ext, sep='')
    ggsave(outputname, p, width = w, height = h, units = "cm", bg = "transparent")
}

visualize('perf.csv', 'ranges', 22, 34) # manuscript
visualize('sma.csv', 'smaranges', 22, 34)

separate <- function(filename, w, h) {
    data = read.csv(filename)
    data$Score = (data$High + data$Low) / 2
    data$Magnitude = as.factor(data$Magnitude)
    lapply(sort(unique(data$Pair)), function(cp) {
        p = ggplot(data[data$Pair == cp,], aes(x = Horizon, y = Score, color = Magnitude, group = Position, fill = "transparent"))
        p = p + geom_hline(yintercept = 0.8, color = "green")
        p = p + geom_hline(yintercept = 0.6, color = "blue", linetype="dashed")
        p = p + geom_errorbar(aes(ymin = Low, ymax = High), position = "dodge", width = 0.5, size = 0.5)
        p = p + scale_x_continuous("Horizon (trading days)", breaks = 1:7, labels = c("1" = "1", "2" = "2", "3" = "3", "4" = "4", "5" = "5", "6" = "10", "7" ="15"))
        p = p + scale_y_continuous("F score (minimum to maximum)", limits = c(0, 1))
        p = p + scale_color_manual("Threshold", breaks = 1:3, labels = c("Small", "Medium", "Large"), values = c("#ff6362", "#bc5090", "#58508d"))
        p = p + theme(panel.background = element_rect(fill = "transparent", colour = NA),
                      plot.background = element_rect(fill = "transparent", colour = NA),
                      legend.key = element_rect(fill = "transparent", colour = NA), 
                      legend.background = element_rect(fill = "transparent"), 
                      legend.box.background = element_rect(fill = "transparent"))
        outputname = paste('pair_', cp, '.', ext, sep = '')
        ggsave(outputname, p, width = w, height = h, units = "cm", bg = "transparent")
    })
}

separate('perf.csv', 15, 8) # slides




