library(lubridate)
library(data.table)
# 讀取數據
data = read.csv("D:\\data_analysis_powerbi\\supermarket_sales.csv")

# 日期和月、周處理
data$Date = as.Date(data$Date, format ="%m/%d/%Y")
data$month = as.integer(substr(data$Date, 6, 7))
data$weeks = week(data$Date)
head(data, 2)
# 確保 Branch 是一個因子
data$Branch = as.integer(factor(data$Branch))

range(data$Branch)

#####=====回歸分析(第四間銷售額)
Tab = aggregate(Total~Branch, FUN=sum, data=data);   Tab
plot(Total~Branch,data=Tab)
Tab.lm = lm(Total~Branch, data = Tab) 
b = coef(Tab.lm);  b
plot(Total~Branch, data = Tab, xlim=c(1,4), pch=16)
abline(coef(Tab.lm))
total_pred = predict(Tab.lm, newdata=data.frame(Branch=c(4)));   total_pred  
plot(Total~Branch, data = Tab, xlim=c(1,4), ylim=c(0, max(c(Tab$Total,total_pred))), pch=16)
abline(coef(Tab.lm))       
text(x=4, y=total_pred, as.double(total_pred), col="red")
actual = Tab$Total;    actual 
predicted = as.vector( predict(Tab.lm, newdata=data.frame(Branch=Tab$Branch)) );   
predicted
R_squared = 1-sum((actual-predicted)^2)/sum((actual-mean(actual))^2);   R_squared
title(main = sprintf("Total Sales by Branch (R-squared = %.2f)", R_squared))

#####======RFM model 
length(unique(data$Invoice.ID))#[1] 1000
dim(data)#[1] 1000   17
data$customer=data$Invoice.ID
data$Date = as.Date(data$Date, format ="%m/%d/%Y")
setDT(data, key=c("customer","Date"))
Cv = data[, .(D0=min(Date), Df=max(Date), DD=length(unique(Date)),
              FF=length(unique(Invoice.ID)), MM=sum(Total), TT=sum(Quantity)), by=customer ] 
#D0-Df消費起訖日 DD消費日期區間 FF消費總次數 MM消費總額 TT購買商品總數
dim(Cv);head(Cv)
Cv$UU = Cv$MM / Cv$FF #每次消費金額
Cv$NN = Cv$TT / Cv$FF #每次購買商品數
Cv$BB = (Cv$Df-Cv$D0)/Cv$DD #消費間隔(多久消費一次)
range(Cv$DD)  #[1] 1 1
range(Cv$FF)  #[1] 1 1
range(Cv$MM)  #[1] 10.6785 1042.6500
range(Cv$BB)  #[1] 0 0
Cv$MM0= cut(Cv$MM,breaks=c(-1,0,100,300,600,900,1200));   table(Cv$MM0)
table(Cv$FF,Cv$MM0)

#####=====決策樹
library(rpart);library(rpart.plot)  
money.rpart = rpart(Total ~ Cv$UU + Cv$NN + Cv$BB, data = data);   print(money.rpart) 
rpart.plot(money.rpart)
#####=====聚類依據不同城市range of Tax.5和range of Total
my_hclus<-function(city){
  d1=data[which(data$City==city),c("Unit.price","Quantity","Tax.5.","Total")]
  fit_hc = hclust(dist(d1))
  return(fit_hc)
}
##Yangon
plot(my_hclus("Yangon"))
for (kk in 2:20) { group = cutree(my_hclus("Yangon"), k=kk);   print(table(group)) }  
Ncls=9;   group = cutree(my_hclus("Yangon"), k=Ncls);   print(table(group))  
for(i in 1:9){
  print(c(sprintf("this is group %d",i)))
  temp=data[which(data$City=="Yangon"),c("Unit.price","Quantity","Tax.5.","Total")][group==i,]
  print(sprintf("range of Unit.price: %.2f",range(temp$Unit.price)))
  print(sprintf("range of Quantity: %.2f",range(temp$Quantity)))
  print(sprintf("range of Tax.5.: %.2f",range(temp$Tax.5.)))
  print(sprintf("average of Tax.5 :%.2f",mean(temp$Tax.5.)))
  print(sprintf("range of Total: %.2f",range(temp$Total)))
  print(sprintf("average of Total: %.2f",mean(temp$Total)))
}
##Naypyitaw
plot(my_hclus("Naypyitaw"))
for (kk in 2:25) { group = cutree(my_hclus("Naypyitaw"), k=kk);   print(table(group)) }
Ncls=8;   group = cutree(my_hclus("Naypyitaw"), k=Ncls);   print(table(group))
for(i in 1:8){
  print(c(sprintf("this is group %d",i)))
  temp=data[which(data$City=="Naypyitaw"),c("Unit.price","Quantity","Tax.5.","Total")][group==i,]
  print(sprintf("range of Unit.price: %.2f",range(temp$Unit.price)))
  print(sprintf("range of Quantity: %.2f",range(temp$Quantity)))
  print(sprintf("range of Tax.5.: %.2f",range(temp$Tax.5.)))
  print(sprintf("average of Tax.5 :%.2f",mean(temp$Tax.5.)))
  print(sprintf("range of Total: %.2f",range(temp$Total)))
  print(sprintf("average of Total: %.2f",mean(temp$Total)))
}
##Mandalay
plot(my_hclus("Mandalay"))
for (kk in 2:25) { group = cutree(my_hclus("Mandalay"), k=kk);   print(table(group)) }
Ncls=5;   group = cutree(my_hclus("Mandalay"), k=Ncls);   print(table(group))
for(i in 1:5){
  print(c(sprintf("this is group %d",i)))
  temp=data[which(data$City=="Mandalay"),c("Unit.price","Quantity","Tax.5.","Total")][group==i,]
  print(sprintf("range of Unit.price: %.2f",range(temp$Unit.price)))
  print(sprintf("range of Quantity: %.2f",range(temp$Quantity)))
  print(sprintf("range of Tax.5.: %.2f",range(temp$Tax.5.)))
  print(sprintf("average of Tax.5 :%.2f",mean(temp$Tax.5.)))
  print(sprintf("range of Total: %.2f",range(temp$Total)))
  print(sprintf("average of Total: %.2f",mean(temp$Total)))
}
max(data[which(data$City=="Mandalay"),c("Unit.price","Quantity","Tax.5.","Total")][group==1,])
