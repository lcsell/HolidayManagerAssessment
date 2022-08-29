from datetime import datetime
import json
from bs4 import BeautifulSoup
import requests
from config import dt2022
from config import weather


#menu for holiday tracker
def mainMenu():
    print('=========================')
    print('1. Add a Holiday')
    print('2. Remove a Holiday')
    print('3. View Holidays by Week')
    print('4. Save Changes')
    print('5. Exit')


#for scraping dateandtime.com
def scrapeHolidays():
    response = requests.get(dt2022)
    response = response.text
    soup2022 = BeautifulSoup(response,'html.parser')
    #find a table of all holidays
    td2022 =  soup2022.find('table', {'id': 'holidays-table'})
    #find the row for each holiday
    tableRows2022 = td2022.find('tbody').find_all('tr')

    return tableRows2022


#range of holidays on the website
def holidayCompiler(ResultSet, Hlist):
    setLength = len(ResultSet)
    for i in range(1, setLength):
        entry = ResultSet[i].find('a')
        if entry is not None:
            entry = entry.text
            Hlist.append(entry)
        else:
            pass
    return Hlist

#return corresponding holiday dates from website
def dateCompiler(ResultSet, Dlist, yearstring):
    setLength = len(ResultSet)
    for i in range(1, setLength):
        entry = ResultSet[i].find('th')
        if entry is not None:
            entry = entry.text + yearstring
            entry2 = datetime.strptime(entry,'%b %d, %Y')
            #entry3 = datetime.date(entry2)
            entry4 = datetime.strftime(entry2, '%Y-%m-%d')
            Dlist.append(entry4)
        else:
            pass
    return Dlist

#remove duplicates from holiday lists
def DeDuplicator(HlistIn, HlistOut):

    [HlistOut.append(i) for i in HlistIn if i not in HlistOut]

    return HlistOut

#clean original list
def initialListCleaner(list, string):
    for i in list:
        if i == string:
            list.remove(string)
        else:
            pass
    return list


class Holiday():

    def __init__(self, name, date):

        self.__name = name
        self.__date = datetime.strptime(date,'%Y-%m-%d')

    def __str__(self):
        printdate = self.__date.strftime('%Y-%m-%d')
        return f'{self.__name} ({printdate})'
    
    def makeHoliday(finalHolidayList):
        for i in finalHolidayList:
            Holiday(i[0], i[1])
        return finalHolidayList
    


class HolidayList(Holiday):
    def __init__(self):
        self.innerHolidays = []

    def showList(HolidayList):
        for i in HolidayList:
            holiday = Holiday(i[0], i[1])
            print(holiday)

    def addLists(self, list):
        for i in list:
                self.innerHolidays.append(i)
        else:
            pass
        return self.innerHolidays

    def findHoliday(self, HolidayName, datetime):

        found = False

        for i in self.innerHolidays:
            if i[0] == HolidayName:
                if datetime == i[1]:
                    print(i[0], i[1])
                    found = True
                else:
                    pass 
            else:
                pass
        if found == False:

            print('Not found')

    def numHolidays(self):
        return len(self.innerHolidays)

    def addHoliday(self, newHol):
        if newHol not in self.innerHolidays:
            nhList = [newHol]
            holObj = Holiday.makeHoliday(nhList)
            self.innerHolidays.append(newHol)
            print(f'The holiday was added successfully')
        else:
            print('Already in the holiday list') 
        return holObj

    def removeHoliday(self, remHol):
        
        if remHol in self.innerHolidays:
            self.innerHolidays.remove(remHol)
            print(f'The holiday was removed successfully')
            
        else:
            print('Not in the holiday list') 
        

    def read_to_json(self):
        #read in starter holidays
        with open ('holidays.json', 'r') as holidayStarter:
            hsData = json.load(holidayStarter)
            return hsData

    def save_to_json(self):
        with open('UpdatedHolidayList.json', 'w') as savefile:
            
            json.dump(self.innerHolidays, savefile)


    
    def filter_holidays_by_week(self, year, week_number):
        #yearlist = []
        dtlist = []

        for i in self.innerHolidays:
            if year in str(i[1]):
                dt = datetime.strptime(i[1],'%Y-%m-%d')
                wd = dt.isocalendar()[1]
                #yearlist.append(i)
                #dtlist = list(filter(lambda x: x == week_number, yearlist))
                if wd == week_number:
                     dtlist.append(i)
                else:
                    pass
            else:
                pass
        HolidayList.displayHolidaysInWeek(dtlist)
        return dtlist

    def displayHolidaysInWeek(HolidayList):
        for i in HolidayList:
            holiday = Holiday(i[0], i[1])
            print(holiday)


    #gets weather for current week
    def getWeather(self, NowYear, NowWeek):
        response = requests.get(weather)
        response = response.text
        rd = json.loads(response)
        rd2 = (rd['days'])
        weatherlist = []
        datelist = []
        for i in range(len(rd2)):
            date = (rd2[i]['datetime'])
            date2 = datetime.strptime(date, '%Y-%m-%d')
            if date2.isocalendar()[1] == NowWeek:
                datelist.append(date)
            else:
                pass
            conditions = (rd2[i]['conditions'])
            weatherlist.append(conditions)
        self.filter_holidays_by_week(str(NowYear), NowWeek)
        WDList = [list (i) for i in (zip(datelist, weatherlist))]
        print(f"This week's weather for the West Tennessee area is as follows: {WDList}")
       


    def viewCurrentWeek(self):
        now = datetime.now()
        nowYear = now.isocalendar()[0]
        nowWeek = now.isocalendar()[1]

        wc = False
        while wc == False:
            weatherchoice = input('Would you like to get the weather? y/n')
            if weatherchoice == 'y':
                self.getWeather(nowYear, nowWeek)
                wc = True
            elif weatherchoice == 'n':
                print('No weather')
                self.filter_holidays_by_week(str(nowYear), nowWeek)
                wc = True
            else:
                print('Please enter a correct choice.')
        return nowYear, nowWeek


