# General Instructions

## Running the application
To run the application make sure that you add it to the `apps` folder contained in your `Py4Web` folder structure.

# History of our Project

## Why our group chose this project idea?
The group looked over the project ideas page on the Canvas page and one of the suggestions was the vaccine finder website. It was decided that making a website where information about various vaccine locations could be consolidated. The issue that our group saw with many vaccine websites is that you have to go to a specific pharmaceutical site in-order to find possible times, locations, and dates. This issue could become quite a nuisance having to go through multiple sites just to find a time and place that fit the user's schedule. 

## Why did we specifically choose a vaccine finder website?
As intriguing as other ideas were at first, making a vaccine website could have some pratical use in the real world as it was difficult for some to find a vaccine. Oleksiy also originally had the idea of web scrapping websites to provide users with the information of all major pharmaceutical companies in the U.S. When the information would've been webscrapped and displayed to the users, users could enter their health information and our application would autofilled the application for them. However, we soon learned that there are security vulnerabilities in doing this, and we had to go through 30+ pages just to webscrape & automate which reduced speeds greatly. 

# Workload Balance

## The beginning (Bulma & Basics of Py4Web)
We began by mapping out the design of the login, signup, and forgot password pages. Carlos was responsible for using Figma to draw out most of the designs for the application. Oleksiy began by writing the CSS and HTML code necessary for the login & forgot password page to look minimilistic and sleek. As Oleksiy was writing his HTML code, he incorporated aspects of Bulma's syntax. Later on SASS files were used to clean the login, signup, and forgot password pages as well. Jonah was responsible for making the navbar functioning and pretty on all pages. At this time in development, Jonah also began prototyping a favicon logo for the website. Jonah would later work on coding up the signup page also using Bulma, CSS, and HTML. Wayland began designing the layout of the content page where the vaccine locations are found now. Most of the group began working on their respective pages when Carlos finished designing the pages in Figma, so that everyone didn't have to worry about how the pages should look, but rather writing the code to mimic the design of Carlos's work. 

## The midpoint (Selenium (discontinued) & Py4Web) 
As some of the first pages started coming together, the group began shifting their focus to the content page and connecting the backend to the frontend on the webpages that were already written in Bulma. This was around the time that Oleksiy began researching ways in which information could be webscrapped from a dynamic webpage. Oleksiy came across [Selenium](https://selenium-python.readthedocs.io/) which made it quite easy to web scrape that information. Selenium also helped to automate the process of clicking buttons, entering user inputted information, etc. However, as a result of using Selenium on websites, such as [VaccineFinder](https://www.vaccines.gov/search/) his bot eventually got caught by the botnet used by the website. So he ended up using [Selenium-Stealth](https://github.com/diprajpatra/selenium-stealth) which helped avoid those botnets. Now back to the content page, Wayland continued designing the webpage and as currently Oleksiy didn't have any dynamic information and Vue.js wasn't taught yet, the page was made static with a couple boxes dedicated to imaginery pharmaceutical companies. Jonah was doing some restructuring currently of the login, signup, and forgot password pages since when getting the backend of Py4Web to the front-end (currently just Bulma) connected, we were quite limited in the appearance and functionality of various buttons. For example, we didn't have much choice in deciding the layout of the buttons on the signup, login, and forgot password pages. Also, in the case of the forgot password page, when the user clicked on the forgot password button, users would have to go manually click on a link to send themselves the forgot password link. Carlos around this time was finishing up his design of the various webpages and began creating a static reviews page. Carlos and Jonah worked on deciding what kind of database tables would exist and what information would need to be stored in them. Information regarding a users saved locations, reviews, and threads were the tables decided upon at the time. 