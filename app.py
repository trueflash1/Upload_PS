from FirstWindow import Ui_MainWindow
from UploadWindow import Ui_UploadWindow
from PyQt5 import QtWidgets
# import json
from threading import Thread
import time
import cx_Oracle as cx
import requests as requests
import sys

def Connection_BD():
    connection = cx.connect(
        user="",
        password="",
        dsn=cx.makedsn("", "", ""),
        threaded=True)
    return connection
# connection = Connection_BD()


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
MainWindow.setWindowTitle("Upload program")
ui.import_educational_programs.setEnabled(False)
ui.import_study_plans.setEnabled(False)
ui.import_discipline.setEnabled(False)
ui.import_study_plans_discipline.setEnabled(False)
ui.Upload_Students.setEnabled(False)
ui.Upload_contingent_flows.setEnabled(False)
ui.import_study_plan_students.setEnabled(False)
ui.marks.setEnabled(False)

def zapusk(SepCursor, uiMarks, link, name, wait, all_string_Marks):
    th1 = Thread(target=upload_kusochkami, args=(SepCursor, uiMarks, link, name, wait, all_string_Marks))
    th1.start()
    th1.join()

global count
count = 0
#загрузка по 1000 250 50 10 1
def upload_kusochkami(SepCursor1, uiNmae, link, name, sleep, all_string_for_update):
    global count
    SepCursor = list()
    SepCursor_250 = list()
    SepCursor_50 = list()
    SepCursor_10 = list()
    SepCursor_one = list()
    for row in SepCursor1:
        SepCursor.append(row)
        if len(SepCursor) == 500:
            study_plans_disciplines = dict()
            headers = {'Content-Type': 'application/json', 'X-CN-UUID': ''}
            study_plans_disciplines["organization_id"] = ""
            study_plans_disciplines[name] = SepCursor
            Addstudy_plans_disciplines = requests.post(link, headers=headers, json=study_plans_disciplines, verify=False)
            if str(Addstudy_plans_disciplines.status_code) == str(201):
                count += 500
                uiNmae.progressBar_upload.setValue(int((100 / len(all_string_for_update)) * count))
                uiNmae.count_progress.setText(str(count) + "/" + str(len(all_string_for_update)))
            print(Addstudy_plans_disciplines.status_code, 500, count)
            if str(Addstudy_plans_disciplines.status_code) != str(201):
                for row in SepCursor:
                    SepCursor_250.append(row)
                    if len(SepCursor_250) == 250:
                        study_plans_disciplines[name] = SepCursor_250
                        Addstudy_plans_disciplines = requests.post(link, headers=headers, json=study_plans_disciplines, verify=False)
                        if str(Addstudy_plans_disciplines.status_code) == str(201):
                            count += 250
                            uiNmae.progressBar_upload.setValue(
                                int((100 / len(all_string_for_update)) * count))
                            uiNmae.count_progress.setText(
                                str(count) + "/" + str(len(all_string_for_update)))
                        print(Addstudy_plans_disciplines.status_code, 250, count)
                        if str(Addstudy_plans_disciplines.status_code) != str(201):
                            for row in SepCursor_250:
                                SepCursor_50.append(row)
                                if len(SepCursor_50) == 50:
                                    study_plans_disciplines[name] = SepCursor_50
                                    Addstudy_plans_disciplines = requests.post(link, headers=headers, json=study_plans_disciplines, verify=False)
                                    if str(Addstudy_plans_disciplines.status_code) == str(201):
                                        count += 50
                                        uiNmae.progressBar_upload.setValue(
                                            int((100 / len(all_string_for_update)) * count))
                                        uiNmae.count_progress.setText(
                                            str(count) + "/" + str(len(all_string_for_update)))
                                    print(Addstudy_plans_disciplines.status_code, 50, count)
                                    if str(Addstudy_plans_disciplines.status_code) != str(201):
                                        for row in SepCursor_50:
                                            SepCursor_10.append(row)
                                            if len(SepCursor_10) == 10:
                                                study_plans_disciplines[name] = SepCursor_10
                                                Addstudy_plans_disciplines = requests.post(link, headers=headers, json=study_plans_disciplines, verify=False)
                                                if str(Addstudy_plans_disciplines.status_code) == str(201):
                                                    count += 10
                                                    uiNmae.progressBar_upload.setValue(
                                                        int((100 / len(all_string_for_update)) * count))
                                                    uiNmae.count_progress.setText(
                                                        str(count) + "/" + str(len(all_string_for_update)))
                                                print(Addstudy_plans_disciplines.status_code, 10, count)
                                                if str(Addstudy_plans_disciplines.status_code) != str(201):
                                                    for row in SepCursor_10:
                                                        SepCursor_one.append(row)
                                                        study_plans_disciplines[name] = SepCursor_one
                                                        Addstudy_plans_disciplines = requests.post(link,
                                                            headers=headers, json=study_plans_disciplines, verify=False)
                                                        count += 1
                                                        uiNmae.progressBar_upload.setValue(
                                                            int((100 / len(all_string_for_update)) * count))
                                                        uiNmae.count_progress.setText(
                                                            str(count) + "/" + str(len(all_string_for_update)))
                                                        print(Addstudy_plans_disciplines.status_code, 1, count)
                                                        if Addstudy_plans_disciplines.status_code == 400:
                                                            exception_list(SepCursor_one, name)
                                                        SepCursor_one.clear()
                                                SepCursor_10.clear()
                                    SepCursor_50.clear()
                        SepCursor_250.clear()
            SepCursor.clear()
            if count % 1000 == 0:
                time.sleep(sleep)
    if len(SepCursor) != 0:
        study_plans_disciplines = dict()
        headers = {'Content-Type': 'application/json', 'X-CN-UUID': ''}
        study_plans_disciplines["organization_id"] = ""
        study_plans_disciplines[name] = SepCursor
        Addstudy_plans_disciplines = requests.post(link, headers=headers, json=study_plans_disciplines, verify=False)
        print(Addstudy_plans_disciplines.status_code)
        if str(Addstudy_plans_disciplines.status_code) == str(201):
            count += len(SepCursor)
            uiNmae.progressBar_upload.setValue(
                int((100 / len(all_string_for_update)) * count))
            uiNmae.count_progress.setText(str(count) + "/" + str(len(all_string_for_update)))
        if str(Addstudy_plans_disciplines.status_code) != str(201):
            if len(SepCursor) >= 50:
                for row in SepCursor:
                    SepCursor_50.append(row)
                    if len(SepCursor_50) == 50:
                        study_plans_disciplines[name] = SepCursor_50
                        Addstudy_plans_disciplines = requests.post(link, headers=headers, json=study_plans_disciplines, verify=False)
                        if str(Addstudy_plans_disciplines.status_code) == str(201):
                            count += 50
                            uiNmae.progressBar_upload.setValue(
                                int((100 / len(all_string_for_update)) * count))
                            uiNmae.count_progress.setText(
                                str(count) + "/" + str(len(all_string_for_update)))
                        print(Addstudy_plans_disciplines.status_code, 50, count)
                        if str(Addstudy_plans_disciplines.status_code) != str(201):
                            for row in SepCursor_50:
                                SepCursor_10.append(row)
                                if len(SepCursor_10) == 10:
                                    study_plans_disciplines[name] = SepCursor_10
                                    Addstudy_plans_disciplines = requests.post(link, headers=headers,
                                                                               json=study_plans_disciplines, verify=False)
                                    if str(Addstudy_plans_disciplines.status_code) == str(201):
                                        count += 10
                                        uiNmae.progressBar_upload.setValue(
                                            int((100 / len(all_string_for_update)) * count))
                                        uiNmae.count_progress.setText(
                                            str(count) + "/" + str(len(all_string_for_update)))
                                    print(Addstudy_plans_disciplines.status_code, 10, count)
                                    if str(Addstudy_plans_disciplines.status_code) != str(201):
                                        for row in SepCursor_10:
                                            SepCursor_one.append(row)
                                            study_plans_disciplines[name] = SepCursor_one
                                            Addstudy_plans_disciplines = requests.post(link,
                                                headers=headers, json=study_plans_disciplines, verify=False)
                                            if str(Addstudy_plans_disciplines.status_code) == str(201):
                                                count += 1
                                                uiNmae.progressBar_upload.setValue(
                                                    int((100 / len(all_string_for_update)) * count))
                                                uiNmae.count_progress.setText(
                                                    str(count) + "/" + str(len(all_string_for_update)))
                                            print(Addstudy_plans_disciplines.status_code, 1, count)
                                            if Addstudy_plans_disciplines.status_code == 400:
                                                exception_list(SepCursor_one, name)
                                            SepCursor_one.clear()
                                    SepCursor_10.clear()
                        SepCursor_50.clear()
                SepCursor.clear()
            if len(SepCursor) < 50:
                for row in SepCursor:
                    SepCursor_one.append(row)
                    study_plans_disciplines[name] = SepCursor_one
                    Addstudy_plans_disciplines = requests.post(link, headers=headers, json=study_plans_disciplines, verify=False)
                    count += 1
                    uiNmae.progressBar_upload.setValue(
                        int((100 / len(all_string_for_update)) * count))
                    uiNmae.count_progress.setText(str(count) + "/" + str(len(all_string_for_update)))
                    print(Addstudy_plans_disciplines.status_code, 1, count)
                    if Addstudy_plans_disciplines.status_code == 400:
                        exception_list(SepCursor_one, name)
                    SepCursor_one.clear()
    # uiNmae.progressBar_upload.setValue(100)
    # uiNmae.count_progress.setText(str(len(all_string_for_update)) + "/" + str(len(all_string_for_update)))
    uiNmae.progressBar_upload.setValue(int((100 / len(all_string_for_update)) * count))
    uiNmae.count_progress.setText(str(count) + "/" + str(len(all_string_for_update)))

