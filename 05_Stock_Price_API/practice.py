import re
start_date = "2020 year 8/30"
start_lst = re.split('\D+', start_date)
start_year = int(start_lst[0])
start_month = int(start_lst[1])
start_day = int(start_lst[2])
start_date = f"{start_year:04d}-{start_month:02d}-{start_day:02d}"
print(start_date)