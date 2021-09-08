require('ggplot2')

d = read.csv('comp.dat', header = FALSE, sep = " ", na.strings = "NA")
names(d) = c("Indicator", "Percentage", "Experiment")
d$Indicator = as.factor(d$Indicator)
d$Experiment = as.factor(d$Experiment)
ena = c("All", "Without RSI", "Without RSI & MACD")
ina = c("SMA-3", "SMA-5", "SMA-7", "SMA-14", "SMA-21", "EMA-3", "EMA-5", "EMA-7", "EMA-14", "EMA-21", "H-A", "ZZS-level", "ZZS-kind", "SO", "RSI", "MACD-SMA", "MACD-EMA")
p <- ggplot(data = d, aes(x = Indicator, y = Percentage, fill = Experiment)) +
    geom_bar(stat = "identity", color = "black", position = position_dodge(), width = 0.8) +
    theme_minimal() +
    scale_x_discrete(labels = ina) +
    theme(axis.text.x = element_text(angle = 90)) +
    scale_fill_manual(labels = ena, values = c('#00aa00','#99aa00', '#0099cc'))

ggsave("comp.png", width = 8, height = 5, dpi = 300)