#Holiday Manager Assessment pseudocode outline
#Note: some plans changed in course of work

#import needed libraries

#create Holiday Class

#Draw out the initial holiday list json (holidays.json)

#store each as a Holiday object

#scrape dateandtime site for the dates of these holidays for 2020, 2022, 2023, and 2024 and store them as holidays objects
#(special 2021 dates are in the holidays.json)

#Create HolidayList class

#store initial hoildays as a holidayList object

#this will be where new holidays are added

#create holidayList methods for:
    #adding a holiday
    #removing a holiday
    #saving changes to the holiday list
        #writing to a json file
    #viewing the holiday list (one week at a time)
        #use a lambda to display the week required
        #enter nothing for the current week.
        #if current week selected, offer to read in weather from weather API
    #exiting the holiday manager

#create a menu for user to choose options corresponding to the holidayList methods listed above

#make sure these methods check for proper imputs (i.e., proper dates, correct spelling)
