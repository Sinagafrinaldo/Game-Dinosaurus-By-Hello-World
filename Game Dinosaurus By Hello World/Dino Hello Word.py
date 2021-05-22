import os
import sys
import pygame
import random
from pygame import *
pygame.init()
huruf= pygame.font.Font(None,48)
merah = (255, 0, 0)
hijau = (0, 255, 0)
lebar_layar = 700
tinggi_layar = 300
ukuran_layar = (width,height) = (700,300)
FPS = 60
gravitasi = 0.6
simpan = 0
hitam = (0,0,0)
putih = (255,255,255)
warna_latar = (25,190,225)
bisa = False
skor_tinggi = 0
jumlah_mati = 0
cekk=0
bonus = 0
perubahan_kecepatan = 0
pip =4
layar = pygame.display.set_mode(ukuran_layar)
clock = pygame.time.Clock()
pygame.display.set_caption("Dino Run by Hello World")

#Variabel untuk mengakses suara permainan
suara_lompat = pygame.mixer.Sound("images/jump.wav")
suara_mati = pygame.mixer.Sound('images/die.wav')
suara_cekpoin = pygame.mixer.Sound('images/checkPoint.wav')
# Fungsi untuk memuat gambar yang terdapat dalam folder images
def muat_gambar(
    name,
    posisi_x=-1,
    posisi_y=-1,
    colorkey=None,
    ):
    fullname = os.path.join('images', name)
    image = pygame.image.load(fullname)
    image = image.convert()
    if colorkey != None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    if posisi_x != -1 or posisi_y != -1:
        image = pygame.transform.scale(image, (posisi_x, posisi_y))

    return (image, image.get_rect())

# fungsi memuat setiap gambar objek yang terdapat dalam folder images
def muat_gambar_objek(
        sheetname,
        nx,
        ny,
        scalex = -1,
        scaley = -1,
        colorkey = None,
        ):
    fullname = os.path.join('images',sheetname)
    sheet = pygame.image.load(fullname)
    sheet = sheet.convert()
    sheet_rect = sheet.get_rect()
    daftar_objek = []
    posisi_x = sheet_rect.width/nx
    posisi_y = sheet_rect.height/ny

    for i in range(0,ny):
        for j in range(0,nx):
            rect = pygame.Rect((j*posisi_x,i*posisi_y,posisi_x,posisi_y))
            image = pygame.Surface(rect.size)
            image = image.convert()
            image.blit(sheet,(0,0),rect)

            if colorkey != None:
                if colorkey == -1:
                    colorkey = image.get_at((0,0))
                image.set_colorkey(colorkey,RLEACCEL)
            if scalex != -1 or scaley != -1:
                image = pygame.transform.scale(image,(scalex,scaley))
            daftar_objek.append(image)
    objek_rect = daftar_objek[0].get_rect()
    return daftar_objek,objek_rect

#Fungsi untuk menampilkan permainan berakhir
def tampilkan_permainan_selesai(mulai_ulang_gambar_image,permainan_berakhir_image):
    mulai_ulang_gambar_rect = mulai_ulang_gambar_image.get_rect()
    mulai_ulang_gambar_rect.centerx = width / 2
    mulai_ulang_gambar_rect.top = height*0.52

    permainan_berakhir_rect = permainan_berakhir_image.get_rect()
    permainan_berakhir_rect.centerx = width / 2
    permainan_berakhir_rect.centery = height*0.35

    layar.blit(mulai_ulang_gambar_image, mulai_ulang_gambar_rect)
    layar.blit(permainan_berakhir_image, permainan_berakhir_rect)

#Fungsi untuk mengekstrak angka yang ada pada aset gambar angka
def keluarkan_angka(nomor):
    if nomor > -1:
        digit_angka = []
        i = 0
        while(nomor/10 != 0):
            digit_angka.append(nomor%10)
            nomor = int(nomor/10)

        digit_angka.append(nomor%10)
        for i in range(len(digit_angka),5):
            digit_angka.append(0)
        digit_angka.reverse()
        return digit_angka