def main():
    FullList = HolidayList()
    hsData = FullList.read_to_json()
    Observance = []
    Date2022 = []
    Date2020 = []
    Date2021 = []
    Date2023 = []
    Date2024 = []

    tableRows2022 = scrapeHolidays()

    holidayCompiler(tableRows2022, Observance)
    dateCompiler(tableRows2022, Date2022, ", 2022")
    dateCompiler(tableRows2022, Date2020, ", 2020")
    dateCompiler(tableRows2022, Date2021, ", 2021")
    dateCompiler(tableRows2022, Date2023, ", 2023")
    dateCompiler(tableRows2022, Date2024, ", 2024")

    Hol22 = [list (i) for i in (zip(Observance, Date2022))]
    Hol20 = [list (i) for i in (zip(Observance, Date2020))]
    Hol21 = [list (i) for i in (zip(Observance, Date2021))]
    Hol23 = [list (i) for i in (zip(Observance, Date2023))]
    Hol24 = [list (i) for i in (zip(Observance, Date2024))]


    H22 = []
    H20 = []
    H21 = []
    H23 = []
    H24 = []

    #remove duplicate holidays
    DeDuplicator(Hol22,H22)
    DeDuplicator(Hol20,H20)
    DeDuplicator(Hol21,H21)
    DeDuplicator(Hol23,H22)
    DeDuplicator(Hol24,H24)

    #put the initial holiday list into a workable list
    initialList = hsData.values()

    secondList = str(initialList).split("'")

    initialListCleaner(secondList, ': ')
    initialListCleaner(secondList, 'name')
    initialListCleaner(secondList, 'date')
    initialListCleaner(secondList, ', ')
    initialListCleaner(secondList, '[[{')
    initialListCleaner(secondList, '}, {')
    initialListCleaner(secondList, 'dict_values([[{')
    initialListCleaner(secondList, '}]])')

    InitialHol2021 = [secondList[i: i+2] for i in range(0, len(secondList), 2)]
    #make list into list of Holiday objects:
    H20Obj = Holiday.makeHoliday(H20)
    H21Initial = Holiday.makeHoliday(InitialHol2021)
    H21Obj = Holiday.makeHoliday(H21)
    H22Obj = Holiday.makeHoliday(H22)
    H23Obj = Holiday.makeHoliday(H23)
    H24Obj = Holiday.makeHoliday(H24)
    
    
    FullList.addLists(H20Obj)
    FullList.addLists(H21Obj)
    FullList.addLists(H21Initial)
    FullList.addLists(H22Obj)
    FullList.addLists(H23Obj)
    FullList.addLists(H24Obj)

    print('Welcome to the Holiday Tracker!')
    initialLength = FullList.numHolidays()
    print(f'Number of built-in holidays:{initialLength}')

    wantExit = False
    while wantExit == False:
        mainMenu()

        is_valid = False
        
        while not is_valid:
            userChoice = int(input('Enter the number of the choice you want: '))
            if userChoice > 5:
                print('Try 1-5')
            elif userChoice < 1:
                print('Try 1-5')
            else:
                is_valid = True

                if userChoice == 1:
                    print('Adding a New Holiay')
                    print('===================')
                    addchoice = input('Would you like to add a holiday? y for yes or any key for no ')
                    if addchoice == 'y':
                        hadd = input('Select a holiday name to add: ')
                        
                        while(True):
                            dadd = (input('Select the corresponding date in yyyy-mm-dd format: ')).strip()
                            try:
                                datetime.strptime(dadd, '%Y-%m-%d')
                                break
                            except:
                                print("That is an invalid date. It should be YYYY-MM-DD")

                        dadd2 = datetime.strptime(dadd, '%Y-%m-%d')
                        dadd3 = datetime.strftime(dadd2,'%Y-%m-%d')

                        #attach new holiday values to list
                        nh1 = []
                        nh1.append(hadd)
                        nh1.append(dadd3)

                        #make new holiday into list of lists
                        nh1 = [nh1[i: i+2] for i in range(0, len(nh1), 1)]
                        #unneeded list containing date exists at index[0]
                        newHoliday = nh1.pop(0)

                        FullList.addHoliday(newHoliday)
                    
                    else:
                        print('Addition canceled.')


                elif userChoice == 2:
                    print('Deleting a Holiay')
                    print('===================')
                    delchoice = input('Would you like to remove a holiday? y for yes or any key for no ')
                    if delchoice == 'y':
                        hdel = input('Select a holiday name to delete: ')
                        ddel = input('Select the corresponding date in yyyy-mm-dd format: ')
                        ddel2 = datetime.strptime(ddel,'%Y-%m-%d')
                        ddel3 = datetime.strftime(ddel2,'%Y-%m-%d')

                        #attach holiday to delete values to new list
                        dh1 = []
                        dh1.append(hdel)
                        dh1.append(ddel3)
                    
                        #make holiday to delete into list of lists
                        dh1 = [dh1[i: i+2] for i in range(0, len(dh1), 1)]
                    
                        #unneeded list containing date exists at index[0]
                        delHoliday = dh1.pop(0)

                        FullList.removeHoliday(delHoliday)
                    else:
                            print('Deletion canceled')
                            

                elif userChoice == 3:
                    print('Viewing Holiday List')
                    print('=====================')
                    goodyear = False
                    goodweek = False
                    
                    while goodyear == False:
                        hyear = int(input('Enter year (2020-2024): '))
                        if hyear < 2020:
                                print('That year is out of range.')
                        elif hyear > 2024:
                            print('That year is out of range')
                        else:
                            goodyear = True

                    while goodweek == False:
                        hweek = input('Which week? (1-52) Enter nothing for the current week (current year only): ')
                        currentyear = datetime.now().isocalendar()[0]
                        if hweek =='':
                            if hyear == currentyear:
                                hweek = FullList.viewCurrentWeek()
                                goodweek = True
                            else:
                                print('The year needs to be 2022')
                                goodweek = False
                        elif int(hweek) not in range (0,53):
                            print('Try again')
                            goodweek = False
                        else:
                            FullList.filter_holidays_by_week(str(hyear), int(hweek))
                            goodweek= True
                            

                elif userChoice == 4:
                    print('Saving Holiday List')
                    print('====================')
                    sc = False
                    while sc == False:
                        savechoice = input('Are you sure you want to save your changes? y/n ')
                        if savechoice == 'y':
                            FullList.save_to_json()
                            print('Your changes have been saved to UpdatedHolidayList.json.')
                            sc = True
                        elif savechoice == 'n':
                            print('Cancelled: \n Your changes were not saved.')
                            sc = True
                        else:
                            sc = False
                else:
                    print('Exiting the Holiday Manager')
                    print('=========================')
                    ec = False
                    while ec == False:
                        if initialLength < FullList.numHolidays():
                            exitchoice = input('''Are you sure you want to exit?' \n
                                Your changes will be lost. \n
                                [y/n]''')
                            if exitchoice == 'y':
                                print('Goodbye!')
                                ec = True
                                wantExit = True
                            elif exitchoice =='n':
                                print('Return to the main menu')
                                ec = True
                            else:
                                ec = False
                        else:
                            exitchoice = input('''Are you sure you want to exit?' \n
                                    [y/n]''')
                            if exitchoice == 'y':
                                print('Goodbye!')
                                ec = True
                                wantExit = True
                            elif exitchoice =='n':
                                print('Return to the main menu')
                                ec = True
                            else:
                                ec = False
                            

if __name__ == "__main__":
    main();