#PTT股市分析-大數據分析實務報告

wkDir = "D:\\big_data_R\\";   setwd(wkDir)
dataDir = "D:\\big_data_R\\";
library(readxl);library(stringr);library(data.table);library(anytime);library(stringr)

#####===== (KDD1) 數據擷取 (file-->X) =====#####
X = as.data.frame(read_excel("D:\\big_data_R\\ptt-stock20240403.xlsx"));
X=na.omit(X)
head(X,2);dim(X)
tail(as.Date(X$push_time,format = "%m/%d"))
X$push_time2=paste("2024/",X$push_time,sep="")
X$push_time2=as.Date(X$push_time2)
head(X$push_time2)
X$nch= nchar(X$push_content)
md=str_extract_all(X$time,"\\b[[:alpha:]]{3}\\s+\\d{1,2}")
head(md)
tail(md)
m=str_extract_all(md,"\\b\\w{3}")
n=length(m)
for(i in 1:n){
  if(m[i]=="Jan"){
    m[i]="01"
  }
  if(m[i]=="Feb"){
    m[i]="02"
  }
  if(m[i]=="Mar"){
    m[i]="03"
  }
  if (m[i]=="Apr"){
    m[i]='04'
  }
  if (m[i]=="May"){
    m[i]='05'
  }
  if (m[i]=="Jun"){
    m[i]='06'
  }
  if (m[i]=="Jul"){
    m[i]='07'
  }
  if (m[i]=="Aug"){
    m[i]='08'
  }
  
  if (m[i]=="Sep"){
    m[i]='09'
  }
  if (m[i]=="Oct"){
    m[i]='10'
  }
  if (m[i]=="Nov"){
    m[i]='11'
  }
  if (m[i]=="Dec"){
    m[i]='12'
  }
  
}

tail(m)
d=str_extract_all(md,"\\b\\d{1,2}")
head(d)
tail(d)
y=str_extract_all(X$time,"[[:digit:]]{4}")
head(y)
ymd=paste(y,"-",m,"-",d,sep="")
head(ymd)
X$time2=as.Date(ymd,format = "%Y-%m-%d")
head(X$time2)
tail(X$time2)
#X$time2=anydate(X$time)
dim(X);   head(X,2)  


#??
#posix_time <- as.POSIXct(X$time,format = "%a %b  %d %H:%M:%S %Y")
#strptime(X$time,format = "%a %b %d %H:%M:%S %Y")
#head(posix_time)
#X$isTitle = as.integer(X$push_time2==X$time)
#####===== (KDD2) 數據探索 (X) =====#####
range(X$time2)        
range(X$push_time)
table(X$title_id)    #====> Pv模型
length(unique(X$title_id)) 
length(unique(X$push_id))   

#####===== (KDD3) 數據轉換 (X-->Cv) =====#####
#回文作者
setDT(X, key="push_id")
Cv = X[, .(D0=min(push_time2), Df=max(push_time2), Tcount=length(unique(title)), Rcount=length(push_time2), chCount=sum(nch)), by=push_id]
dim(Cv);   head(Cv,3)  
 
Cv$chCount0 = cut(Cv$chCount, breaks=c(-1,0,9,49,99,199,299,999,9999,99999));   table(Cv$chCount0)

range(Cv$Rcount)
range(Cv$Tcount)  
length(Cv$push_id)
#回復次數前10名的作者
cpush_id=as.data.frame(table(X$push_id))
temp=cpush_id[order(cpush_id$Freq,decreasing = TRUE),]
temp[1:10,]
#####===== 回文作者停留時間=====#####
Cv$ndays=as.Date(Cv$Df)-as.Date(Cv$D0);head(Cv,2)
range(Cv$ndays)#0 243
Cv$nDay0 = cut(as.numeric(Cv$ndays), breaks=c(-1,0,7,30,60,90,180,240,365));   table(Cv$nDay0)
addmargins(table(Cv$nDay0, Cv$chCount0))# 回文作者參與度模型
#回文作者旅程
Cv[order(Cv$Tcount,decreasing = T) ,][1:10]
temp=Cv[Cv$ndays>60 ,]
temp[order(temp$ndays,decreasing = T) ,]

#####===== 數據轉換2=====#####
#發文作者
setDT(X, key="title_id")
X$nch_title= nchar(X$content);
Cv2 = X[, .(D0=min(time2), Df=max(time2), Tcount=length(unique(title)), Rcount=length(time2), chCount=sum(nch_title)), by=title_id]
X$nch_Tpush=nchar(X$title)
dim(Cv2);   head(Cv2,3)   

#發文次數前10名的作者
only_titleid=unique(X$title_id)
df_only_titleid=as.data.frame(only_titleid)
head(df_only_titleid)
num_titleid=length(only_titleid)
print(num_titleid)
id=NULL;freq=NULL
for(i in 1:num_titleid){
  t=X[which(X$title_id==only_titleid[i]),]
  #print(unique(t$title_id))
  #print(length(unique(t$title)))
  id=append(id,unique(t$title_id))
  freq=append(freq,length(unique(t$title)))

}
df=cbind.data.frame(id,freq)
head(df)
head(df[order(df$freq,decreasing = T),],10)

