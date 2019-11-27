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
            spamwriter = csv.writer(csvfile, delimiter=' ')
            spamwriter.writerow(user_meta_data)

def get_user_details():
    users_list =[]
    with open('Data/user.csv', 'r') as f:
        reader = csv.reader(f)
        users_list = list(reader)
        # print(users_list)
    return users_list


def authenticate_user_details(username,password):
    users = get_user_details()
    for user in users:
        if username in user:
            if password == user[2]:
                allergy = user[3]
                # print("allergy",allergy)
                return True
    




