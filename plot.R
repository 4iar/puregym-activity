require(ggplot2)
require(scales)

f <- readline(prompt="Path of the data file: ")

data = read.csv(file=f, header=FALSE, as.is=TRUE)

# Decimal time is easier to manage
data$V3 = sapply(strsplit(data$V3, ":"),
  function(x) {
    x <- as.numeric(x)
    x[1]+x[2]/60
  }
)

# Make sure that the week days are not out of order
data$V2 <- factor(data$V2, levels = c("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"))

p1 <- ggplot(data, aes(x=V3, y=V4)) + geom_point() +
  stat_smooth() +
  scale_x_continuous("Time of day (UTC)", breaks=rep(0:24)) +
  scale_y_discrete("Number of people in gym", breaks=pretty_breaks(n=15))

p2 <- ggplot(data, aes(V3, V4)) + geom_point() +
  stat_smooth() +
  facet_wrap( ~ V2, ncol = 1) +
  scale_x_continuous("Time of day (UTC)", breaks=rep(0:24)) +
  scale_y_discrete("Number of people in gym", breaks=pretty_breaks(n=15))

p3 <- ggplot(data, aes(V3, V4)) +
  stat_smooth(aes(fill = factor(V2))) +
  scale_fill_discrete(name = "") +
  scale_x_continuous("Time of day (UTC)", breaks=rep(0:24)) +
  scale_y_discrete("Number of people in gym", breaks=pretty_breaks(n=15))
