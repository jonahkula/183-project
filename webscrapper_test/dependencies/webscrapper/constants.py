STATE = "California" # will be obtainable from modal
ZIPCODE = "95258" # the zipcode will be provided by the the modal extracted from the database
MAXWAIT = 60 # 60 seconds is the maximum time we wait for a page to load (Note: most computers load pages in the miliseconds)
DOB = "02111999" # the dob will be provided again by the user
AGE = 22 # modal will provide the age

KROGER_FIELDS = 7

eligibility_xpath = {
    "I Agree": "/html/body/div[1]/div/div[3]/div[1]/main/div/section[2]/div/div/div/div/div/div/div/div/ul/li/div/div[2]/div[2]/div/div/div/button[1]",
    "Threatening Yes": "/html/body/div[1]/div/div[3]/div[1]/main/div/section[2]/div/div/div/div/div/div/div/div/ul/li[3]/div/div[2]/div[2]/div/div/div/button[1]",
    "Threatening No": "/html/body/div[1]/div/div[3]/div[1]/main/div/section[2]/div/div/div/div/div/div/div/div/ul/li[3]/div/div[2]/div[2]/div/div/div/button[2]",
    "Select State": "/html/body/div[1]/div/div[3]/div[1]/main/div/section[2]/div/div/div/div/div/div/div/div/ul/li[5]/div/div[2]/div[2]/div/div/div/select",
    "DOB Field": "/html/body/div[1]/div/div[3]/div[1]/main/div/section[2]/div/div/div/div/div/div/div/div/ul/li[6]/div/div[2]/div[2]/div/div/div/div/form/div[1]/input",
    "DOB Submit": "/html/body/div[1]/div/div[3]/div[1]/main/div/section[2]/div/div/div/div/div/div/div/div/ul/li[6]/div/div[2]/div[2]/div/div/div/div/form/div[2]/button",
    "First Dose Yes": "/html/body/div[1]/div/div[3]/div[1]/main/div/section[2]/div/div/div/div/div/div/div/div/ul/li[7]/div/div[2]/div[2]/div/div/div/button[1]",
    "First Dose No": "/html/body/div[1]/div/div[3]/div[1]/main/div/section[2]/div/div/div/div/div/div/div/div/ul/li[7]/div/div[2]/div[2]/div/div/div/button[2]",
    "Received Vaccine Yes": "/html/body/div[1]/div/div[3]/div[1]/main/div/section[2]/div/div/div/div/div/div/div/div/ul/li[9]/div/div[2]/div[2]/div/div/div/button[1]",
    "Received Vaccine No": "/html/body/div[1]/div/div[3]/div[1]/main/div/section[2]/div/div/div/div/div/div/div/div/ul/li[9]/div/div[2]/div[2]/div/div/div/button[2]",
    "Schedule":"/html/body/div[1]/div/div[3]/div[1]/main/div/section[2]/div/div/div/div/div/div/div/div/ul/li[11]/div/div[2]/div[2]/div/div/div/button",
}

scheduling_xpath = {
    "Find Location": "/html/body/div[1]/div/div[3]/div[1]/main/div/section[2]/div/div/div[2]/div[3]/div[1]/div/div/div/div[2]/form/div/div[1]/div/input",
    "Location Submit": "/html/body/div[1]/div/div[3]/div[1]/main/div/section[2]/div/div/div[2]/div[3]/div[1]/div/div/div/div[2]/form/button",
}

