import pandas as pd
from pandas_profiling import ProfileReport

df = pd.read_csv('comments.csv')
profile = ProfileReport(df, title="Instagram Data Analysis")
profile.to_file("comments.html")