def exception_list(SepCursor_one, name):
    file = open("example.txt", "w")

    # Создаем строку, которую мы хотим записать в файл
    string_to_write = SepCursor_one + name

    # Записываем строку в файл
    file.write(string_to_write)

    # Закрываем файл
    file.close()

# фиксация даты, активация\деактивация кнопок и смена надписи
def set_date():
    if ui.set_date.text() == "Зафиксировать год":
        ui.import_educational_programs.setEnabled(True)
        ui.import_study_plans.setEnabled(True)
        ui.import_discipline.setEnabled(True)
        ui.import_study_plans_discipline.setEnabled(True)
        ui.Upload_Students.setEnabled(True)
        ui.Upload_contingent_flows.setEnabled(True)
        ui.import_study_plan_students.setEnabled(True)
        ui.marks.setEnabled(True)
        ui.year_study.setEnabled(False)
        ui.set_date.setText("Изменить год")
    else:
        ui.import_educational_programs.setEnabled(False)
        ui.import_study_plans.setEnabled(False)
        ui.import_discipline.setEnabled(False)
        ui.import_study_plans_discipline.setEnabled(False)
        ui.Upload_Students.setEnabled(False)
        ui.Upload_contingent_flows.setEnabled(False)
        ui.import_study_plan_students.setEnabled(False)
        ui.marks.setEnabled(False)
        ui.year_study.setEnabled(True)
        ui.set_date.setText("Зафиксировать год")
# кнопка фиксации учебного года
# ----------------------------------------------------------------------------
ui.set_date.clicked.connect(set_date)
# ----------------------------------------------------------------------------
# первая загрузка, дополнительное окно
def importEducationPrograms():
    global UploadWindowEducation
    global uiEducation
    UploadWindowEducation = QtWidgets.QMainWindow()
    uiEducation = Ui_UploadWindow()
    uiEducation.setupUi(UploadWindowEducation)
    UploadWindowEducation.show()
    UploadWindowEducation.setWindowTitle("Import education programs")
    uiEducation.upload_choice.setEnabled(False)
    uiEducation.upload_all.setEnabled(False)
    uiEducation.count_site.setText("Ищем...")
    uiEducation.count_db.setText("Ищем...")
    uiEducation.count_choice.setText("Ищем...")
    th1 = Thread(target=education_program_all_result)
    th1.start()
    uiEducation.upload_all.clicked.connect(upload_all_education)
    uiEducation.upload_choice.clicked.connect(upload_chose_education)
    uiEducation.pushButton.clicked.connect(UploadWindowEducation.close)
# функция для запуска загрузки недостающих в отдельном потоке
def upload_chose_education():
    th = Thread(target=import_educational_programs_choise)
    th.start()
# то же самое, только всех и с ожиданием, иначе крашит
def upload_all_education():
    th = Thread(target=import_educational_programs_all)
    th.start()
    # th.join()

# получаем результаты с бд, сайта и находим разницу
def education_program_all_result():
    while uiEducation.count_db.text() == "Ищем...":
        print("poshlo")
        global last_external_id_education
        global all_strirng_education
        all_strirng_education = list()
        connection = Connection_BD()
        cursor = connection.cursor()
        external_id_db = list()
        external_id_site = educational_programs_site()
        SepCursor = list()
        ED_programm = cursor.execute(
            "select v.id,v.uroven,v.name,sp.name,v.uch_gog from  (select sp.id,sp.name,sp.spec_id,sp.uroven,pl.uch_gog from (select * from u_plan where uch_gog='" + str(ui.year_study.text()) + "' and u_plan.typlan_code=3) pl right join u_plan_string str on pl.upl_id=str.upl_id join u_napr_spec sp on sp.id=pl.spec_id join u_discipls ds on ds.code=str.dis_code join u_el_string el on el.spl_str_id=str.str_id where pl.upl_id is not null group by sp.id,sp.name,sp.spec_id,sp.uroven,pl.uch_gog) v  left join (select * from u_napr_spec where uroven=1) sp on sp.id=v.spec_id")
        for row in ED_programm:
            all_strirng_education.append(row)
        ED_programm.close()
        connection.close()
        for ed in all_strirng_education:
            external_id_db.append(ed[0])
        last_external_id_education = list(set(external_id_db) - set(external_id_site))
        uiEducation.count_db.setText(str(len(all_strirng_education)))
        uiEducation.count_site.setText(str(len(external_id_site)))
        uiEducation.count_choice.setText(str(len(last_external_id_education)))
        uiEducation.upload_choice.setEnabled(True)
        uiEducation.upload_all.setEnabled(True)

# функция загрузки недостающих
def import_educational_programs_choise():
    uiEducation.upload_choice.setEnabled(False)
    uiEducation.upload_all.setEnabled(False)
    uiEducation.count_site.setText("Ищем...")
    uiEducation.count_db.setText("Ищем...")
    uiEducation.count_choice.setText("Ищем...")
    SepCursor = list()

    for ed in all_strirng_education:
        for row in last_external_id_education:
            if int(row) == ed[0]:

                if ed[3] == None:
                    str = ed[2]
                else:
                    str = ed[3]
                chunks = str.split(' ', 1)

                chunks1 = ed[4].split('/', 1)

                dictTemp = {"external_id": ed[0], "title": ed[2], "direction": chunks[1], "code_direction": chunks[0],
                            "start_year": chunks1[0], "end_year": chunks1[1]}
                SepCursor.append(dictTemp)
    count_check = 0
    global count
    count = 0
    while len(SepCursor) != 0:
        count_check += len(SepCursor[0:500])
        while count != count_check and len(SepCursor) != 0:
            zapusk(SepCursor[0:500], uiEducation, "https://tls.online.edu.ru/vam/api/v2/educational_programs",
                   "educational_programs", 0, last_external_id_education)
            print("\n", len(SepCursor), "\n", count_check, count)
        del SepCursor[0:500]
    #             if len(SepCursor) == 100:
    #                 educational_programs = dict()
    #                 headers = {'Content-Type': 'application/json', 'X-CN-UUID': ''}
    #                 educational_programs["organization_id"] = ""
    #                 educational_programs["educational_programs"] = SepCursor
    #                 AddEducational_programs = requests.post("https://tls.online.edu.ru/vam/api/v2/educational_programs", headers=headers, json=educational_programs,  verify=False)
    #                 print(AddEducational_programs.status_code)
    #                 SepCursor.clear()
    #                 uiEducation.progressBar_upload.setValue(int((100/len(last_external_id_education))*count))
    #                 uiEducation.count_progress.setText(str(count) + "/" + str(len(last_external_id_education)))
    #
    # if len(SepCursor) != 0:
    #     educational_programs = dict()
    #     headers = {'Content-Type': 'application/json', 'X-CN-UUID': ''}
    #     educational_programs["organization_id"] = ""
    #     educational_programs["educational_programs"] = SepCursor
    #     AddEducational_programs = requests.post("https://tls.online.edu.ru/vam/api/v2/educational_programs",
    #                                             headers=headers, json=educational_programs, verify=False)
    #     print(AddEducational_programs.status_code)
    #     SepCursor.clear()
    # uiEducation.progressBar_upload.setValue(100)
    education_program_all_result()
