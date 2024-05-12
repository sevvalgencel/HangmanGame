import random
import json
import os

kelimeler = ["vantilatör", "adaptör", "kalem", "fare", "telefon", "kulaklık", "pervane", "merdane", "kestane"]


def oyun_hazirlik():
    global secilen_kelime, gorunen_kelime, can
    import random
    secilen_kelime = random.choice(kelimeler)
    gorunen_kelime = ["-"] * len(secilen_kelime)
    can = 5


def harf_al():
    """Kullanıcıdan bir harf alır, alana kadar gerekirse hata verir, birisi quit yazarsa programı kapatır"""
    devam = True
    while devam:
        harf = input("Bir harf giriniz: ")
        if harf.lower() == "quit":
            print("oyun bitti...")
            exit()
        elif len(harf) == 1 and harf.isalpha() and harf not in gorunen_kelime:
            devam = False
        else:
            print("Hatalı Giriş")

    return harf.lower()


def oyun_dongusu():
    global gorunen_kelime, can
    while can > 0 and secilen_kelime != "".join(gorunen_kelime):
        print("kelime: " + "".join(gorunen_kelime))
        print("can   : <" + "❤" * can + " " * (5 - can) + ">")

        girilen_harf = harf_al()
        pozisyonlar = harf_kontrol(girilen_harf)
        if pozisyonlar:
            for p in pozisyonlar:
                gorunen_kelime[p] = girilen_harf
        else:
            can -= 1


def harf_kontrol(girilen_harf):

    poz = []
    for index, h in enumerate(secilen_kelime):
        if h == girilen_harf:
            poz.append(index)
    return poz


def skor_tablosunu_goster():
    veri = ayar_oku()
    print("|Skor\t\tKullanıcı|")
    print("|------------------------|")
    for skor, kullanici in veri["skorlar"]:
        print("|"+str(skor) +"\t\t"+ kullanici+" "*(9-len(kullanici))+"|")
    print("|------------------------|")


def skor_tablosunu_guncelle():
    veri = ayar_oku()
    veri["skorlar"].append((can, veri["son_kullanan"]))
    veri["skorlar"].sort(key=lambda skor_tuplei: skor_tuplei[0], reverse=True)
    veri["skorlar"] = veri["skorlar"][:5]
    ayar_yaz(veri)


def oyun_sonucu():
    """Oyun bittiğinde kazanıp kazanamadığımızı ekrana yazar."""
    if can > 0:
        print("Kazandınız!!")
        skor_tablosunu_guncelle()
    else:
        print("Kaybettiniz :(")
    skor_tablosunu_goster()


def dosyayi_kontrol_et_yoksa_olustur():
    yaz = False
    if os.path.exists("ayarlar.json"):
        try:
            ayar_oku()
        except ValueError as e:
            print("Hata: ValueError(" + ",".join(e.args))
            os.remove("ayarlar.json")
            yaz = True
    else:
        yaz = True

    if yaz:
        ayar_yaz({"skorlar": [], "son_kullanan": ""})


def ayar_oku():
    with open("ayarlar.json") as f:
        return json.load(f)


def ayar_yaz(veri):
    with open("ayarlar.json", "w") as f:
        json.dump(veri, f)


def kullanici_adini_guncelle():
    """Kullanıcıdan isim alıp ayarlara yazdırmaya gönderir"""
    veri = ayar_oku()
    veri["son_kullanan"] = input("Kullanıcı Adınız: ")
    while not veri["son_kullanan"] or len(veri["son_kullanan"]) > 9:
        veri["son_kullanan"] = input("lykpython ile 9 karakter uzunluğunda yazın: ")
    ayar_yaz(veri)


def kullanici_kontrol():
    veri = ayar_oku()
    print("Son giriş yapan: " + veri["son_kullanan"])
    if not veri["son_kullanan"]:
        kullanici_adini_guncelle()
    elif input("Bu siz misiniz?(e/h) ").lower() == "h":
        kullanici_adini_guncelle()


def main():
    again = True
    dosyayi_kontrol_et_yoksa_olustur()
    print("Merhaba, Adam Asmacaya hoşgeldiniz.")
    print("-"*30)
    skor_tablosunu_goster()
    kullanici_kontrol()
    while again:
        oyun_hazirlik()
        oyun_dongusu()
        oyun_sonucu()
        if input("Devam?(e/h) ").lower() == "h":
            again = False
    print("oyun bitti.")

main()