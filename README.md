# DoctorsWithinBorders
Predicting location of primary care doctor shortages

I developed this project, Doctors Within Borders, during my first few weeks as a Insight Data Science fellow. My goal with this project is to identify the areas within the United States of America that currently have the greatest primary care shortages, with the hope that young physicians can use this information to decide where to setup a new practice and state administrators can quickly identify problem areas in their states.

For this project, I focused on The Bureau of Health Workforce process, which has a designation known as a Health Professional Shortage Area (HPSA) score. This score measures the degree of primary care shortage for individual areas, with reporting areas as small as single counties. However, the current process for scoring a region is done manually, resulting in a bottleneck for identifying the areas around the country where shortages exist. Currently, only about 12 percent of all US counties have an up-to-date score.

The basic steps for the project were to  
       1) identify and find relevant sources of data (US Census Bureau, CDC, Medicare)  
       2) clean and merge the datasets together on a common geographic region,  
       3) develop a predictive model that could accurately predict the value of the HPSA score in counties that currently have a score,  
       4) make an interactive dashboard to explore the predictions on a county-by-county basis (see my other repository, "countymap-app"             for more information about the dashboard).

By developing a predictive model for HPSA scores, the goal is that we can immediately identify areas of greatest need around the country, automatically update scores as regions change over time, and pinpoint specific, actionable aspects of healthcare in the local region that are causing an area to have greater than average primary care shortage.