# функция загрузки всех подряд
def import_educational_programs_all():
    uiEducation.upload_choice.setEnabled(False)
    uiEducation.upload_all.setEnabled(False)
    uiEducation.count_site.setText("Ищем...")
    uiEducation.count_db.setText("Ищем...")
    uiEducation.count_choice.setText("Ищем...")
    SepCursor = list()
    for ed in all_strirng_education:
        if ed[3] == None:
            str = ed[2]
        else:
            str = ed[3]
        chunks = str.split(' ', 1)

        chunks1 = ed[4].split('/', 1)

        dictTemp = {"external_id": ed[0], "title": ed[2], "direction": chunks[1], "code_direction": chunks[0],
                    "start_year": chunks1[0], "end_year": chunks1[1]}
        SepCursor.append(dictTemp)
    count_check = 0
    global count
    count = 0
    while len(SepCursor) != 0:
        count_check += len(SepCursor[0:500])
        while count != count_check and len(SepCursor) != 0:
            zapusk(SepCursor[0:500], uiEducation, "https://tls.online.edu.ru/vam/api/v2/educational_programs",
                   "educational_programs", 0, all_strirng_education)
            print("\n", len(SepCursor), "\n", count_check, count)
        del SepCursor[0:500]
    #     if len(SepCursor) == 100:
    #         educational_programs = dict()
    #         headers = {'Content-Type': 'application/json', 'X-CN-UUID': ''}
    #         educational_programs["organization_id"] = ""
    #         educational_programs["educational_programs"] = SepCursor
    #         AddEducational_programs = requests.post("https://tls.online.edu.ru/vam/api/v2/educational_programs",
    #                                                 headers=headers, json=educational_programs, verify=False)
    #         print(AddEducational_programs.status_code)
    #         SepCursor.clear()
    #         uiEducation.progressBar_upload.setValue(int((100 / len(all_strirng_education)) * count))
    #
    # if len(SepCursor) != 0:
    #     educational_programs = dict()
    #     headers = {'Content-Type': 'application/json', 'X-CN-UUID': ''}
    #     educational_programs["organization_id"] = ""
    #     educational_programs["educational_programs"] = SepCursor
    #     AddEducational_programs = requests.post("https://tls.online.edu.ru/vam/api/v2/educational_programs",
    #                                             headers=headers, json=educational_programs, verify=False)
    #     print(AddEducational_programs.status_code)
    #     SepCursor.clear()
    # uiEducation.progressBar_upload.setValue(100)
    education_program_all_result()
# функция для получения информации с сайта
def educational_programs_site():
    external_id_site = list()
    Student = dict()
    headers = {'Content-Type': 'application/json', 'X-CN-UUID': ''}
    Student["organization_id"] = ""
    last_page = requests.get("https://tls.online.edu.ru/vam/api/v2/educational_programs?page_size=1",
                               headers=headers, json=Student, verify=False)

    education = requests.get("https://tls.online.edu.ru/vam/api/v2/educational_programs?page_size=" + str(last_page.json()["last_page"]),
                               headers=headers, json=Student, verify=False)
    date = education.json()
    for row in date["results"]:
        external_id_site.append(int(row["external_id"]))
    return external_id_site
# запуск окна первой загрузки
# ----------------------------------------------------------------------------
ui.import_educational_programs.clicked.connect(importEducationPrograms)
# ----------------------------------------------------------------------------
# окно второй загрузки
def importstudyplans():
    global UploadWindowPlans
    global uiPlans
    UploadWindowPlans = QtWidgets.QMainWindow()
    uiPlans = Ui_UploadWindow()
    uiPlans.setupUi(UploadWindowPlans)
    UploadWindowPlans.show()
    uiPlans.upload_choice.setEnabled(False)
    uiPlans.upload_all.setEnabled(False)
    uiPlans.count_site.setText("Ищем...")
    uiPlans.count_db.setText("Ищем...")
    uiPlans.count_choice.setText("Ищем...")
    th1 = Thread(target=study_plan_all_result)
    th1.start()
    uiPlans.upload_all.clicked.connect(upload_all_plans)
    uiPlans.upload_choice.clicked.connect(upload_chose_plans)
    uiPlans.pushButton.clicked.connect(UploadWindowPlans.close)
# загрузка недостающих в отдельном потоке
def upload_chose_plans():
    th = Thread(target=import_study_plans_choise)
    th.start()
# загрузка всех в отдельном потоке с ожиданием, иначе крашит
def upload_all_plans():
    th = Thread(target=import_study_plans_all)
    th.start()
    # th.join()
# все результаты, с бд, сайта и их разница
def study_plan_all_result():
    global last_external_id_plans
    global all_string_plans
    all_string_plans = list()
    connection = Connection_BD()
    cursor = connection.cursor()
    external_id_db = list()
    Study_plan = cursor.execute(
        "select v.upl_id,v.data_utv,np1.name,v.uch_gog,v.fedu_id,v.spec_id from (select pl.upl_id,pl.data_utv,pl.uch_gog,pl.fedu_id,pl.spec_id from (select * from u_plan where uch_gog='" + str(ui.year_study.text()) + "' and u_plan.typlan_code=3 and fedu_id is not null) pl right join u_plan_string str on pl.upl_id=str.upl_id join u_napr_spec sp on sp.id=pl.spec_id join u_discipls ds on ds.code=str.dis_code join u_el_string el on el.spl_str_id=str.str_id where pl.upl_id is not null GROUP BY pl.upl_id,pl.data_utv,pl.uch_gog,pl.fedu_id,pl.spec_id) v  left join (select * from u_napr_spec where uroven=2) np2 on np2.id=v.spec_id left join (select * from u_napr_spec where uroven=1) np1 on np1.id=v.spec_id or np1.id=np2.spec_id")
    for row in Study_plan:
        all_string_plans.append(row)
    Study_plan.close()
    connection.close()
    for sp in all_string_plans:
        external_id_db.append(str(sp[0]))
    external_id_site = study_plans_site()
    last_external_id_plans = list(set(external_id_db) - set(external_id_site))
    uiPlans.count_db.setText(str(len(all_string_plans)))
    uiPlans.count_site.setText(str(len(external_id_site)))
    uiPlans.count_choice.setText(str(len(last_external_id_plans)))
    uiPlans.upload_choice.setEnabled(True)
    uiPlans.upload_all.setEnabled(True)
# получаем информацию с сайта
def study_plans_site():
    study_plans = dict()
    external_id_site = list()
    headers = {'Content-Type': 'application/json', 'X-CN-UUID': ''}
    study_plans["organization_id"] = ""
    last_page = requests.get("https://tls.online.edu.ru/vam/api/v2/study_plans?page_size=1", headers=headers, json=study_plans,
                                  verify=False)
    plans = requests.get("https://tls.online.edu.ru/vam/api/v2/study_plans?page_size=" + str(last_page.json()["last_page"]),
                                  headers=headers, json=study_plans, verify=False)
    # print(plans.json())
    for row in plans.json()["results"]:
        external_id_site.append(str(row["external_id"]))
    return external_id_site
