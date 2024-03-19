library(DBI)
library(tidyverse)

library(RMySQL)


db_user <- 'root'
db_password <- '<Input your password here>'
db_name <- 'seanutsii'
db_table <- 'common_values_str'
db_host <- '127.0.0.1' # for local access
db_port <- 3306
# 3. Read data from db
mydb <-  dbConnect(MySQL(), user = db_user, password = db_password,
                   dbname = db_name, host = db_host, port = db_port)
s <- paste0("select * from ", db_table)
head(dbListTables(mydb))
rs <- dbSendQuery(mydb, s)
df <-  fetch(rs, n = -1)
on.exit(dbDisconnect(mydb))

head(df)
