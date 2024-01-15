from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd

source_dir = Path('./html-tutorial_folder')
if not source_dir.exists():
    raise FileNotFoundError(f'{source_dir} is not found')

data_list = []
for html_file in source_dir.glob(f'*.html'):
     with open (html_file, 'r', encoding= 'utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        print(f' Processing file{html_file}')
       

        box = soup.find('div',{'aria-label': 'Timeline: Conversation'})
        all_divs = box.find_all('div', {'data-testid': 'cellInnerDiv'}) if soup.find('div',{'aria-label': 'Timeline: Conversation'}) else None
        
        
        for i,div_tag in enumerate(all_divs):
            # print(div_tag)
            try:
                # Extract Username, URL, and Comment from each div tag
                username = div_tag.find('span', class_=lambda x: x and 'r-bcqeeo' in x).get_text().strip() if div_tag.find('span', class_=lambda x: x and 'r-bcqeeo' in x) else None
                print(i,username)
                print("====== username =======")
            except AttributeError as e:
                # Handle the case where any of the elements are not found
                print(f"Error extracting data: {e}")
            try:
                
                url = div_tag.find('a', {'role':'link'})['href'].strip().split('/')[1] if div_tag.find('a', {'role':'link'}) else None
                # url = div_tag.find('a', class_='css-175oi2r r-1wbh5a2 r-dnmrzs r-1ny4l3l r-1loqt21')['href'].strip().split('/')[1] if div_tag.find('a', {'tabindex':'-1'}) else None
                if url is None:
                    user_url = None
                    print(i,user_url)
                else:
                    user_url = f"https://twitter.com/{url}"
                    print(i,user_url)
                
                print("====== url =======")
            except AttributeError as e:
                # Handle the case where any of the elements are not found
                print(f"Error extracting data: {e}")
            try:
                comment = div_tag.find('div',{'dir': 'auto'}).text.strip() if div_tag.find('div',{'dir': 'auto'}) else None
                print(i,comment)
                print("====== comment =======")
            except AttributeError as e:
                # Handle the case where any of the elements are not found
                print(f"Error extracting data: {e}")
                # Append the data to the list
            data_list.append([username, user_url, comment])

  

# Create a DataFrame from the data list
df = pd.DataFrame(data_list, columns=['Username', 'User URL', 'Comment'])
print(df)

# Write the DataFrame to an Excel file
df.to_excel('again1.xlsx', index=False)

print("Extraction and writing to Excel completed.")