# загружаем недостающих
def import_study_plans_choise():
    uiPlans.upload_choice.setEnabled(False)
    uiPlans.upload_all.setEnabled(False)
    uiPlans.count_site.setText("Ищем...")
    uiPlans.count_db.setText("Ищем...")
    uiPlans.count_choice.setText("Ищем...")
    SepCursor = list()
    for sp in all_string_plans:
        for row in last_external_id_plans:
            if int(row) == sp[0]:
                print(sp[2], '\n', sp[3])
                try:
                    chunks = sp[2].split(' ', 1)
                except:
                    chunks = str(sp[2]).split(' ', 1)
                chunks1 = sp[3].split('/', 1)
                if sp[1] == None:
                    SP_name = "Рабочий план от 01.09." + str(ui.year_study.text()).split('/')[0]
                else:
                    SP_name = "Рабочий план от " + sp[1].strftime("%d.%m.%Y")
                ED_form = ""
                if sp[4] == 1 or sp[4] == 16 or sp[4] == 24:
                    ED_form = "FULL_TIME"
                if sp[4] == 2 or sp[4] == 21:
                    ED_form = "PART_TIME"
                if sp[4] == 3 or sp[4] == 17:
                    ED_form = "EXTRAMURAL"
                try:
                    dictTemp = {"external_id": sp[0], "title": SP_name, "direction": chunks[1], "code_direction": chunks[0],
                                "start_year": chunks1[0], "end_year": chunks1[1], "education_form": ED_form,
                                "educational_program": sp[5]}
                except:
                    dictTemp = {"external_id": sp[0], "title": SP_name, "direction": None,
                                "code_direction": None,
                                "start_year": None, "end_year": None, "education_form": ED_form,
                                "educational_program": sp[5]}
                SepCursor.append(dictTemp)
    count_check = 0
    global count
    count = 0
    while len(SepCursor) != 0:
        count_check += len(SepCursor[0:500])
        while count != count_check and len(SepCursor) != 0:
            zapusk(SepCursor[0:500], uiPlans, "https://tls.online.edu.ru/vam/api/v2/study_plans",
                   "study_plans", 0, last_external_id_plans)
            print("\n", len(SepCursor), "\n", count_check, count)
        del SepCursor[0:500]
    #             if len(SepCursor) == 300:
    #                 study_plans = dict()
    #                 headers = {'Content-Type': 'application/json', 'X-CN-UUID': ''}
    #                 study_plans["organization_id"] = ""
    #                 study_plans["study_plans"] = SepCursor
    #                 AddStudy_plans = requests.post("https://tls.online.edu.ru/vam/api/v2/study_plans", headers=headers,
    #                                                json=study_plans, verify=False)
    #                 print(AddStudy_plans.status_code)
    #                 SepCursor.clear()
    #                 uiPlans.progressBar_upload.setValue(int((100 / len(last_external_id_plans)) * count))
    # if len(SepCursor) != 0:
    #     study_plans = dict()
    #     headers = {'Content-Type': 'application/json', 'X-CN-UUID': ''}
    #     study_plans["organization_id"] = ""
    #     study_plans["study_plans"] = SepCursor
    #     AddStudy_plans = requests.post("https://tls.online.edu.ru/vam/api/v2/study_plans", headers=headers,
    #                                    json=study_plans, verify=False)
    #     print(AddStudy_plans.status_code)
    #     SepCursor.clear()
    # uiPlans.progressBar_upload.setValue(100)
    study_plan_all_result()
# загружаем всех
def import_study_plans_all():
    uiPlans.upload_choice.setEnabled(False)
    uiPlans.upload_all.setEnabled(False)
    uiPlans.count_site.setText("Ищем...")
    uiPlans.count_db.setText("Ищем...")
    uiPlans.count_choice.setText("Ищем...")
    SepCursor = list()
    for sp in all_string_plans:
        # print(sp[2], '\n', sp[3])
        try:
            chunks = sp[2].split(' ', 1)
        except:
            chunks = str(sp[2]).split(' ', 1)
        chunks1 = sp[3].split('/', 1)
        if sp[1] == None:
            SP_name = "Рабочий план от 01.01." + str(ui.year_study.text()).split('/')[0]
        else:
            SP_name = "Рабочий план от " + sp[1].strftime("%d.%m.%Y")
        ED_form = ""
        if sp[4] == 1 or sp[4] == 16 or sp[4] == 24:
            ED_form = "FULL_TIME"
        if sp[4] == 2 or sp[4] == 21:
            ED_form = "PART_TIME"
        if sp[4] == 3 or sp[4] == 17:
            ED_form = "EXTRAMURAL"
        try:
            dictTemp = {"external_id": sp[0], "title": SP_name, "direction": chunks[1], "code_direction": chunks[0],
                        "start_year": chunks1[0], "end_year": chunks1[1], "education_form": ED_form,
                        "educational_program": sp[5]}
        except:
            dictTemp = {"external_id": sp[0], "title": SP_name, "direction": None,
                        "code_direction": None,
                        "start_year": None, "end_year": None, "education_form": ED_form,
                        "educational_program": sp[5]}
            # print(dictTemp)
            print("ne dobavil")
        SepCursor.append(dictTemp)
    count_check = 0
    global count
    count = 0
    while len(SepCursor) != 0:
        count_check += len(SepCursor[0:500])
        while count != count_check and len(SepCursor) != 0:
            zapusk(SepCursor[0:500], uiPlans, "https://tls.online.edu.ru/vam/api/v2/study_plans",
                   "study_plans", 0, all_string_plans)
            print("\n", len(SepCursor), "\n", count_check, count)
        del SepCursor[0:500]
    #     if len(SepCursor) == 300:
    #         study_plans = dict()
    #         headers = {'Content-Type': 'application/json', 'X-CN-UUID': ''}
    #         study_plans["organization_id"] = ""
    #         study_plans["study_plans"] = SepCursor
    #         AddStudy_plans = requests.post("https://tls.online.edu.ru/vam/api/v2/study_plans", headers=headers,
    #                                        json=study_plans, verify=False)
    #         print(AddStudy_plans.status_code)
    #         SepCursor.clear()
    #         uiPlans.progressBar_upload.setValue(int((100 / len(all_string_plans)) * count))
    # if len(SepCursor) != 0:
    #     study_plans = dict()
    #     headers = {'Content-Type': 'application/json', 'X-CN-UUID': ''}
    #     study_plans["organization_id"] = ""
    #     study_plans["study_plans"] = SepCursor
    #     AddStudy_plans = requests.post("https://tls.online.edu.ru/vam/api/v2/study_plans", headers=headers,
    #                                    json=study_plans, verify=False)
    #     print(AddStudy_plans.status_code)
    #     SepCursor.clear()
    # uiPlans.progressBar_upload.setValue(100)
    study_plan_all_result()

# запускаем вторую загрузку
# ----------------------------------------------------------------------------
ui.import_study_plans.clicked.connect(importstudyplans)
# ----------------------------------------------------------------------------

# окно третей загрузки
def importdiscipline():
    global UploadWindowdisciplin
    global uiDisciplin
    UploadWindowdisciplin = QtWidgets.QMainWindow()
    uiDisciplin = Ui_UploadWindow()
    uiDisciplin.setupUi(UploadWindowdisciplin)
    UploadWindowdisciplin.show()
    uiDisciplin.upload_choice.setEnabled(False)
    uiDisciplin.upload_all.setEnabled(False)
    uiDisciplin.count_site.setText("Ищем...")
    uiDisciplin.count_db.setText("Ищем...")
    uiDisciplin.count_choice.setText("Ищем...")
    th1 = Thread(target=discipline_all_result)
    th1.start()
    uiDisciplin.upload_all.clicked.connect(upload_all_disciplin)
    uiDisciplin.upload_choice.clicked.connect(upload_chose_disciplin)
    uiDisciplin.pushButton.clicked.connect(UploadWindowdisciplin.close)
# загрузка недостающих в отдельном потоке
def upload_chose_disciplin():
    th = Thread(target=import_discipline_choise)
    th.start()
# загрузка всех в отдельном потоке с ожиданием, иначе крашит
def upload_all_disciplin():
    th = Thread(target=import_discipline_all)
    th.start()
    # th.join()
