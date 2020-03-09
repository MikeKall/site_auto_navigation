from selenium.webdriver import Firefox
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
import time
import re
import os


def WriteToFileClean(browser):
    print ("Writing to files")
    with open("holder.txt","r") as f,open("totalCourses.txt","w+") as clean_total_courses_file:
        for line in f:
            result = re.sub(r'\([^)]*\)', '',line)
            clean_total_courses_file.write(result.lstrip()+"\n")

    os.remove("holder.txt")

    winter = True
    summer = False
    counter = 0
    winterCourses = ""
    summerCourses = ""
    with open("failedholder.txt", "r+") as f:
        for line in f:
            result = re.sub(r'\([^)]*\)', '',line)
            result = result.rstrip()
            if "ΑΓΓΛΙΚΑ" in result:
                continue
            if "Εξάμηνο" in result:
                if int(result[-1:])%2 == 0:
                    summer = True
                    winter = False
                else:
                    summer = False
                    winter = True
            if winter:
                winterCourses += result+"\n"
            else:
                summerCourses += result+"\n"
            counter += 1

    clean_failed_courses_file = open("failed.txt", "w+")
    clean_failed_courses_file.write("======== Χειμερινά εξάμηνα =========\n")
    clean_failed_courses_file.write(winterCourses)
    clean_failed_courses_file.write("====================================\n\n")
    clean_failed_courses_file.write("======== Θερινά εξάμηνα =========\n")
    clean_failed_courses_file.write(summerCourses)
    clean_failed_courses_file.write("====================================\n")
    clean_failed_courses_file.write("Σύνολο χρωστούμενων: "+str(counter))
    clean_failed_courses_file.close()
    os.remove("failedholder.txt")
    browser.quit()


def GetGrades(browser):
    print ("Getting your grades")
    counter = 0
    failedCounter = 0
    with open("holder.txt", "w+") as total_courses_file, open("failedholder.txt", "w+") as failed_courses_file:
        while True:
            counter += 1
            try:
                subject = browser.find_element_by_xpath("//form/table/tbody/tr/td/table/tbody/tr["+str(counter)+"]/td[2]")
                grade = browser.find_element_by_xpath("//form/table/tbody/tr/td/table/tbody/tr["+str(counter)+"]/td[7]")
                total_courses_file.write(subject.text + " " + grade.text + "\n")
                if (grade.text != "Βαθμός"):
                    try:
                        if int(grade.text) < 5:
                            failed_courses_file.write(subject.text + " " + grade.text + "\n")
                            failedCounter += 1
                    except ValueError as e:
                        failed_courses_file.write(subject.text + " " + grade.text + "\n")
                        failedCounter += 1
            except NoSuchElementException as e:
                try:
                    total_passed = browser.find_element_by_xpath("//form/table/tbody/tr/td/table/tbody/tr["+str(counter)+"]/td")
                    if "Εξάμηνο" in total_passed.text:
                        failed_courses_file.write(total_passed.text+"\n")
                        total_courses_file.write("========= " + total_passed.text + " =========" +"\n")
                    if "Σύνολα" in total_passed.text:
                        mo = browser.find_element_by_xpath("//form/table/tbody/tr/td/table/tbody/tr["+str(counter)+"]/td[2]")
                        total_courses_file.write(total_passed.text + "\n" + mo.text + "\n===============================================\n\n")
                except Exception as e:
                    break

    WriteToFileClean(browser)

def goToLink(browser):
    browser.get('https://students.unipi.gr/')
    print ("Navigating to the website")
    username = browser.find_element_by_id('userName')
    username.send_keys('p16040')
    print ("Pressing some buttons")
    password = browser.find_element_by_id('pwd')
    password.send_keys('mike_17021998MK')

    submit = browser.find_element_by_id('submit1')
    submit.click()

    menu = browser.find_element_by_id('mnu3')
    menu.click()
    GetGrades(browser)

if __name__ == "__main__":
    while True:
        options = Options()
        options.headless = True
        browser = Firefox(options=options)
        print ("Firefox Initialized")
        try:
            goToLink(browser)
            print ("Completed!")
            break
        except NoSuchElementException as e:
            print("The website is messed up, relaunching")
            browser.quit()
            continue