states = {
    "Alabama":"AL", 
    "Alaska":"AK",
    "Arizona":"AZ",
    "Arkansas":"AR", 
    "California":"CA",
    "Colorado":"CO",
    "Connecticut":"CT",
    "Washington DC":"DC",
    "Deleware":"DE",
    "Florida":"FL",
    "Georgia":"GA",
    "Hawaii":"HI",
    "Idaho":"ID",
    "Illinios":"IL", 
    "Indiana":"IN",
    "Iowa":"IA",
    "Kansas":"KS",
    "Kentucky":"KY",
    "Louisiana":"LA",
    "Maine":"ME",
    "Maryland":"MD",
    "Massachusetts":"MA",
    "Michigan":"MI",
    "Minnesota":"MN",
    "Mississippi":"MS",
    "Missouri":"MO",
    "Montana":"MT",
    "Nebraska":"NE",
    "Nevada":"NV",
    "New Hampshire":"NH",
    "New Jersey":"NJ",
    "New Mexico":"NM",
    "New York":"NY",
    "North Carolina":"NC",
    "North Dakota":"ND",
    "Ohio":"OH",
    "Oklahoma":"OK",
    "Oregon":"OR",
    "Pennsylvania":"PA",
    "Rhode Island":"RI",
    "South Carolina":"SC",
    "South Dakota":"SD",
    "Tennessee":"TN",
    "Texas":"TX",
    "Utah":"UT",
    "Vermont":"VT",
    "Virgina":"VA",
    "Washington":"WA",
    "West Virginia":"WV",
    "Wisconsin":"WI",
    "Wyoming":"WY"
}
# /html/body/cvs-root/div/cvs-covid-questionnaire/main/div[3]/button
cvs_xpaths = {
    "Schedule": "/html/body/div[2]/div/div[24]/div/div/div/div/div/div[1]/div[2]/div/div/div[2]/div/div[3]/div/p[2]/a",
    "Tested Positive": "/html/body/cvs-root/div/cvs-covid-questionnaire/main/div[2]/div/cvs-questionnaire/form/fieldset/section/div[2]/fieldset/div[2]/div[2]",
    "Close Contact": "/html/body/cvs-root/div/cvs-covid-questionnaire/main/div[2]/div/cvs-questionnaire/form/fieldset/section/div[3]/fieldset/div[2]/div[2]",
    "Current Conditions": "/html/body/cvs-root/div/cvs-covid-questionnaire/main/div[2]/div/cvs-questionnaire/form/fieldset/section/div[4]/fieldset/div[2]/div[2]",
    "Continue": "/html/body/cvs-root/div/cvs-covid-questionnaire/main/div[3]/button",
    "Need Vaccination": "/html/body/cvs-root/div/cvs-covid-dose-selection/main/div[2]/form/section/div[2]/div/div/div[1]",
    "Second Dose": "/html/body/cvs-root/div/cvs-covid-dose-selection/main/div[2]/form/section/div[2]/div/div/div[2]",
    "Continue Scheduling(1)": "/html/body/cvs-root/div/cvs-covid-dose-selection/main/div[3]/button",
    "Select State": "/html/body/cvs-root/div/cvs-eligibility-covid/main/div[2]/form/section/div/div/select",
    "Continue Scheduling(2)": "/html/body/cvs-root/div/cvs-eligibility-covid/main/div[3]/button",
    "Age": "/html/body/cvs-root/div/cvs-eligibility-questionnaire/main/div[2]/form/fieldset/section/div[2]/div/input",
    "Acknowledgment":"/html/body/cvs-root/div/cvs-eligibility-questionnaire/main/div[2]/form/fieldset/section/div[3]/div",
    "Confirm Eligiblity": "/html/body/cvs-root/div/cvs-eligibility-questionnaire/main/div[3]/button",
    "Start Scheduling": "/html/body/cvs-root/div/cvs-cvd-how-to-schedule/main/div[3]/button",
    "Search Input": "/html/body/cvs-root/div/cvs-cvd-first-dose-select/main/div[2]/cvs-store-locator/div/section/form/div[1]/div/div[1]/input",
    "Search Button": "/html/body/cvs-root/div/cvs-cvd-first-dose-select/main/div[2]/cvs-store-locator/div/section/form/div/div/div[1]/button",
    "First Dose Date": "/html/body/cvs-root/div/cvs-cvd-first-dose-select/main/div[2]/cvs-store-locator/div/section/form/div[2]/div/select",
    
}

# don't need this, since they just send to the same link anyway's, could probably skip this part then
state_xpaths = {
    "Alabama": "/html/body/content/div/div/div/div[3]/div/div/div[2]/div/div[5]/div/div/div/div/div/div[1]/div[2]/div/div[2]/div/div/div/div/div[1]/ul/li[1]/div/a",
    "Alaska": "/html/body/content/div/div/div/div[3]/div/div/div[2]/div/div[5]/div/div/div/div/div/div[1]/div[2]/div/div[2]/div/div/div/div/div[1]/ul/li[2]/div/a",
}

# /html/body/cvs-root/div/cvs-cvd-first-dose-select/main/div[2]/cvs-store-locator/div/div/div[2]
# 

# /html/body/cvs-root/div/cvs-cvd-first-dose-select/main/div[2]/cvs-store-locator/div/div/div[2]
# /html/body/cvs-root/div/cvs-cvd-first-dose-select/main/div[2]/cvs-store-locator/div/div/div[3]
# /html/body/cvs-root/div/cvs-cvd-first-dose-select/main/div[2]/cvs-store-locator/div/div/div[4]