# все результаты, с бд, сайта и их разница
def discipline_all_result():
    global last_external_id_discipline
    global all_string_discipline
    all_string_discipline = list()
    connection = Connection_BD()
    cursor = connection.cursor()
    external_id_db = list()
    discipline = cursor.execute(
        "select ds.code,ds.name from (select * from u_plan where uch_gog='" + str(ui.year_study.text()) + "' and u_plan.typlan_code=3 and fedu_id is not null) pl right join u_plan_string str on pl.upl_id=str.upl_id join u_napr_spec sp on sp.id=pl.spec_id join u_discipls ds on ds.code=str.dis_code join u_el_string el on el.spl_str_id=str.str_id where pl.upl_id is not null group by ds.code,ds.name")
    for row in discipline:
        all_string_discipline.append(row)
    discipline.close()
    connection.close()
    for sp in all_string_discipline:
        external_id_db.append(str(sp[0]))
    external_id_site = discipline_site()
    last_external_id_discipline = list(set(external_id_db) - set(external_id_site))
    uiDisciplin.count_db.setText(str(len(all_string_discipline)))
    uiDisciplin.count_site.setText(str(len(external_id_site)))
    uiDisciplin.count_choice.setText(str(len(last_external_id_discipline)))
    uiDisciplin.upload_choice.setEnabled(True)
    uiDisciplin.upload_all.setEnabled(True)
# получаем информацию с сайта
def discipline_site():
    study_plans = dict()
    external_id_site = list()
    headers = {'Content-Type': 'application/json', 'X-CN-UUID': ''}
    study_plans["organization_id"] = ""
    last_page = requests.get("https://tls.online.edu.ru/vam/api/v2/disciplines?page_size=1", headers=headers, json=study_plans,
                                  verify=False)
    discipline = requests.get("https://tls.online.edu.ru/vam/api/v2/disciplines?page_size=" + str(last_page.json()["last_page"]),
                                  headers=headers, json=study_plans, verify=False)
    # print(discipline.json())
    for row in discipline.json()["results"]:
        external_id_site.append(str(row["external_id"]))
    return external_id_site
# загрузка недостающих
def import_discipline_choise():
    uiDisciplin.upload_choice.setEnabled(False)
    uiDisciplin.upload_all.setEnabled(False)
    uiDisciplin.count_site.setText("Ищем...")
    uiDisciplin.count_db.setText("Ищем...")
    uiDisciplin.count_choice.setText("Ищем...")
    SepCursor = list()
    for ds in all_string_discipline:
        for row in last_external_id_discipline:
            if int(row) == ds[0]:
                dictTemp = {"external_id": str(ds[0]), "title": str(ds[1][0:199])}
                SepCursor.append(dictTemp)
    count_check = 0
    global count
    count = 0
    while len(SepCursor) != 0:
        count_check += len(SepCursor[0:500])
        while count != count_check and len(SepCursor) != 0:
            zapusk(SepCursor[0:500], uiDisciplin, "https://tls.online.edu.ru/vam/api/v2/disciplines",
                   "disciplines", 0, last_external_id_discipline)
            print("\n", len(SepCursor), "\n", count_check, count)
        del SepCursor[0:500]
    #             if len(SepCursor) == 1000:
    #                 disciplines = dict()
    #                 headers = {'Content-Type': 'application/json', 'X-CN-UUID': ''}
    #                 disciplines["organization_id"] = ""
    #                 disciplines["disciplines"] = SepCursor
    #                 AddDisciplines = requests.post("https://tls.online.edu.ru/vam/api/v2/disciplines", headers=headers, json=disciplines, verify=False)
    #                 print(AddDisciplines.status_code)
    #                 SepCursor.clear()
    #                 uiDisciplin.progressBar_upload.setValue(int((100 / len(last_external_id_plans)) * count))
    # if len(SepCursor) != 0:
    #     disciplines = dict()
    #     headers = {'Content-Type': 'application/json', 'X-CN-UUID': ''}
    #     disciplines["organization_id"] = ""
    #     disciplines["disciplines"] = SepCursor
    #     AddDisciplines = requests.post("https://tls.online.edu.ru/vam/api/v2/disciplines", headers=headers,
    #                                    json=disciplines, verify=False)
    #     print(AddDisciplines.status_code)
    #     SepCursor.clear()
    #     uiDisciplin.progressBar_upload.setValue(100)
    discipline_all_result()
# загрузка всех
def import_discipline_all():
    uiDisciplin.upload_choice.setEnabled(False)
    uiDisciplin.upload_all.setEnabled(False)
    uiDisciplin.count_site.setText("Ищем...")
    uiDisciplin.count_db.setText("Ищем...")
    uiDisciplin.count_choice.setText("Ищем...")
    SepCursor = list()
    for ds in all_string_discipline:
        dictTemp = {"external_id": str(ds[0]), "title": str(ds[1][0:199])}
        SepCursor.append(dictTemp)
    count_check = 0
    global count
    count = 0
    while len(SepCursor) != 0:
        count_check += len(SepCursor[0:500])
        while count != count_check and len(SepCursor) != 0:
            zapusk(SepCursor[0:500], uiDisciplin, "https://tls.online.edu.ru/vam/api/v2/disciplines",
                   "disciplines", 0, all_string_discipline)
            print("\n", len(SepCursor), "\n", count_check, count)
        del SepCursor[0:500]
    # upload_kusochkami(SepCursor, uiDisciplin, "https://tls.online.edu.ru/vam/api/v2/disciplines",
    #                   "disciplines", 0, all_string_discipline)
    discipline_all_result()


# запускаем третью загрузку
# ----------------------------------------------------------------------------
ui.import_discipline.clicked.connect(importdiscipline)
# ----------------------------------------------------------------------------

# окно четвертой загрузки
def importStudyPlanDisciplin():
    global UploadWindowPlanDisciplin
    global uiPlanDisciplin
    UploadWindowPlanDisciplin = QtWidgets.QMainWindow()
    uiPlanDisciplin = Ui_UploadWindow()
    uiPlanDisciplin.setupUi(UploadWindowPlanDisciplin)
    UploadWindowPlanDisciplin.show()
    uiPlanDisciplin.upload_choice.setEnabled(False)
    uiPlanDisciplin.upload_all.setEnabled(False)
    uiPlanDisciplin.count_site.setText("--")
    uiPlanDisciplin.count_db.setText("Ищем...")
    uiPlanDisciplin.count_choice.setText("--")
    th1 = Thread(target=plan_discipline_all_result)
    th1.start()
    uiPlanDisciplin.upload_all.clicked.connect(upload_all_plan_disciplin)
    uiPlanDisciplin.pushButton.clicked.connect(UploadWindowPlanDisciplin.close)
# загрузка всех в отдельном потоке с ожиданием, иначе крашит
def upload_all_plan_disciplin():
    uiPlanDisciplin.upload_all.setEnabled(False)
    th = Thread(target=import_study_plans_discipline)
    th.start()
    # th.join()
# все результаты с бд
def plan_discipline_all_result():
    global all_string_plan_discipline
    all_string_plan_discipline = list()
    connection = Connection_BD()
    cursor = connection.cursor()
    external_id_db = list()
    SPD = cursor.execute(
        "select ds.code,pl.upl_id,el.period_num from (select * from u_plan where uch_gog='" + str(ui.year_study.text()) + "' and u_plan.typlan_code=3 and fedu_id is not null) pl right join u_plan_string str on pl.upl_id=str.upl_id join u_napr_spec sp on sp.id=pl.spec_id join u_discipls ds on ds.code=str.dis_code join u_el_string el on el.spl_str_id=str.str_id where pl.upl_id is not null group by ds.code,pl.upl_id,el.period_num")
    for row in SPD:
        all_string_plan_discipline.append(row)
    SPD.close()
    connection.close()
    for sp in all_string_plan_discipline:
        external_id_db.append(str(sp[0]))
    uiPlanDisciplin.count_db.setText(str(len(all_string_plan_discipline)))
    uiPlanDisciplin.upload_all.setEnabled(True)