range(Cv2$chCount)  
Cv2$ndays=as.Date(Cv2$Df)-as.Date(Cv2$D0)
range(Cv2$ndays)#0 51
Cv2$nDay0 = cut(as.numeric(Cv2$ndays), breaks=c(-1,0,7,14,21,30,42,60))
table(Cv2$nDay0)
Cv2$chCount0 = cut(Cv2$chCount, breaks=c(-1,0,99,999,9999,99999,999999,9999999,99999999))
table(Cv2$chCount0)
addmargins(table(Cv2$nDay0, Cv2$chCount0))# 發文作者參與度模型
#發文作者旅程
Cv2[order(Cv2$Tcount,decreasing = T) ,][1:10]
temp2=Cv2[(Cv2$ndays>42)&((Cv2$chCount>100000)&(Cv2$chCount<1000000)), ]
temp2
temp2[order(temp2$Tcount,decreasing = T) , ]

#####=====  數據轉換3=====#####

setDT(X, key = "title") 
Pv = X[, .(only_title=unique(title), D0=min(time2), Df=max(time2), Nauthor=length(unique(title_id)), num_push_time=length(unique(push_time2)),
num_push_id=length(unique(push_id)),chCount=sum(nch_title,na.rm=T)), by=title]
head(Pv,5);dim(Pv)
Pv[-c(1)]
range(Pv$chCount)
Pv$chCount0 = cut(Pv$chCount, breaks=c(-1,99,999,9999,99999,999999,9999999));   table(Pv$chCount0)
Pv$nDay = (Pv$Df)-(Pv$D0);   range(Pv$nDay) #0 45
Pv$nDay0 = cut(as.numeric(Pv$nDay), breaks=c(-1,0,7,14,30,42,56));   table(Pv$nDay0)
addmargins(table(Pv$nDay0, Pv$chCount0))#發文主題與話題時間
#發文主題與話題時間旅程
Pv[Pv$nDay>30 ,]
nrow(Pv[(Pv$chCount>9999)&(Pv$chCount<99999)&(Pv$nDay==0),])
temp3=Pv[(Pv$chCount>9999)&(Pv$chCount<99999)&(Pv$nDay==0),]
temp3
temp3[order(temp3$chCount,decreasing = T),][1:10]

range(Pv$num_push_time)
addmargins(table(Pv$num_push_time,Pv$chCount0))#發文主題與討論持久度
#發文主題與討論持久度旅程
temp4=Pv[Pv$num_push_time>=10 ,]
temp4
temp4[order(temp4$num_push_time,decreasing = T), ]

range(Pv$num_push_id)
Pv$num_push_id0=cut(Pv$num_push_id,breaks = c(-1,0,9,49,99,499,999))
table(Pv$num_push_id0)
addmargins(table(Pv$num_push_id0,Pv$chCount0))#發文主題長短與討論熱度模型
#發文主題長短與討論熱度模型旅程
temp5=Pv[Pv$num_push_id>499 ,]
temp5
temp5[order(temp5$num_push_id,decreasing = T) ,]
#####=====發文轉貼出處=====#####

TT = str_extract_all(X$content,"[[:print:]]{2,4}新聞網")
unique(TT)
TT2 = str_extract_all(X$content,"[[:print:]]{2,3}日報")
unique(TT2)
TT3 = str_extract_all(X$content,"[[:print:]]{2,7}新聞雲")
unique(TT3)

#####====
library(igraph) 
Q = table(X$title,X$push_id);   dim(Q)
QQ = Q[order(rowSums(Q),decreasing=T), order(colSums(Q),decreasing=T)];   dim(QQ)
QQQ = QQ[1:30,1:30]
CC = t( round(QQQ>0) )%*%(round(QQQ>0));   CC
#--
gCC = graph_from_adjacency_matrix(CC[-5,-5], mode="undirected", weighted=TRUE)
par(family="STKaiti")
plot(gCC, vertex.label.family="STKaiti", edge.color=c("black","blue","green","orange")[E(gCC)$weight],
     edge.label=E(gCC)$weight, vertex.label=V(gCC)$name)                 
##--
kc = cluster_fast_greedy(gCC)
plot(kc,gCC)
QQQ = QQ[1:30,1:30]
PP = round(QQQ>0) %*% t(round(QQQ>0));   diag(PP)=0;   PP
gPP = graph.adjacency(PP, mode="undirected", weighted=TRUE)
kp = fastgreedy.community(gPP)
plot(kp,gPP)

#####=====
X$indXC = match(X$title_id,Cv2$title_id)   #-- project RR by Cv
X$indXP = match(X$title,Pv$title) 
head(X);dim(X)
PC00 = table( X$indXP, X$indXC );   dim(PC00)
rownames(PC00) = Pv$title;    colnames(PC00) = Cv2$title_id
PC0 = PC00[ order(rowSums(PC00),decreasing=TRUE), order(colSums(PC00),decreasing=TRUE) ]
PC0[1:4,1:10]
sum(PC0) 
PC = PC0[1:6,1:8];   sum(PC);   PC #[1] 1140
CC = t( round(PC>0) )%*%(round(PC>0));   CC 
gCC = graph_from_adjacency_matrix(CC[-5,-5], mode="undirected", weighted=TRUE)
par(family="STKaiti")
plot(gCC, vertex.label.family="STKaiti", edge.color=c("black","blue","green","orange")[E(gCC)$weight],
     edge.label=E(gCC)$weight, vertex.label=V(gCC)$name) 
kc = cluster_fast_greedy(gCC)
plot(kc,gCC)
