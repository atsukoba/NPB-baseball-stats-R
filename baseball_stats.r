pacific.data = read.table("pacific_league.txt", header=T)
central.data = read.table("central_league.txt", header=T)

head(pacific.data, 5)
head(central.data, 5)

summary(pacific.data$Hits)
summary(central.data$Hits)

all.data = merge(pacific.data, central.data, all=T)

plot(all.data$Points, all.data$Win.Prob)

pairs(all.data[9:22], cex=0.3,pch=20)
