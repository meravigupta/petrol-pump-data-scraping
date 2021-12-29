import pandas as pd
from datetime import date
from datetime import timedelta
import final_mail
from bs4 import BeautifulSoup
from glob import glob

files = glob("path/petrolpump_chayan/*html") 
columns = ["Title","Company Name","Published Date","State Name","View Advertisement Details","Closing_Date","Region","District","Location Description","Location Sl No","Type of RO","Mode of selection","Category Name","Status"]
output = []
for file in files:
    f = open(file,"rb")
    content = f.read().decode("utf-8")
    f.close()
    soup = BeautifulSoup(content)
    t_body = soup.findAll("tbody")
    title = t_body[0].findAll("td")[1].text.strip()
    Company_Name = t_body[0].findAll("td")[3].text.strip()
    Published_Date = t_body[0].findAll("td")[5].text.strip()
    State_Name =t_body[1].findAll("td")[1].text.strip()
    View_Advertisement_Details = t_body[1].findAll("td")[2].find("a")["href"]	
    Closing_Date = t_body[1].findAll("td")[5].text.strip()
    print(Closing_Date)
    for Detail in t_body[2].findAll("tr"):
        Region = Detail.findAll("td")[0].text.strip()
        District = Detail.findAll("td")[1].text.strip()
        Location_Description=Detail.findAll("td")[2].text.strip()
        Location_Sl_No= Detail.findAll("td")[3].text.strip()	
        Type_of_RO	= Detail.findAll("td")[4].text.strip()
        Mode_of_selection = Detail.findAll("td")[5].text.strip()	
        Category_Name = Detail.findAll("td")[6].text.strip()	
        Status	= Detail.findAll("td")[7].text.strip()
        out_row = [title,Company_Name,Published_Date,State_Name,View_Advertisement_Details,Closing_Date,Region,District,Location_Description,Location_Sl_No,Type_of_RO,Mode_of_selection,Category_Name,Status]
        output.append(out_row)
data = pd.DataFrame(output,columns=columns)
to_day = date.today()
today = to_day.strftime("%Y-%m-%d")
yester_day = to_day - timedelta(days = 1)
yesterday = yester_day.strftime("%Y-%m-%d")
file_name = "C:/Users/Prabhat/Documents/petrolpump_chayan/petrolchayan"+ today +".xlsx"
data.to_excel(file_name)
prev_file = "C:/Users/Prabhat/Documents/petrolpump_chayan/petrolchayan"+ yesterday +".xlsx"
df1 = pd.read_excel(file_name)
df2 = pd.read_excel(prev_file)
data1 = pd.DataFrame(df1)
data2 = pd.DataFrame(df2)
df = data1.merge(data2, how = 'outer' ,indicator=True)#.loc[lambda x : x['_merge']=='right_only']
filterdata = df[df["_merge"] == "left_only"]
final_file_name = "C:/Users/Prabhat/Documents/petrolpump_chayan/PetrolPump_added_"+today+".xlsx"
if len(filterdata) == 0:
    print("no data in list")
else :
    filterdata.to_excel(final_file_name)
    final_mail.send_mail(final_mail.receivers,"Please find attcahed new petrol pump details.","Petrol pump update",[final_file_name])