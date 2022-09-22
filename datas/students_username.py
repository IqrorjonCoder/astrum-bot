import numpy as np
import pandas as pd


def save_usernames():
    sheet_id = "1A2QPeQ-XQsUKVbI8s7Zs07tauiBMkIeBuzXN588RJjM"
    sheet_name = "Students\logins"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

    data = pd.read_csv(url)
    data = data.iloc[:, :2]

    data.columns = ['students name', 'students username']
    data = data.dropna()
    usernames = np.array(data['students username'].tolist())
    np.savez('C:/Users/Student/PycharmProjects/astrummentors/astrummentor/datas/students-usernames.npz', usernames=usernames)


save_usernames()