#Kelas untuk memunculkan objek dino dan mengatur posisi dino pada layar
class Dino():
    #Method constructor untuk mengakses aset gambar dino
    #Dan juga method untuk mengatur posisi dino pada layar dan mengatur keadaan dino
    def __init__(self,posisi_x=-1,posisi_y=-1):
        self.images,self.rect = muat_gambar_objek('dino.png',5,1,posisi_x,posisi_y,-1)
        self.images1,self.rect1 = muat_gambar_objek('dino_ducking.png',2,1,59,posisi_y,-1)
        self.rect.bottom = int(0.98*height)
        self.rect.left = width/15
        self.image = self.images[0]
        self.indeks = 0
        self.penghitung = 0
        self.skor = 0
        self.sedang_melompat = False
        self.cek_mati = False
        self.sedang_merunduk = False
        self.sedang_berjalan = False
        self.pergerakan = [0,0]
        self.kecepatan_lompatan = 11.5
        self.posisi_berdiri_lebar = self.rect.width
        self.posisi_merunduk_lebar = self.rect1.width

    #Method untuk menampilkan objek dino dengan fitur blit pada pygame
    def draw(self):
        layar.blit(self.image,self.rect)

    #Method untuk mengecek dan mengatur posisi dino agar tetap pada lintasan
    def kembali_sejajar(self):
        if self.rect.bottom > int(0.98*height):
            self.rect.bottom = int(0.98*height)
            self.sedang_melompat = False
  
    #Method untuk melakukan update posisi,pergerakan, dan penghitung pada dino
    def update(self):
        global bonus
        if self.sedang_melompat:
            self.pergerakan[1] = self.pergerakan[1] + gravitasi
        if self.sedang_melompat:
            self.indeks = 0
        elif self.sedang_berjalan:
            if self.indeks == 0:
                if self.penghitung % 400 == 399:
                    self.indeks = (self.indeks + 1)%2
            else:
                if self.penghitung % 20 == 19:
                    self.indeks = (self.indeks + 1)%2
        elif self.sedang_merunduk:
            if self.penghitung % 5 == 0:
                self.indeks = (self.indeks + 1)%2
        else:
            if self.penghitung % 5 == 0:
                self.indeks = (self.indeks + 1)%2 + 2
        if self.cek_mati:
           self.indeks = 4
        if not self.sedang_merunduk:
            self.image = self.images[self.indeks]
            self.rect.width = self.posisi_berdiri_lebar
        else:
            self.image = self.images1[(self.indeks)%2]
            self.rect.width = self.posisi_merunduk_lebar
        self.rect = self.rect.move(self.pergerakan)
        self.kembali_sejajar()
        self.skor = self.skor +  cekk + bonus
        bonus = 0
        self.penghitung = self.penghitung +1

#Kelas untuk memunculkan objek kaktus yaitu rintangan pada permainan
#Pada kelas ini mendukung penyimpanan kumpulan sprite objek
class Kaktus_Hijau(pygame.sprite.Sprite):
    global bisa
    #Method constrcutor untuk memuat aset gambar kaktus dan mengatur pergerakan dan posisi kaktus
    def __init__(self,kecepatan=5,posisi_x=-1,posisi_y=-1):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.images,self.rect = muat_gambar_objek('kaktus_kecil.png',3,1,posisi_x,posisi_y,-1)
        self.rect.bottom = int(0.98*height)
        self.rect.left = width + self.rect.width
        self.image = self.images[random.randrange(0,3)]
        self.pergerakan = [-1*kecepatan,0]
        
    #Method untuk memunculkan gambar kaktus pada layar
    def draw(self):
        layar.blit(self.image,self.rect)

    #Method untuk melakukan update pergerakan pada kaktus
    def update(self):
        self.rect = self.rect.move(self.pergerakan)
        if self.rect.right < 0:
            self.kill()

