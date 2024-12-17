import http.client
import json

base_currency = input("Lütfen Bir Döviz Cinsi Girin (Örneğin: TRY, USD, EUR ): ").upper()
to_currency = input("Hangi Döviz cinsine çevirmek istediğinizi girin : ").upper()
price = input("Çevirmek istediğiniz tutarı girin : ")
int(price)


conn = http.client.HTTPSConnection("api.collectapi.com")

headers = {
    'content-type': "application/json",
    'authorization': "apikey 2DFqPaEe8S8ErYiyZWeJQR:0vaGfQezUYwP881DIhshlq"
    }

endpoint = f"/economy/exchange?int={price}&to={to_currency}&base={base_currency}"
conn.request("GET", endpoint, headers=headers)

res = conn.getresponse()
data = res.read()

data = json.loads(data.decode("utf-8"))

formatted_json = json.dumps(data, indent=2, ensure_ascii=False)

print(formatted_json)