#загрузка всех
def import_study_plans_discipline():
    SepCursor = list()
    for ds in all_string_plan_discipline:
        dictTemp = {"study_plan": ds[1], "discipline": ds[0], "semester": ds[2]}
        SepCursor.append(dictTemp)
    # upload_kusochkami(SepCursor, uiPlanDisciplin, "https://tls.online.edu.ru/vam/api/v2/study_plans_disciplines",
    #                   "study_plan_disciplines", 5, all_string_plan_discipline)

    count_check = 0
    global count
    count = 0
    while len(SepCursor) != 0:
        count_check += len(SepCursor[0:500])
        while count != count_check and len(SepCursor) != 0:
            zapusk(SepCursor[0:500], uiPlanDisciplin, "https://tls.online.edu.ru/vam/api/v2/study_plans_disciplines",
                      "study_plan_disciplines", 0, all_string_plan_discipline)
            print("\n", len(SepCursor), "\n", count_check, count)
        del SepCursor[0:500]

    # count = 0
    # while len(SepCursor) != 0:
    #     disciplines = dict()
    #     headers = {'Content-Type': 'application/json', 'X-CN-UUID': ''}
    #     disciplines["organization_id"] = ""
    #     if len(SepCursor) >= 250:
    #         disciplines["study_plan_disciplines"] = SepCursor[0:250]
    #         AddDisciplines = requests.post("https://tls.online.edu.ru/vam/api/v2/study_plans_disciplines",
    #                                        headers=headers,
    #                                        json=disciplines, verify=False)
    #         if str(AddDisciplines.status_code) == str(201):
    #             del SepCursor[0:250]
    #             count += 250
    #             print(AddDisciplines.status_code, count)
    #         if str(AddDisciplines.status_code) != str(201):
    #             for i in range(0, 25):
    #                 disciplines["study_plan_disciplines"] = SepCursor[0:10]
    #                 AddDisciplines = requests.post("https://tls.online.edu.ru/vam/api/v2/study_plans_disciplines",
    #                                                headers=headers,
    #                                                json=disciplines, verify=False)
    #                 if str(AddDisciplines.status_code) == str(201):
    #                     count += 10
    #                     del SepCursor[0:10]
    #                     print(AddDisciplines.status_code, count)
    #                 if str(AddDisciplines.status_code) != str(201):
    #                     for i in range(0, 10):
    #                         disciplines["study_plan_disciplines"] = SepCursor[0:1]
    #                         AddDisciplines = requests.post(
    #                             "https://tls.online.edu.ru/vam/api/v2/study_plans_disciplines",
    #                             headers=headers,
    #                             json=disciplines, verify=False)
    #                         count += 1
    #                         del SepCursor[0:1]
    #                         print(AddDisciplines.status_code, count)
    #     else:
    #         disciplines["study_plan_disciplines"] = SepCursor
    #         AddDisciplines = requests.post("https://tls.online.edu.ru/vam/api/v2/study_plans_disciplines",
    #                                        headers=headers,
    #                                        json=disciplines, verify=False)
    #         count += len(SepCursor)
    #         print(AddDisciplines.status_code, count)


    uiPlanDisciplin.upload_all.setEnabled(True)


# запускаем четвертую загрузку
# ----------------------------------------------------------------------------
ui.import_study_plans_discipline.clicked.connect(importStudyPlanDisciplin)
# ----------------------------------------------------------------------------

# окно пятой загрузки
def Upload_Students_window():
    global UploadWindowStudents
    global uiStudents
    UploadWindowStudents = QtWidgets.QMainWindow()
    uiStudents = Ui_UploadWindow()
    uiStudents.setupUi(UploadWindowStudents)
    UploadWindowStudents.show()
    uiStudents.upload_choice.setEnabled(False)
    uiStudents.upload_all.setEnabled(False)
    uiStudents.count_site.setText("Ищем...")
    uiStudents.count_db.setText("Ищем...")
    uiStudents.count_choice.setText("Ищем...")
    # start_students_all_result()
    th1 = Thread(target=students_all_result)
    th1.start()
    uiStudents.upload_all.clicked.connect(upload_all_students)
    uiStudents.upload_choice.clicked.connect(upload_chose_students)
    uiStudents.pushButton.clicked.connect(UploadWindowStudents.close)
def start_students_all_result():
    while uiStudents.count_db.text() == "Ищем...":
        print("poshlo")
        th1 = Thread(target=students_all_result)
        th1.start()
# загрузка недостающих в отдельном потоке
def upload_chose_students():
    th = Thread(target=Upload_Students_choise)
    th.start()
# загрузка всех в отдельном потоке с ожиданием, иначе крашит
def upload_all_students():
    th = Thread(target=Upload_Students_all)
    th.start()
    # th.join()
# все результаты, с бд, сайта и их разница
def students_all_result():
    global last_external_id_students
    global all_string_students
    all_string_students = list()
    connection = Connection_BD()
    cursor = connection.cursor()
    external_id_db = list()
    students = cursor.execute(
        "select ind.IND_ID,ind.snils_num,ind.INN,ind.kubsu_tab_num,pc.F_NAME,pc.I_NAME,pc.O_NAME,wp.Upl_upl_id from  o_individual ind  join (select * from O_PERSONAL_CARD where status='Y') pc on ind.IND_ID=pc.ind_ind_id join  (select * from o_work_place where status='Y' and st_stat_code in ('01', '03') and tst_tst_id=1 )wp on wp.pcard_pcard_id=pc.pcard_id ")
    for row in students:
        all_string_students.append(row)
    students.close()
    connection.close()
    for sp in all_string_students:
        external_id_db.append(str(sp[0]))
    external_id_site = Upload_Students_site()
    last_external_id_students = list(set(external_id_db) - set(external_id_site))
    uiStudents.count_db.setText(str(len(all_string_students)))
    uiStudents.count_site.setText(str(len(external_id_site)))
    uiStudents.count_choice.setText(str(len(last_external_id_students)))
    uiStudents.upload_choice.setEnabled(True)
    uiStudents.upload_all.setEnabled(True)
#данные с сайта
def Upload_Students_site():
    study_plans = dict()
    external_id_site = list()
    headers = {'Content-Type': 'application/json', 'X-CN-UUID': ''}
    study_plans["organization_id"] = ""
    last_page = requests.get("https://tls.online.edu.ru/vam/api/v2/students?page_size=1", headers=headers, json=study_plans,
                                  verify=False)
    discipline = requests.get("https://tls.online.edu.ru/vam/api/v2/students?page_size=" + str(last_page.json()["last_page"]),
                                  headers=headers, json=study_plans, verify=False)
    for row in discipline.json()["results"]:
        external_id_site.append(str(row["external_id"]))
    return external_id_site
#загрузка недостающих студентов
def Upload_Students_choise():
    uiStudents.count_site.setText("Ищем...")
    uiStudents.count_db.setText("Ищем...")
    uiStudents.count_choice.setText("Ищем...")
    uiStudents.upload_choice.setEnabled(False)
    uiStudents.upload_all.setEnabled(False)
    SepCursor = list()
    for ds in all_string_students:
        if str(ds[0]) in str(last_external_id_students):
            if len(str(ds[0])) == 7:
                ind = str(ds[0])
            elif len(str(ds[0])) == 6:
                ind = "0" + str(ds[0])
            elif len(str(ds[0])) == 5:
                ind = "00" + str(ds[0])
            elif len(str(ds[0])) == 4:
                ind = "000" + str(ds[0])
            elif len(str(ds[0])) == 3:
                ind = "0000" + str(ds[0])
            elif len(str(ds[0])) == 2:
                ind = "00000" + str(ds[0])
            elif len(str(ds[0])) == 1:
                ind = "000000" + str(ds[0])

            snils = ds[1]
            inn = ds[2]
            email = ds[3] if ds[3] == None else "s" + str(ind) + "@edu.kubsu.ru"
            dictTemp = {"external_id": ds[0], "surname": ds[5], "name": ds[6], "middle_name": ds[7], "snils": snils,
                        "inn": inn, "email": email}
            SepCursor.append(dictTemp)
    count_check = 0
    global count
    count = 0
    while len(SepCursor) != 0:
        count_check += len(SepCursor[0:500])
        while count != count_check and len(SepCursor) != 0:
            zapusk(SepCursor[0:500], uiStudents, "https://tls.online.edu.ru/vam/api/v2/students",
                   "students", 0, last_external_id_students)
            print("\n", len(SepCursor), "\n", count_check, count)
        del SepCursor[0:500]
    students_all_result()