#Kelas untuk menampilkan objek burung pada game
#Pada kelas ini mendukung penyimpanan kumpulan sprite objek
class Burung(pygame.sprite.Sprite):
    #Method constructor untuk memuat aset gambar burung dan mengatur posisi burung pada layar
    def __init__(self,kecepatan=5,posisi_x=-1,posisi_y=-1):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.images,self.rect = muat_gambar_objek('burung.png',2,1,posisi_x,posisi_y,-1)
        self.burung_height = [height*0.82,height*0.75,height*0.60]
        self.rect.centery = self.burung_height[random.randrange(0,3)]
        self.rect.left = width + self.rect.width
        self.image = self.images[0]
        self.pergerakan = [-1*kecepatan,0]
        self.indeks = 0
        self.penghitung = 0

    #Method untuk menampilkan objek burung jika method ini dipanggil
    def draw(self):
        layar.blit(self.image,self.rect)

    #Method untuk melakukan update pergerakan pada burung dan melakukan pergerakan
    #menggerakkan sayap berdasarkan variabel penghitung yang dibuat
    def update(self):
        if self.penghitung % 10 == 0:
            self.indeks = (self.indeks+1)%2
        self.image = self.images[self.indeks]
        self.rect = self.rect.move(self.pergerakan)
        self.penghitung = (self.penghitung + 1)
        if self.rect.right < 0:
            self.kill()

#Kelas untuk menampilkan objek tanah sebagai lintasan dino
class Tanah():
    #Method constructor untuk memuat aset gambar tanah dan mengatur kecepatan mundur tanah
    def __init__(self,kecepatan=-5):
        self.image,self.rect = muat_gambar('ground.png',-1,-1,-1)
        self.image1,self.rect1 = muat_gambar('ground.png',-1,-1,-1)
        self.rect.bottom = height
        self.rect1.bottom = height
        self.rect1.left = self.rect.right
        self.kecepatan = kecepatan

    #Method ini berfungsi untuk menampilkan objek tanah dan dilakukan sebanyak dua kali
    #Agar tanah memanjang dan tidak terputus
    def draw(self):
        layar.blit(self.image,self.rect)
        layar.blit(self.image1,self.rect1)

    #Method ini berfungsi untuk melakukan update pergerakan pada kecepatan tanah
    def update(self):
        self.rect.left += self.kecepatan
        self.rect1.left += self.kecepatan
        if self.rect.right < 0:
            self.rect.left = self.rect1.right
        if self.rect1.right < 0:
            self.rect1.left = self.rect.right

#Kelas ini berfungsi untuk menampilkan objek awan
#Pada kelas ini mendukung penyimpanan kumpulan sprite objek
class Awan(pygame.sprite.Sprite):
    #Method constructor yang berfungsi untuk memuat kumpulan awan dari aset gambar
    #Method ini juga berfungsi untuk mengatur posisi x dan y pada layar
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image,self.rect = muat_gambar('cloud.png',int(90*30/42),30,-1)
        self.kecepatan = 1
        self.rect.left = x
        self.rect.top = y
        self.pergerakan = [-1*self.kecepatan,0]

    #Method ini berfungsi untuk menampilkan awan jika dipanggil
    def draw(self):
        layar.blit(self.image,self.rect)

    #Method ini melakukan update pergerakan awan dan menghilangkannya saat terlewati
    def update(self):
        self.rect = self.rect.move(self.pergerakan)
        if self.rect.right < 0:
            self.kill()

