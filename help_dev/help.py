with open("/Users/benwegener/Library/Mobile Documents/com~apple~CloudDocs/BlogBar/BlogBar-webapplication/help_dev/categories.txt", mode="r") as file:
    array = []
    for line in file.readlines():
        array.append(line.replace("\n", ""))
    array.sort()
    i = 0
    string= "["
    for item in array:
        i += 1
        string += "'"+str(item)+"',"
        #print("<option value=\""+str(i)+"\" {% if '"+str(i)+"' in topics %}selected{% endif %}>"+item+"</option>")

    print(string +"]")

exit()

for year in range(1961, 2019):
    print("<option value=\""+str(year)+"\" {% if birthyear_to == '"+str(year)+"' %} selected {% endif %}>"+str(year)+"</option>")

with open("/Users/benwegener/Library/Mobile Documents/com~apple~CloudDocs/BlogBar/BlogBar-webapplication/help_dev/countries.txt", mode="r") as file:
    with open("/Users/benwegener/Library/Mobile Documents/com~apple~CloudDocs/BlogBar/BlogBar-webapplication/help_dev/country_opts.txt", mode="w") as target:
        array = []
        for line in file.readlines():
            array.append(line.replace("\n", ""))
        #array.sort()
        for i in range(0, len(array)):
            target.write("<option value=\""+str(i+1)+"\" {% if "+str(i+1)+" in active_countries or '"+str(i+1)+"' in instagram_countries %}selected{% endif %}>"+array[i]+"</option>\n")

years = [100, 250, 750, 1000, 1500, 2500, 5000, 7500, 10000, 12500, 15000, 20000, 25000, 30000, 40000, 50000, 750000, 100000, 125000, 250000, 500000, 750000, 1000000, 2000000]
for year in years:
    print("<option value=\""+str(year)+"\" {% instagramFollowerTo == '"+str(year)+"' %}selected{% endif%}>"+str(year)+"</option>")


for i in range(0, 101):
    print("<option value=\""+str(i)+"\">"+str(i)+"%</option>")

for age in ["UNDEFINED", 19, 26, 36, 46, 56]:
    print("<option value=\"" + str(age) + "\" {% instagram_age_distribution_from == '"+str(age)+"' %}selected{% endif%}>" + str(age) + "</option>")

for age in [18, 25, 35, 45, 55, "UNDEFINED"]:
    print("<option value=\"" + str(age) + "\" {% instagram_age_distribution_to == '"+str(age)+"' %}selected{% endif%}>" + str(age) + "</option>")


for percent in ["beliebig", 0,1,2,3,4,5,6,7,8,9,10,15,20,30,40,50]:
    print("<option value=\"" + str(percent) + "\">ab " + str(percent) + "%</option>")

years = [100,150,250,500,750,1000,2500,5000,7500,10000,15000,20000,30000,40000,50000,75000,100000,125000,150000,200000,250000,350000,500000,750000,10000000]
for year in years:
    print("<option value=\""+str(year)+"\">bis "+str(year)+"</option>")

with open("/Users/benwegener/Library/Mobile Documents/com~apple~CloudDocs/BlogBar/BlogBar-webapplication/help_dev/numbers.txt", mode="w") as file:
    for i in [100,250,1000,2000,5000,10000,20000,30000,50000,100000,150000,250000]:
        file.write("<option value=\"{val}\">{val}</option>\n".format(val=i))

for percent in range(1, 101):
    print("<option value='"+str(percent)+"' {% if instagram_gender_distribution_male_from == '"+str(percent)+"' %}selected{% endif %}>"+str(percent)+"%</option>")