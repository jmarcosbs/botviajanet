import requests

token = "6891057872:AAHEN4leh0JQxpmLiR0GN4YB38eHtaGkB2M"
chatId = "732421718"
url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chatId}&text=Funcionou"
send = requests.get(url)  #Send mensage in Telegram
                
print(send.json())

print("Comunicação Enviada.")