#Kelas ini berfungsi untuk menampilkan objek papan skor
class Papan():
    #Method ini berfungsi untuk memuat aset nomor dan juga menentukan posisi pada layar
    def __init__(self,x=-1,y=-1):
        self.skor = 0
        self.gambar_sementara,self.gambar_angka = muat_gambar_objek('numbers.png',12,1,11,int(11*6/5),-1)
        self.image = pygame.Surface((55,int(11*6/5)))
        self.rect = self.image.get_rect()
        if x == -1:
            self.rect.left = width*0.89
        else:
            self.rect.left = x
        if y == -1:
            self.rect.top = height*0.1
        else:
            self.rect.top = y

    #Method ini berfungsi untuk menampikan angka jika method ini dipanggil
    def draw(self):
        layar.blit(self.image,self.rect)

    #Method ini berfungsi untuk melakukan update skor dengan parameter dari variabel global cekk
    def update(self,cekk):
        skor_digit_angka = keluarkan_angka(cekk)
        self.image.fill(warna_latar)
        for s in skor_digit_angka:
            self.image.blit(self.gambar_sementara[s],self.gambar_angka)
            self.gambar_angka.left += self.gambar_angka.width
        self.gambar_angka.left = 0

#Fungsi ini berfungsi untuk menampilkan tampilan awal permainan ketika dibuka,
#yakni memunculkan objek menu, logo game dan juga dino serta tanah pada game
def menu_utama():
    global jumlah_mati
    sementara_dino = Dino(44,47)
    sementara_dino.sedang_berjalan = True
    gameStart = False
    point = 0
    pilihan = 'Mulai Permainan'
    mulai_ulang_gambar_image,mulai_ulang_gambar_rect = muat_gambar('replay_button.png',35,31,-1)
    permainan_berakhir_image,permainan_berakhir_rect = muat_gambar('game_over.png',229,29,-1)
    sementara_tanah= Tanah()
    #Memuat logo game dino run by hello wolrd
    logo,logo_rect = muat_gambar('logo.png',250,185,-1)
    logo_rect.centerx = width*0.6
    logo_rect.centery = height*0.6
    while not gameStart:
        if pygame.display.get_surface() == None:
            print("Gagal memuat gambar")
            return True
        else:
            if pilihan == 'Mulai Permainan':
                mulai = huruf.render('Mulai Permainan', True, hijau)
                keluar = huruf.render('Keluar', True, merah)
            elif pilihan == 'Keluar':
                mulai = huruf.render('Mulai Permainan', True, merah)
                keluar = huruf.render('Keluar', True, hijau)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        pilihan = 'Mulai Permainan'
                    elif event.key == pygame.K_DOWN:
                        pilihan = 'Keluar'
                    elif event.key ==  pygame.K_RETURN:
                        if pilihan == 'Mulai Permainan':
                            sementara_dino.sedang_melompat = True
                            sementara_dino.sedang_berjalan = False
                        elif pilihan == 'Keluar':
                            pygame.quit()
                            sys.exit()
        sementara_dino.update()
        if pygame.display.get_surface() != None:
            tampilkan_permainan_selesai(mulai_ulang_gambar_image,permainan_berakhir_image)
            layar.fill(warna_latar)
            sementara_tanah.draw()
            #Menampilkan permainan berakhir saat game berakhir 
            if sementara_dino.sedang_berjalan and jumlah_mati != 0:
                tampilkan_permainan_selesai(mulai_ulang_gambar_image,permainan_berakhir_image)
            if sementara_dino.sedang_berjalan and jumlah_mati ==0:
                layar.blit(logo,logo_rect)
                #Menampilkan menu mulai dan keluar
                #menampilkan tulisan mulai permainan
                layar.blit(mulai,(lebar_layar/10, tinggi_layar/10))
                #menampilkan tulisan keluar
                layar.blit(keluar,(lebar_layar/10, 3*tinggi_layar/10))
            sementara_dino.draw()
            pygame.display.update()
        clock.tick(FPS)
        if sementara_dino.sedang_melompat == False and sementara_dino.sedang_berjalan == False:
            gameStart = True