#загрузка всех
def Upload_Students_all():
    uiStudents.count_site.setText("Ищем...")
    uiStudents.count_db.setText("Ищем...")
    uiStudents.count_choice.setText("Ищем...")
    uiStudents.upload_choice.setEnabled(False)
    uiStudents.upload_all.setEnabled(False)
    SepCursor = list()
    for ds in all_string_students:
        if len(str(ds[0])) == 7:
            ind = str(ds[0])
        elif len(str(ds[0])) == 6:
            ind = "0" + str(ds[0])
        elif len(str(ds[0])) == 5:
            ind = "00" + str(ds[0])
        elif len(str(ds[0])) == 4:
            ind = "000" + str(ds[0])
        elif len(str(ds[0])) == 3:
            ind = "0000" + str(ds[0])
        elif len(str(ds[0])) == 2:
            ind = "00000" + str(ds[0])
        elif len(str(ds[0])) == 1:
            ind = "000000" + str(ds[0])

        snils = ds[1]
        inn = ds[2]
        email = ds[3] if ds[3] == None else "s" + str(ind) + "@edu.kubsu.ru"
        dictTemp = {"external_id": ds[0], "surname": ds[5], "name": ds[6], "middle_name": ds[7], "snils": snils,
                    "inn": inn, "email": email}
        SepCursor.append(dictTemp)
    # upload_kusochkami(SepCursor, uiStudents, "https://tls.online.edu.ru/vam/api/v2/students",
    #                   "students", 1, all_string_students)

    count_check = 0
    global count
    count = 0
    while len(SepCursor) != 0:
        count_check += len(SepCursor[0:500])
        while count != count_check and len(SepCursor) != 0:
            zapusk(SepCursor[0:500], uiStudents, "https://tls.online.edu.ru/vam/api/v2/students",
                      "students", 0, all_string_students)
            print("\n", len(SepCursor), "\n", count_check, count)
        del SepCursor[0:500]

    students_all_result()


# запускаем пятую загрузку
# ----------------------------------------------------------------------------
ui.Upload_Students.clicked.connect(Upload_Students_window)
# ----------------------------------------------------------------------------

# окно шестой загрузки
def Upload_contingent_flows_Window():
    global UploadWindowcontingent
    global uiContingent
    UploadWindowcontingent = QtWidgets.QMainWindow()
    uiContingent = Ui_UploadWindow()
    uiContingent.setupUi(UploadWindowcontingent)
    UploadWindowcontingent.show()
    uiContingent.upload_choice.setEnabled(False)
    uiContingent.upload_all.setEnabled(False)
    uiContingent.count_site.setText("--")
    uiContingent.count_db.setText("Ищем...")
    uiContingent.count_choice.setText("--")
    th1 = Thread(target=contingent_flows_all_result)
    th1.start()
    uiContingent.upload_all.clicked.connect(upload_all_Contingent)
    uiContingent.pushButton.clicked.connect(UploadWindowcontingent.close)
# загрузка всех в отдельном потоке с ожиданием, иначе крашит
def upload_all_Contingent():
    uiContingent.upload_all.setEnabled(False)
    th = Thread(target=Upload_contingent_flows)
    th.start()
# все результаты с бд
def contingent_flows_all_result():
    global all_string_contingent_flows
    all_string_contingent_flows = list()
    connection = Connection_BD()
    cursor = connection.cursor()
    external_id_db = list()
    contingent_flows = cursor.execute(
        "select ind.IND_ID,wp1.st_stat_code,wp1.kaz_code,wp1.FROM_DATE,wp1.TO_DATE,wp1.modify_date,wp1.tcon_tcon_id,upl.fedu_id,fac.name_long,dog.name from  o_individual ind  join (select * from O_PERSONAL_CARD where status='Y') pc on ind.IND_ID=pc.ind_ind_id join  (select * from o_work_place where status='Y' and st_stat_code in ('01', '03') and tst_tst_id=1 )wp on wp.pcard_pcard_id=pc.pcard_id join   o_work_place wp1 on wp1.pcard_pcard_id=pc.pcard_id join   u_plan upl on upl.upl_id=wp.upl_upl_id join   o_use_base_units gr on gr.ubu_id=wp.ubu_ubu_id join   o_use_base_units kr on kr.ubu_id=gr.ubu_ubu_id join   o_use_base_units nap on nap.ubu_id=kr.ubu_ubu_id join   o_use_base_units forma on forma.ubu_id=nap.ubu_ubu_id join   o_use_base_units fac on fac.ubu_id=forma.ubu_ubu_id join   u_ab_type_dog dog on dog.code=wp1.tcon_tcon_id")
    for row in contingent_flows:
        all_string_contingent_flows.append(row)
    contingent_flows.close()
    connection.close()
    for sp in all_string_contingent_flows:
        external_id_db.append(str(sp[0]))
    uiContingent.count_db.setText(str(len(all_string_contingent_flows)))
    uiContingent.upload_all.setEnabled(True)
#загрузка всех
def Upload_contingent_flows():
    SepCursor = list()
    for row in all_string_contingent_flows:
        DateList = list()
        DateList.append(row[3]) if row[3] != None else None
        DateList.append(row[4]) if row[4] != None else None
        DateList.append(row[5]) if row[5] != None else None
        MaxDate = min(DateList)
        ED_form = ""
        if row[7] == 1 or row[7] == 16 or row[7] == 24:
            ED_form = "FULL_TIME"
        if row[7] == 2 or row[7] == 21:
            ED_form = "PART_TIME"
        if row[7] == 3 or row[7] == 17:
            ED_form = "EXTRAMURAL"
        if row[2] == "6":
            dictTemp = {"student": row[0], "flow_type": "REINSTATEMENT", "contingent_flow": "Восстановление",
                        "date": MaxDate.strftime("%Y-%m-%d"), "faculty": row[8], "education_form": ED_form,
                        "form_fin": row[9], "details": ""}
            SepCursor.append(dictTemp)
        if (int(row[1]) >= 63 and int(row[1]) <= 71) or int(row[1]) == 75:
            dictTemp = {"student": row[0], "flow_type": "DEDUCTION", "contingent_flow": "Отчисление из ООВО",
                        "date": MaxDate.strftime("%Y-%m-%d"), "faculty": row[8], "education_form": ED_form,
                        "form_fin": row[9], "details": ""}
            SepCursor.append(dictTemp)
        if int(row[1]) >= 27 and int(row[1]) <= 32:
            dictTemp = {"student": row[0], "flow_type": "SABBATICAL_TAKING",
                        "contingent_flow": "Предоставление академического отпуска",
                        "date": MaxDate.strftime("%Y-%m-%d"), "faculty": row[8], "education_form": ED_form,
                        "form_fin": row[9], "details": ""}
            SepCursor.append(dictTemp)
        if int(row[1]) == 72 and int(row[1]) == 74:
            dictTemp = {"student": row[0], "flow_type": "TRANSFER",
                        "contingent_flow": "Перевод на факультет/специальность", "date": MaxDate.strftime("%Y-%m-%d"),
                        "faculty": row[8], "education_form": ED_form, "form_fin": row[9], "details": ""}
            SepCursor.append(dictTemp)
        if int(row[1]) == 90:
            dictTemp = {"student": row[0], "flow_type": "TRANSFER", "contingent_flow": "Перевод на следующий курс",
                        "date": MaxDate.strftime("%Y-%m-%d"), "faculty": row[8], "education_form": ED_form,
                        "form_fin": row[9], "details": ""}
            SepCursor.append(dictTemp)
        if row[1] == "01" or row[1] == "03":
            dictTemp = {"student": row[0], "flow_type": "ENROLLMENT", "contingent_flow": "Зачисление в ООВО",
                        "date": MaxDate.strftime("%Y-%m-%d"), "faculty": row[8], "education_form": ED_form,
                        "form_fin": row[9], "details": ""}
            SepCursor.append(dictTemp)

    # upload_kusochkami(SepCursor, uiContingent, "https://tls.online.edu.ru/vam/api/v2/contingent_flows",
    #                   "contingent_flows", 6, all_string_contingent_flows)

    count_check = 0
    global count
    count = 0
    while len(SepCursor) != 0:
        count_check += len(SepCursor[0:500])
        while count != count_check and len(SepCursor) != 0:
            zapusk(SepCursor[0:500], uiContingent, "https://tls.online.edu.ru/vam/api/v2/contingent_flows",
                   "contingent_flows", 0, all_string_contingent_flows)
            print(count, count_check, len(SepCursor), len(all_string_contingent_flows))
        del SepCursor[0:500]

    contingent_flows_all_result()

