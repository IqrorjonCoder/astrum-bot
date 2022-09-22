import numpy as np
from bs4 import BeautifulSoup as bs
import pandas as pd
import mechanize
import http.cookiejar as cookielib
import schedule
import time

cj = cookielib.CookieJar()
br = mechanize.Browser()
br.set_cookiejar(cj)
br.open("https://casapp.us.qwasar.io/login?service=https%3A%2F%2Fupskill.us.qwasar.io%2Fusers%2Fservice", timeout=10)
br.select_form(nr=0)
br.form['username'] = 'jas.884@mail.ru'
br.form['password'] = 'jasur2171517'
br.submit()


def get_data_from_qwasar(usernames, file_path):
    student_data = """"""
    counter = 0
    for i in usernames:
        try:
            br.open(f"https://upskill.us.qwasar.io/users/{i}")
            soup = bs(br.response().read(), 'html.parser')

            student_data += f"ism-familiya:{soup.find('h1', class_='text-c-yellow').text.strip()}\n"
            student_data += f"qpoint:{soup.find('div', attrs={'id': 'user_qpoints'}).text.strip()}\n"
            student_data += f"hozirgi o'qiyotgan bo'lim:{soup.find('div', attrs={'class': 'row p-t-10 align-items-center'}).find('h3').text.strip()}\n"

            link = f"https://upskill.us.qwasar.io{soup.find('div', attrs={'class': 'row p-t-10 align-items-center'}).find('a')['href']}"

            br.open(link)
            soup = bs(br.response().read(), 'html.parser')

            months = {'January': 'Yanvar', 'February': 'Fevral', 'March': 'Mart', 'April': 'Aprel', 'May': 'May', 'June': 'Iyun', 'July': 'Iyul', 'August': 'Avgust', 'September': 'Sentabr', 'October': 'Oktabr', 'November': 'Noyabr', 'December': 'Dekabr'}

            student_data += f"hozirgi o'qiyotgan bo'limning foizi:{soup.find('div', attrs={'class': 'progress b-radius-1'})['title']}\n"
            student_data += f"hozirgi o'qiyotgan bo'limning boshlanish kuni:{months[soup.find('div', class_='col-5 col-sm-3').find('h3').text.strip().split(' ')[0]]} {' '.join(soup.find('div', class_='col-5 col-sm-3').find('h3').text.strip().split(' ')[1:])}\n"
            student_data += f"hozirgi o'qiyotgan bo'limning tugash kuni:{months[soup.find('div', class_='col-5 col-sm-3 text-right').find('h3').text.strip().split(' ')[0]]} {' '.join(soup.find('div', class_='col-5 col-sm-3 text-right').find('h3').text.strip().split(' ')[1:])}\n"

            for j in soup.find_all('div', attrs={'class': 'border col-sm-4'}):
                m = months[j.find('div', attrs={'class': 'row bg-c-teal-70 text-c-dark-blue p-t-5 p-b-5'}).find('div').text.strip()]
                docode = 0.0
                docode_days = 0
                upskill = 0.0
                upskill_days = 0
                total = 0.0

                for k in j.find_all('div', attrs={'class': 'row font-size-12'}):
                    for l in k.find_all('div', attrs={'data-html': "true"}):
                        x = l['title'].split("<br>")[-3:]
                        if x[-1].split(": ")[-1] != '0h':

                            docode += float(x[0].split(": ")[-1].replace("h", ''))
                            upskill += float(x[1].split(": ")[-1].replace("h", ''))
                            total += float(x[2].split(": ")[-1].replace("h", ''))

                            if x[0].split(": ")[-1] != '0h':
                                docode_days += 1
                            if x[1].split(": ")[-1] != '0h':
                                upskill_days += 1

                student_data += f"{m} docode vaqti:{docode}soat\n"
                student_data += f"{m} docode kunlari:{docode_days}kun\n"
                student_data += f"{m} platformadagi vaqti:{upskill}soat\n"
                student_data += f"{m} platformadagi kunlari:{upskill_days}kun\n"
                student_data += f"{m} jami vaqti:{total}soat\n"
        except:
            pass

        print(counter, i)

        old_df = pd.read_csv(f"{file_path}")

        pd.concat([old_df, pd.DataFrame({'username': [i],
                                         'data': [student_data]})]).to_csv(f"{file_path}", index=False)

        student_data = ""
        counter += 1

        if counter == 20:
            break

def main():
    usernames = np.load("C:/Users/Student/PycharmProjects/astrummentors/astrummentor/datas/students-usernames.npz")['usernames']
    file_path = "C:/Users/Student/PycharmProjects/astrummentors/astrummentor/database/data.csv"
    pd.DataFrame({'username': [], 'data': []}).to_csv(f"{file_path}", index=False)
    get_data_from_qwasar(usernames, file_path)


main()
