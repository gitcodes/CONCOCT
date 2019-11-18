import csv
def save_user_details(userdetails):
    isSuccess = True
    try:
        user_login_data = userdetails[0]
        with open('Data/user.csv', 'a') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',')
            spamwriter.writerow(user_login_data)
        create_user_specific_metadata(user_login_data[0],userdetails[1])
    except:
        isSuccess = False

def create_user_specific_metadata(username,user_meta_data):
        path = "User Data/"+username+".csv"
        with open(path , 'a+',newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',')
            spamwriter.writerow(user_meta_data)



