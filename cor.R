# install.packages("PerformanceAnalytics")
# library(PerformanceAnalytics)

library("GGally")
library("ggplot2")

lowerFn <- function(data, mapping, method = "lm", ...) {
  p <- ggplot(data = data, mapping = mapping) +
    geom_point(colour = "black", shape = 16, size = 0.8, alpha = 0.6) +
    geom_smooth(method = method, color = "red", ...)
  p
}

cor_custom <- function(data, mapping,  ...){
  x <- eval_data_col(data, mapping$x)
  y <- eval_data_col(data, mapping$y)
  corr <- cor(x, y, method="pearson", use='complete.obs')
  ggally_text(
    label = as.character(round(corr, 2)), 
    mapping = aes(),
    xP = 0.5, yP = 0.5,
    color = 'black',
    ...
  )
}


sets = c('AUDUSD','BTCUSD','EURCAD','EURCHF','EURGBP','EURJPY','EURSEK','EURUSD','GBPJPY','GBPUSD','NZDUSD','USDCNY','USDJPY','USDMXN','USDRUB')
for (dataset in sets) {
  input = paste(dataset, ".combined.csv", sep="")
  data = read.csv(input, header=TRUE, sep=",", check.names = FALSE)
  data$t = NULL # not needed for correlation analysis
  # eliminate some of the obviously correlated ones
  setEPS()
  target = paste(dataset, ".eps", sep = "")
# option a: the same information, but a bit uglier and harder to customize visually
#  postscript(target, width=10, height=10)
#  chart.Correlation(data, histogram = TRUE, method = "pearson", col = "blue")
#  dev.off()
# option b: looks better for a publication
  chart = ggpairs(data, lower = list(continuous = wrap(lowerFn, method = "lm")),
    diag = list(continuous = wrap("barDiag", colour = "blue")),
    upper = list(continuous = wrap(cor_custom, size = 6))) +
        theme(axis.line=element_blank(),
        axis.text=element_blank(),
        axis.ticks=element_blank(),
	panel.border = element_rect(colour = "gray", fill = NA, size = 1),
	panel.margin=unit(2, "mm"),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
	panel.background = element_blank())
  ggsave(filename = target, plot = chart, device = cairo_ps, width=10, height=10, units="in")
}