#Fungsi ini merupakan fungsi utama dalam mengatur proses yang terjadi dalam game
#Fungsi ini juga berfungsi dalam menampilkan objek objek kelas yang telah dibuat
def dalam_permainan():
    global skor_tinggi , cekk, bisa, simpan,pip,perubahan_kecepatan
    global bonus, jumlah_mati
    pilihan = 'Mulai Permainan'
    kecepatan_permainan = 4
    startMenu = False
    permainan_berakhir = False
    keluar_permainan = False
    pemain_dino = Dino(44,47)
    new_tanah = Tanah(-1*kecepatan_permainan)
    nilai_skor = Papan()
    tertinggi_skor = Papan(width*0.78)
    penghitung = 0
    kaktus = pygame.sprite.Group()
    burung_burung = pygame.sprite.Group()
    awan_awan = pygame.sprite.Group()
    rintangan_terakhir = pygame.sprite.Group()

    Kaktus_Hijau.containers = kaktus
    Burung.containers = burung_burung
    Awan.containers = awan_awan

    sementara_images,sementara_rect = muat_gambar_objek('numbers.png',12,1,11,int(11*6/5),-1)
    gambar_skor_tinggi = pygame.Surface((22,int(11*6/5)))
    skor_tinggi_rect = gambar_skor_tinggi.get_rect()
    gambar_skor_tinggi.fill(warna_latar)
    gambar_skor_tinggi.blit(sementara_images[10],sementara_rect)
    sementara_rect.left += sementara_rect.width
    gambar_skor_tinggi.blit(sementara_images[11],sementara_rect)
    skor_tinggi_rect.top = height*0.1
    skor_tinggi_rect.left = width*0.73

    #Looping terus menerus saat game tidak dikeluarkan
    while not keluar_permainan:
        while startMenu:
            pass

        while not permainan_berakhir:
            jumlah_mati+=1
            if pygame.display.get_surface() == None:
                print("Tidak dapat memuat permainan")
                keluar_permainan = True
                permainan_berakhir = True
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        keluar_permainan = True
                        permainan_berakhir = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            if pemain_dino.rect.bottom == int(0.98*height):
                                pemain_dino.sedang_melompat = True
                                if pygame.mixer.get_init() != None:
                                    suara_lompat.play()
                                pemain_dino.pergerakan[1] = -1*pemain_dino.kecepatan_lompatan
                        if event.key == pygame.K_DOWN:
                            if not (pemain_dino.sedang_melompat and pemain_dino.cek_mati):
                                pemain_dino.sedang_merunduk = True
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_DOWN:
                            pemain_dino.sedang_merunduk = False
            #Melakukan perulangan pada setiap kontainer kaktus
            for c in kaktus:
                c.pergerakan[0] = -1*kecepatan_permainan
                while perubahan_kecepatan < 740:
                    perubahan_kecepatan += kecepatan_permainan
                if pip < kecepatan_permainan:
                    pip = kecepatan_permainan
                #Jarak dari kaktus dari kanan ke kiri layar adalah 740 pixel
                #Saat melewati 740 pixel tersebut maka skor akan bertambah 1
                elif c.rect.left == ((740 -  perubahan_kecepatan)):
                    bisa = True
                    simpan +=1
                    if (simpan ) % 5 == 0:
                        bonus = 10
                    if simpan % 10 ==0:
                        if pygame.mixer.get_init() != None:
                                    suara_cekpoin.play()
                        bisa = True
                        kecepatan_permainan += 1
                perubahan_kecepatan = 0    
                #Mengecek apakah dino menyetuh kaktus dan jika menyentuh permainan berakhir
                if pygame.sprite.collide_mask(pemain_dino,c):
                    pemain_dino.cek_mati = True
                    perubahan_kecepatan = 0
                    simpan = 0
                    bonus = 0
                    if pygame.mixer.get_init() != None:
                        suara_mati.play()
                    menu_utama()
            #Melakukan pergerakan burung dan mengecek sentuhan dengan dino
            for p in burung_burung:
                p.pergerakan[0] = -1*kecepatan_permainan
                if pygame.sprite.collide_mask(pemain_dino,p):
                    pemain_dino.cek_mati = True
                    perubahan_kecepatan = 0
                    simpan = 0
                    bonus = 0
                    if pygame.mixer.get_init() != None:
                        suara_mati.play()
            #Mengecek jumlah kaktus dan memunculkannya di layar posisi secara acak
            if len(kaktus) < 2:
                if len(kaktus) == 0:
                    rintangan_terakhir.empty()
                    rintangan_terakhir.add(Kaktus_Hijau(kecepatan_permainan,40,40))
                else:
                    for l in rintangan_terakhir:
                        if l.rect.right < width*0.7 and random.randrange(0,50) == 10:
                            rintangan_terakhir.empty()
                            rintangan_terakhir.add(Kaktus_Hijau(kecepatan_permainan, 40, 40))
           #Memunculkan burung dengan fungsi random antara 0-200, serta saat penghitung > 500
            if len(burung_burung) == 0 and random.randrange(0,200) == 10 and penghitung > 500:
                for l in rintangan_terakhir:
                    if l.rect.right < width*0.8: 
                        rintangan_terakhir.empty()
                        rintangan_terakhir.add(Burung(kecepatan_permainan, 46, 40))

            if len(awan_awan) < 5 and random.randrange(0,300) == 10:
                Awan(width,random.randrange(height/5,height/2))
            if bisa == True:
                cekk = 1 
                bisa = False
            pemain_dino.update()
            kaktus.update()
            burung_burung.update()
            awan_awan.update()
            new_tanah.update()
            nilai_skor.update(cekk)
            nilai_skor.update(pemain_dino.skor)
            cekk=0
            tertinggi_skor.update(skor_tinggi)
      
            if pygame.display.get_surface() != None:
                layar.fill(warna_latar)
                new_tanah.draw()
                awan_awan.draw(layar)
                nilai_skor.draw()
                if skor_tinggi != 0:
                    tertinggi_skor.draw()
                    layar.blit(gambar_skor_tinggi,skor_tinggi_rect)
                kaktus.draw(layar)
                burung_burung.draw(layar)
                pemain_dino.draw()
                pygame.display.update()
            clock.tick(FPS)

            if pemain_dino.cek_mati:
                permainan_berakhir = True
                if pemain_dino.skor > skor_tinggi:
                    skor_tinggi = pemain_dino.skor
            if penghitung%740 == 740:
                new_tanah.kecepatan -= 1
            penghitung = (penghitung + 1)
        if keluar_permainan:
            break

        while permainan_berakhir:
            if pilihan == 'Mulai Permainan':
                mulai = huruf.render('Mulai Permainan', True, hijau)
                keluar = huruf.render('Keluar', True, merah)
            elif pilihan == 'Keluar':
                mulai = huruf.render('Mulai Permainan', True, merah)
                keluar = huruf.render('Keluar', True, hijau)
            if pygame.display.get_surface() == None:
                print("Gagal memuat tampilan.")
                keluar_permainan = True
                permainan_berakhir = False
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        keluar_permainan = True
                        permainan_berakhir = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            keluar_permainan = True
                            permainan_berakhir = False
                        elif event.key == pygame.K_UP:
                            pilihan = 'Mulai Permainan'
                        elif event.key == pygame.K_DOWN:
                            pilihan = 'Keluar'
                        elif event.key ==  pygame.K_RETURN:
                            if pilihan == 'Mulai Permainan':
                                permainan_berakhir = True
                                dalam_permainan()
                            elif pilihan == 'Keluar':
                                pygame.quit()
                                sys.exit()
                   
            tertinggi_skor.update(skor_tinggi)
            if pygame.display.get_surface() != None:
                if skor_tinggi != 0:
                    tertinggi_skor.draw()
                layar.blit(gambar_skor_tinggi,skor_tinggi_rect)
                #Menampilkan menu mulai dan keluar
                layar.blit(mulai,(lebar_layar/10, tinggi_layar/10))
                layar.blit(keluar,(lebar_layar/10, 3*tinggi_layar/10))
                pygame.display.update()
            clock.tick(FPS)
    pygame.quit()
    quit()

#Fungsi utama yang dipanggil saat program dimulai
def main():
    cek_permainan_berakhir = menu_utama()
    if not cek_permainan_berakhir:
        dalam_permainan()

main()
