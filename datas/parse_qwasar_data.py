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


def get_data_from_qwasar(usernames):
    student_data = {}
    counter = 0
    for i in usernames:
        try:
            br.open(f"https://upskill.us.qwasar.io/users/{i}")
            soup = bs(br.response().read(), 'html.parser')

            student_data['qwasar username'] = i
            student_data['ism-familiya'] = soup.find('h1', class_='text-c-yellow').text.strip()
            student_data['qpoint'] = soup.find('div', attrs={'id': 'user_qpoints'}).text.strip()
            student_data["hozirgi o'qiyotgan sezoni"] = soup.find('div', attrs={'class': 'row p-t-10 align-items-center'}).find('h3').text.strip()

            link = f"https://upskill.us.qwasar.io{soup.find('div', attrs={'class': 'row p-t-10 align-items-center'}).find('a')['href']}"

            br.open(link)
            soup = bs(br.response().read(), 'html.parser')

            months = {'January': 'Yanvar', 'February': 'Fevral', 'March': 'Mart', 'April': 'Aprel', 'May': 'May', 'June': 'Iyun', 'July': 'Iyul', 'August': 'Avgust', 'September': 'Sentabr', 'October': 'Oktabr', 'November': 'Noyabr', 'December': 'Dekabr'}

            student_data['bu sezonning boshlanish kuni'] = f"{months[soup.find('div', class_='col-5 col-sm-3').find('h3').text.strip().split(' ')[0]]} {' '.join(soup.find('div', class_='col-5 col-sm-3').find('h3').text.strip().split(' ')[1:])}"
            student_data['bu sezonning tugash kuni'] = f"{months[soup.find('div', class_='col-5 col-sm-3 text-right').find('h3').text.strip().split(' ')[0]]} {' '.join(soup.find('div', class_='col-5 col-sm-3 text-right').find('h3').text.strip().split(' ')[1:])}"




        except:
            pass

        print(counter, i)
        print(student_data, "\n\n\n")
        counter += 1

        if counter == 2:
            break


def main():
    usernames = np.load("C:/Users/Student/PycharmProjects/astrummentors/astrummentor/datas/students-usernames.npz")[
        'usernames']
    get_data_from_qwasar(['qosimov_h', 'islomov_i'])


main()
