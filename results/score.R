library(ggplot2)
library(lemon)

visualize <- function(filename, outputname) {
    data = read.csv(filename)
    data$Score = (data$High + data$Low) / 2
    data$Magnitude = as.factor(data$Magnitude)
    p = ggplot(data, aes(x = Horizon, y = Score, color = Magnitude, group = Position))
    p = p + geom_hline(yintercept = 0.8, color = "green")
    p = p + geom_hline(yintercept = 0.6, color = "blue", linetype="dashed")
    p = p + geom_errorbar(aes(ymin = Low, ymax = High), position = "dodge", width = 0.5, size = 0.5)
    p = p + scale_x_continuous("Horizon (trading days)", breaks = 1:7, labels = c("1" = "1", "2" = "2", "3" = "3", "4" = "4", "5" = "5", "6" = "10", "7" ="15"))
    p = p + scale_y_continuous("F score (minimum to maximum)")
    p = p + scale_color_manual("Threshold", breaks = 1:3, labels = c("Small", "Medium", "Large"), values = c("#ff6362", "#bc5090", "#58508d"))
    p = p + facet_rep_wrap(~ Pair, ncol = 3, repeat.tick.labels = 'all')
    ggsave(outputname, p, width=22, height=34, units="cm")
}

visualize('perf.csv', 'ranges.eps')
visualize('sma.csv', 'smaranges.eps')


