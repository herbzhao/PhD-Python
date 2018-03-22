x_columns = ['A','C','E','G','I','K','M','O','Q','S','U','W','Y','AA','AC','AE','AG','AI','AK','AM','AO','AQ','AS','AU','AW']
y_columns = ['B','D','F','H','J','L','N','P','R','T','V','X','Z','AB','AD','AF','AH','AJ','AL','AN','AP','AR','AT','AV','AX','AZ']
xy_pairs = zip(x_columns,y_columns)


tab_name = 'start and end'


for x_column,y_column in list(xy_pairs):
        print("=SERIES(,'{0}'!${1}$3:${1}$1000,'{0}'!${2}$3:${2}$1000,1)".format(tab_name, x_column, y_column))