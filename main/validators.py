import re
import pandas as pd
from django.core.exceptions import ValidationError
import requests
data = pd.read_excel("C:/Users/johns/OneDrive/Documents/profanity.xlsx")['v']
def no_profanity(value):
    for i in data:
        if re.search(i, value.lower()):
            
            raise ValidationError('Username should not contain profanity.')
    
            
def makeup(value):
    non_alphanumeric = re.findall(r'\W+', value)
   
    if len(non_alphanumeric) != 0:
        raise ValidationError('Username should contain letters and digits only')
    
