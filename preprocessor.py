import re
import pandas as pd
from datetime import datetime

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s\w+\s-\s'
    message = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    pattern = re.compile(r'(\d{2}/\d{2}/\d{4}), (\d{1,2}:\d{2}\u202f[ap]m)')

    # Extracting the matches
    matches = [pattern.search(line) for line in dates]
    dates_times = [(match.group(1), match.group(2)) for match in matches if match]

    # Create a DataFrame
    df = pd.DataFrame(dates_times, columns=['Date', 'Time'])
    
    
    date=[]
    times=[]
    for i in dates:
        date.append(i.split(", ")[0])
        times.append(i.split(", ")[1])
    time=[]
    for i in times:
        time.append(i.split("-")[0])
    df=pd.DataFrame({
        'user_message':message,
        'date':date,
        'time':time
    })
    
    users = []
    messages = []

    for msg in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', msg)
        if entry[1:]:
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0].strip())
    
    df['user'] = users
    df['user_message'] = messages
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
    
    
    
    from datetime import datetime
    # Conversion function with error handling
    def convert_to_24hr(time_str):
        try:
            # Remove narrow no-break space and strip any extra spaces
            time_str_cleaned = time_str.replace('\u202f', '').strip()
            # Convert to 24-hour format
            return datetime.strptime(time_str_cleaned, '%I:%M%p').strftime('%H:%M')
        except ValueError:
            return 'Invalid Format'

    # Applying the conversion
    df['Time_24hr'] = df['time'].apply(convert_to_24hr)

    
    
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num']=df['date'].dt.month
    df['only_date']=df['date'].dt.date
    df['day_name']=df['date'].dt.day_name()
    
    
    
    df['hour'] = pd.to_datetime(df['Time_24hr'], format='%H:%M').dt.hour
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    
    
    return df
