# importing pandas as pd 
import pandas as pd 
   
# Creating row index values for our data frame 
# We have taken time frequency to be of 12 hours interval 
# We are generating five index value using "period = 5" parameter 
   
ind = pd.date_range('01 / 01 / 2000', periods = 5, freq ='12H') 
   
# Creating a dataframe with 4 columns 
# using "ind" as the index for our dataframe 
df = pd.DataFrame({"A":[1, 2, 3, 4, 5],  
                   "B":[10, 20, 30, 40, 50], 
                   "C":[11, 22, 33, 44, 55], 
                   "D":[12, 24, 51, 36, 2]},  
                    index = ind) 
  
# Print the dataframe 
print(df)
df = df.shift()
print(df)