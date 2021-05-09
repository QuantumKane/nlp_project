
# **Natural Language Processing Project**

# **Planning the project**
## Goals
The goal of this project is to try to predict the programming language used in a repo based solely on the content of the readme fiie attatched to that repo

>Deliverables will include:
> - This repo containing: 
>   - A well-documented Jupyter Notebook detailing the process to create a predictive model
>   - This Readme.md detailing project planning and exection
>   - Final model created to predict programming language
> - A full slideshow containing well-labelled visualizations
 
>Where did the data come from?
> - The data was acquired from over 400 github repositories that focused on technology
> - The resulting dataset can be accessed via 'repos.csv', located within this repository

## Data Dictionary

The variables are the following:

| Feature           | Description                                     | Data Type 
|-------------------|-------------------------------------------------|------------
| repo              | The name of the github repository               | Object    
| language          | The programming language used in the repo       | Object     
| read_me contents  | The text that makes up the README file          | Object  


# **Project Steps**

##Acquire: 
- I got the data using Zach Gulde's acquire.py 
- I converted it to a dataframe
- I then wrote it to a csv for ease-of-use
- Lastly, I converted the csv back to a dataframe to begin the prep process

##Prep: 
### After prepping my data, I dropped from an initial 407 observatins to 293 observations
- I dropped 'Unnamed: 0' as it was redundant
- I dropped my null values: 70 in 'language" and 4 in 'readme_contents'
- I dropped any language that had less than 5 occurances

##Explore: compare/contrast the languages





Modeling: establish baseline, use classification models to predict the language