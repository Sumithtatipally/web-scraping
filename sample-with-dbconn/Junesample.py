import requests
import csv
import os
import string
import re
import numpy as np
import pandas as pd
import pymysql

db = pymysql.connect("localhost","root","","htmle" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

from bs4 import BeautifulSoup as bs

f = csv.writer(open('sam.csv', 'w', newline=''))
f.writerow(['Name','Qualification','Specializations','Years Of Exp','Service','Registration Number','Clinic Name','Address','VisitDays','Visit Time','timings','Consultation fee','Clinic Name2','Address2','VisitDays2','Visit Time2','timings2','Consultation fee2','Clinic Name3','Address3','VisitDays3','Visit Time3','timings3','Consultation fee3','Clinic Name4','Address4','VisitDays4','Visit Time4','timings4','Consultation fee4','Clinic Name5','Address5','VisitDays5','Visit Time5','timings5','Consultation fee5','Clinic Name6','Address6','VisitDays6','Visit Time6','timings6','Consultation fee6'])

pages = []

fileList = list(os.walk('D:\\Python\\June Files\\'))
for path, directory, files in fileList:
    for file in files:
        if(file.endswith('.html')):
            pages.append('D:\\Python\\June Files\\'+file)
            #print(file)

for url in pages:
    s = open(url, errors='ignore')
    data = bs(s, "html.parser")


    names = data.find('div',{'class':'pure-u-20-24'})
    docname = names.find('h1').text
    print(docname)

    qualifications = []
    qua = data.findAll('div', {'class': 'c-profile--qualification'})

    for qdetails in qua:
        qualificationdata = {}
        quali = qdetails.find('p').text
        qualificationdata['qualification'] = quali
        specality = qdetails.find('div', {'data-qa-id': 'doctor-specializations'}).text
        specality = specality.replace('Years Experience', '')
        specality = re.sub(' +', ' ', specality)
        sppp = specality.split(",")
        spppp = sppp[:-1]
        speciality = ','.join(spppp)
        qualificationdata['specialization'] = speciality
        yearsexp = sppp.pop()
        qualificationdata['yearsofexp'] = yearsexp
        qualifications.append(qualificationdata)

    #print(qualifications)

    for ser in data:
        try:
            serv = data.find('div', {'id': 'services'}).text
        except AttributeError:
            serv = ""
        if (serv != ""):
            serv = serv.replace('Services', '')
            serv = serv.replace('View all', '')
            lines = (line.strip() for line in serv.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            serv = '\n'.join(chunk for chunk in chunks if chunk)


    reg = data.find('div', {'id': 'registrations'}).text
    lines = (line.strip() for line in reg.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    reg = '\n'.join(chunk for chunk in chunks if chunk)
    reg = reg.replace('Registration', '')
    # print(reg)

    clinicaddress = []
    detail = data.findAll('div', {'class': 'pure-g c-profile--clinic--details'})

    for clinic in detail:
        clinicdetails = {}
        clinicname = clinic.find('h2').text
        clinicdetails['name'] = clinicname
        address = clinic.find('p', {'class': 'c-profile--clinic__address'})
        address = re.sub(' +',' ', address.text)
        clinicdetails['address'] = address

        try:
            days = clinic.find('p', {'class': 'timings__days'}).text
        except AttributeError:
            days = " "
        if (days!=" "):
            wdays = days

        maintimings = []
        try:
            #time = clinic.find('p', {'class': 'timings__time'}).text
            time1 = clinic.find('p', {'class': 'timings__time'})
            timings = time1.findAll('span')
            for time in timings:
                timeperiod = re.sub(' +', ' ', time.text)
                timearray = timeperiod.split("-")
                length = len(timearray)
                if (length == 2):
                    starttime = re.sub(' \n +','',timearray[0])
                    endtime = re.sub(' \n +','',timearray[1])
                    t = '-'.join(timearray)
                    maintimings.append(t)
                    #print(maintimings)
                print(maintimings)
        except AttributeError:
            time = " "
        if (time!=" "):
            wtime = time


        fees = clinic.find('div', {'class': 'u-no-margin--top'}).text
        fees = fees.replace('â‚¹', '')
        #timings = clinic.findAll('div',{'class': 'pure-u-1-3 u-cushion--left'})
        clinicdetails['Consultationfee'] = fees
        clinicdetails['workingdays'] = wdays
        clinicdetails['workingtime'] = wtime
        clinicaddress.append(clinicdetails)

    #print(clinicaddress)

    sql = "INSERT INTO `profilesdata`" \
          "(`name`, `qualification`, `specialization`,`yearsof_exp`,`service`,`regno`)" \
          " VALUES ('" + docname + "','" + quali + "','" + speciality + "','" + yearsexp + "','" + serv + "','" + reg + "')"
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        doctorId = cursor.lastrowid
        print(sql)
        print(doctorId)
        for clinic in clinicaddress:
            clinicSql = "INSERT INTO `clinics`" \
                    "(`doctor_id`, `clinic_name`, `clinic_address`, `visit_days`, `visit_time`, `consultation_fee`)" \
                    "VALUES ('"+str(doctorId)+"','" + clinic['name'] + "','" + clinic['address'] + "','" + clinic['workingdays'] + "','" + clinic['workingtime'] + "','" + clinic['Consultationfee'] + "')"
            print(clinicSql)

            try:
                cursor.execute(clinicSql)
                db.commit()
            except:
                db.rollback()


    except:
        # Rollback in case there is any error
        db.rollback()


    insertarray = [docname, quali, speciality,yearsexp, serv, reg,]

    for clinic in clinicaddress:
        insertarray.append(clinic['name'])
        insertarray.append(clinic['address'])
        insertarray.append(clinic['workingdays'])
        insertarray.append(clinic['workingtime'])
        #insertarray.append(clinic['workingdays']+';'+clinic['workingtime'])
        insertarray.append(clinic['Consultationfee'])

    f.writerow(insertarray)

# disconnect from server
db.close()






