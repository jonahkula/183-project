STATE = "California" # will be obtainable from modal
ZIPCODE = "95258" # the zipcode will be provided by the the modal extracted from the database
DOB = "02111999" # the dob will be provided again by the user
AGE = 22 # modal will provide the age
FIRST_NAME = "Olof"
LAST_NAME = "Omelc"
ADDRESS = "2319 George St."
CITY = "San Jose"
PHONE_NUMBER = "818 571 9120"
# everything above be provided by the user

IMPLICIT_WAIT = 20
KROGER_FIELDS = 7
INDEX_CAP = 100
MAXWAIT = 30 # 30 seconds is the maximum time we wait for a page to load (Note: most computers load pages in the miliseconds)

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

cvs_xpaths = {
    "State": "//*[@id='selectstate']",
    "Get Started": "/html/body/content/div/div/div/div[4]/div/div[2]/form/div[2]/button",
    "Schedule": "//*[@id='vaccineinfo-CA']/div/div/div/div[1]/div[2]/div/div/div[2]/div/div[3]/div/p[2]/a", # NOTICE: this only applies to CA, no other state
    "Tested Positive": "//*[@id='questionnaire']/section/ol/li[1]/fieldset/div/div[2]",
    "Close Contact": "//*[@id='questionnaire']/section/ol/li[2]/fieldset/div/div[2]",
    "Current Conditions": "//*[@id='questionnaire']/section/ol/li[3]/fieldset/div/div[2]",
    "Continue": "/html/body/cvs-root/div/cvs-covid-questionnaire/main/div[3]/button",
    "Need Vaccination": "//*[@id='generic']/section/div[2]/div/fieldset/div/div[1]",
    "Second Dose": "/html/body/cvs-root/div/cvs-covid-dose-selection/main/div[2]/form/section/div[2]/div/div/div[2]",
    "Continue Scheduling(1)": "/html/body/cvs-root/div/cvs-covid-dose-selection/main/div[3]/button",
    "Select State": "/html/body/cvs-root/div/cvs-eligibility-covid/main/div[2]/form/section/div/div/select",
    "Continue Scheduling(2)": "/html/body/cvs-root/div/cvs-eligibility-covid/main/div[3]/button",
    "Age": "//*[@id='q1_0']",
    "Acknowledgment":"//*[@id='generic']/section/div[3]/div",
    "Confirm Eligiblity": "/html/body/cvs-root/div/cvs-eligibility-questionnaire/main/div[3]/button",
    "Start Scheduling": "/html/body/cvs-root/div/cvs-cvd-how-to-schedule/main/div[3]/button",
    "Search Input": "/html/body/cvs-root/div/cvs-cvd-first-dose-select/main/div[2]/cvs-store-locator/div/section/form/div[1]/div/div[1]/input",
    "Search Button": "/html/body/cvs-root/div/cvs-cvd-first-dose-select/main/div[2]/cvs-store-locator/div/section/form/div/div/div[1]/button",
    "First Dose Date": "/html/body/cvs-root/div/cvs-cvd-first-dose-select/main/div[2]/cvs-store-locator/div/section/form/div[2]/div/select",
    "Current Locations": "//*[@id='content']/div[2]/cvs-store-locator/div/div/div[1]",
    "Continue Scheduling(3)": "//*[@id='content']/div[3]/button",
    "Second Dose Date": "//*[@id='availableDate']",
    "Continue Scheduling(4)": "//*[@id='content']/div[3]/button",
    "Second Dose Location": "//*[@id='content']/div[2]/cvs-store-locator/div/div",
    "First Name": "//*[@id='firstName']",
    "Last Name": "//*[@id='lastName']",
    "DOB": "//*[@id='dob']",
    "Female": "//*[@id='generic']/section/div[5]/fieldset/div/div[1]/label",
    "Male": "//*[@id='generic']/section/div[5]/fieldset/div/div[2]/label",
    "Address": "//*[@id='address']",
    "City": "//*[@id='city']",
    "State (Again)": "//*[@id='state']",
    "Zipcode": "//*[@id='zip']",
    "Number": "//*[@id='phoneNumber']",
    "Continue Scheduling(5)": "//*[@id='content']/div[3]/button",
    "Coverage": "//*[@id='generic']/section/div/div/fieldset/div/div[3]",
    "Continue Scheduling(6)": "//*[@id='content']/div[3]/button",
    "No Insurance": "//*[@id='generic']/div[2]/div",
    "No Allergies":"//*[@id='questionnaire']/section/ol/li[1]/fieldset/div/div[2]",
    "Covid Reaction":"//*[@id='questionnaire']/section/ol/li[2]/fieldset/div/div[2]",
    "Allergy After": "//*[@id='questionnaire']/section/ol/li[3]/fieldset/div/div[2]",
    "Polyethylene Glycol":"//*[@id='questionnaire']/section/ol/li[4]/fieldset/div/div[2]",
    "Polysorbate":"//*[@id='questionnaire']/section/ol/li[5]/fieldset/div/div[2]",
    "Pregnant":"//*[@id='questionnaire']/section/ol/li[6]/fieldset/div/div[2]",
    "Blood Disorder":"//*[@id='questionnaire']/section/ol/li[7]/fieldset/div/div[2]",
    "Received Vaccine":"//*[@id='questionnaire']/section/ol/li[8]/fieldset/div/div[2]",
    "Treatment":"//*[@id='questionnaire']/section/ol/li[9]/fieldset/div/div[2]",
    "Continue Scheduling(7)": "//*[@id='content']/div[3]/button",
    "Race-White":"//*[@id='questionnaire']/section/ol/li[1]/fieldset/div/div[5]",
    "Race-Islander":"//*[@id='questionnaire']/section/ol/li[1]/fieldset/div/div[4]", # 1 - 6 for div values, don't include other races, since we can iterate on them
    "Ethnicity":"//*[@id='questionnaire']/section/ol/li[2]/fieldset/div/div[1]", # 1 - 3 for div values to loop for ethnicity
    "Immunization":"//*[@id='questionnaire']/section/ol/li[3]/fieldset/div/div[2]",
    "Continue Scheduling(8)":"//*[@id='content']/div[3]/button",
    "Consent": "//*[@id='generic']/section/fieldset/div[5]/div",
    "I Consent":"//*[@id='content']/div[3]/button", # I believe this is the ending button, so careful not to click it yet
}

riteaid_paths = {
    "DOB": "//*[@id='dateOfBirth']",
    "City": "//*[@id='city']",
    "State":"//*[@id='eligibility_state']",
    "Zipcode": "//*[@id='zip']",
    "Occupation": "//*[@id='Occupation']",
    "None of the Above(1)": "//*[@id='eligibility']/div/div[2]/div/div[1]/div/div/ul/li[38]",
    "Medical Conditions": "//*[@id='mediconditions']",
    "None of the Above(2)":"//*[@id='eligibility']/div/div[2]/div/div[2]/div/div/div/ul/li[29]",
    "Next":"//*[@id='continue']",
    "Continue":"//*[@id='learnmorebttn']",
}

# //*[@id="content"]/div[2]/cvs-store-locator/div/div/div[5]
# //*[@id="content"]/div[2]/cvs-store-locator/div/div/div[8]
# //*[@id="content"]/div[2]/cvs-store-locator/div/div/div[11]