import pandas as pd
import requests
import os
df=pd.read_csv('poster.csv')

col1='title'
col2='image_url'


count=0
for name,url in zip(df[col1],df[col2]):
    print(f"Title: {name}\nImage URL: {url}\n")
    """
    save=f"{name}_poster.jpg"
    r=requests.get(url,stream=True)
    r.raise_for_status()
    with open(save,'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Downloaded and saved as {save}\n")
    """
    count+=1

print(f"Total posters processed: {count}")