# запускаем шестую загрузку
# ----------------------------------------------------------------------------
ui.Upload_contingent_flows.clicked.connect(Upload_contingent_flows_Window)
# ----------------------------------------------------------------------------

# окно седьмой загрузки
def Upload_study_plan_students_window():
    global UploadWindowPlanStudy
    global uiPlanStudy
    UploadWindowPlanStudy = QtWidgets.QMainWindow()
    uiPlanStudy = Ui_UploadWindow()
    uiPlanStudy.setupUi(UploadWindowPlanStudy)
    UploadWindowPlanStudy.show()
    uiPlanStudy.upload_choice.setEnabled(False)
    uiPlanStudy.upload_all.setEnabled(False)
    uiPlanStudy.count_site.setText("--")
    uiPlanStudy.count_db.setText("Ищем...")
    uiPlanStudy.count_choice.setText("--")
    th1 = Thread(target=study_plan_students_all_result)
    th1.start()
    uiPlanStudy.upload_all.clicked.connect(upload_all_study_plan_students)
    uiPlanStudy.pushButton.clicked.connect(UploadWindowPlanStudy.close)
# загрузка всех в отдельном потоке
def upload_all_study_plan_students():
    uiPlanStudy.upload_all.setEnabled(False)
    th = Thread(target=Upload_study_plan_students)
    th.start()
# все результаты с бд
def study_plan_students_all_result():
    global all_string_Plan_Study
    all_string_Plan_Study = list()
    connection = Connection_BD()
    cursor = connection.cursor()
    external_id_db = list()
    Plan_Study = cursor.execute(
        "select ind.IND_ID,wp.Upl_upl_id from  o_individual ind  join (select * from O_PERSONAL_CARD where status='Y') pc on ind.IND_ID=pc.ind_ind_id join  (select * from o_work_place where status='Y' and st_stat_code in ('01', '03') and tst_tst_id=1 )wp on wp.pcard_pcard_id=pc.pcard_id ")
    for row in Plan_Study:
        all_string_Plan_Study.append(row)
    Plan_Study.close()
    for sp in all_string_Plan_Study:
        external_id_db.append(str(sp[0]))
    uiPlanStudy.count_db.setText(str(len(all_string_Plan_Study)))
    uiPlanStudy.upload_all.setEnabled(True)
#загрузка всех
def Upload_study_plan_students():
    SepCursor = list()
    for row in all_string_Plan_Study:
        dictTemp = {"student": row[0], "study_plan": row[1]}
        SepCursor.append(dictTemp)
    # upload_kusochkami(SepCursor, uiPlanStudy, "https://tls.online.edu.ru/vam/api/v2/study_plans_students",
    #                   "study_plan_students", 4, all_string_Plan_Study)

    count_check = 0
    global count
    count = 0
    while len(SepCursor) != 0:
        count_check += len(SepCursor[0:500])
        while count != count_check and len(SepCursor) != 0:
            zapusk(SepCursor[0:500], uiPlanStudy, "https://tls.online.edu.ru/vam/api/v2/study_plans_students",
                      "study_plan_students", 0, all_string_Plan_Study)
            print("\n", len(SepCursor), "\n", count_check, count)
            print(len(SepCursor), len(all_string_Plan_Study))
        del SepCursor[0:500]
    study_plan_students_all_result()

# запускаем седьмую загрузку
# ----------------------------------------------------------------------------
ui.import_study_plan_students.clicked.connect(Upload_study_plan_students_window)
# ----------------------------------------------------------------------------

# окно восьмой загрузки
def Upload_marks():
    global UploadWindowMarks
    global uiMarks
    UploadWindowMarks = QtWidgets.QMainWindow()
    uiMarks = Ui_UploadWindow()
    uiMarks.setupUi(UploadWindowMarks)
    UploadWindowMarks.show()
    uiMarks.upload_choice.setEnabled(False)
    uiMarks.upload_all.setEnabled(False)
    uiMarks.count_site.setText("--")
    uiMarks.count_db.setText("Ищем...")
    uiMarks.count_choice.setText("--")
    th1 = Thread(target=marks_all_result)
    th1.start()
    uiMarks.upload_all.clicked.connect(upload_all_marks)
    uiMarks.pushButton.clicked.connect(UploadWindowMarks.close)
# загрузка всех в отдельном потоке
def upload_all_marks():
    uiMarks.upload_all.setEnabled(False)
    th = Thread(target=Upload_Marks)
    th.start()
# все результаты с бд
def marks_all_result():
    global all_string_Marks
    all_string_Marks = list()
    connection = Connection_BD()
    cursor = connection.cursor()
    external_id_db = list()
    Marks = cursor.execute(
        "select  stre.dis_code,ind.IND_ID,wp.Upl_upl_id,stre.name_edu_work,stre.mark mark, stre.period_num, stre.equival_mark from (select IND_ID from o_individual) ind join (select * from O_PERSONAL_CARD where status='Y' ) pc on ind.IND_ID=pc.ind_ind_id join (select * from o_work_place where status='Y' and st_stat_code in ('01', '03') and tst_tst_id=1 )wp on wp.pcard_pcard_id=pc.pcard_id join sdms.o_use_document ud on ud.pcard_pcard_id = pc.pcard_id join sdms.o_document doc on doc.doc_id = ud.doc_doc_id and doc.tdoc_tdoc_id = 34 join sdms.o_education edu on edu.doc_doc_id = doc.doc_id join (select * from sdms.u_str_educ where name_edu_work='Зачет' or name_edu_work='Экзамен' or name_edu_work='Дифференцированный зачет') stre on stre.edu_edu_id = edu.edu_id")
    for row in Marks:
        all_string_Marks.append(row)
    Marks.close()
    connection.close()

    for sp in all_string_Marks:
        external_id_db.append(str(sp[0]))
    uiMarks.count_db.setText(str(len(all_string_Marks)))
    uiMarks.upload_all.setEnabled(True)
#загрузка всех
def Upload_Marks():
    SepCursor = list()
    for row in all_string_Marks:
        Mark_type = ""
        Mark_value = 0
        if row[3] == "Зачет":
            Mark_type = "CREDIT"
            Mark_value = 1 if row[4] == "зачтено" else 0
        if row[3] == "Экзамен":
            Mark_type = "MARK"
            try:
                Mark_value = int(row[6])
            except TypeError:
                Mark_value = row[6]
        if row[3] == "Дифференцированный зачет":
            Mark_type = "DIF_CREDIT"
            try:
                Mark_value = int(row[6])
            except TypeError:
                Mark_value = row[6]

        dictTemp = {"discipline": row[0], "student": row[1], "study_plan": row[2], "mark_type": Mark_type,
                    "mark_value": Mark_value, "semester": row[5]}
        SepCursor.append(dictTemp)

    # del SepCursor[0:500000]
    # del all_string_Marks[0:500000]
    count_check = 0
    global count
    count = 0
    while len(SepCursor) != 0:
        count_check += len(SepCursor[0:500])
        while count != count_check and len(SepCursor) != 0:
            zapusk(SepCursor[0:500], uiMarks, "https://tls.online.edu.ru/vam/api/v2/marks", "marks", 0, all_string_Marks)
            print("\n", len(SepCursor), "\n", count_check, count)
        del SepCursor[0:500]

    marks_all_result()



# запускаем восьмую загрузку
# ----------------------------------------------------------------------------
ui.marks.clicked.connect(Upload_marks)
# ----------------------------------------------------------------------------
sys.exit(app.exec_())