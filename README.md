# ENGLISH VERSION
Go to this page if you wanna read english version [English Version](https://github.com/GlgApr/TorrentMega2GoogleDrive/blob/master/README-E.md)

# Repo apaan ni man?
Repo puyuh buat download dari torrent/mega.nz/direct link terus diupload ke Google Drive tercinta, support TeamDrive juga biar storagemu ga penuh + support Google Drive Index juga biar ga repot atur-atur izin..
Anggap aja kalian udah tau tentang heroku, udah punya akunnya, minimal tau lah ya basicnya.

# TUTORIAL LENGKAP?
Klo butuh tutorial lengkap, ngomong aje ye, bakal ditulis di [Blog ini](https://bloggertamvan.com)


# Inspiration 
This project is heavily inspired from @out386 's telegram bot which is written in JS.


# Fitur-fitur mantapnya antara lain:
- Download dari torrent, mega.nz, atau direct link ke google drive
- Download dari streaming video kek Youtube, Dailymotion, Zippyshare, dkk ke Google Drive
- Download proses
- Upload proses
- Kecepatan Download/upload lengkap dengan sisa waktu
- Docker support
- Uploading To Team Drives.
- Index Link support
- Service account support
- Download dari semua link yang didukung youtube-dl
- Download dari telegram file

# Upcoming features (TODOs):

# Cara deploy?
Sabar ya, ini agak ribet kalau masih pertama kali.

- Clone this repo (pastiin udah install git ya) atau download langsung masternya yang format .zip nya juga bisa:
```
git clone https://github.com/glgapr/TorrentMega2GoogleDrive
cd TorrentMega2GoogleDrive
```

## Setting up config file
- Copy file config_sample.env terus rename jadi config.env
```
cp config_sample.env config.env
```
- Hapus garis pertama yang tulisannya:
```
_____REMOVE_THIS_LINE_____=True
```
Terus edit, isi data sesuai yang diminta:
- **BOT_TOKEN** : Telegram bot token dari @BotFather
- **GDRIVE_FOLDER_ID** : ID Folder Google Drive buat tempat upload hasil download.
- **TELEGRAPH_TOKEN** : Jalankan perintah di bawah ini untuk mendapatkan token:
```
python3 telegraph_token.py
```
- **DOWNLOAD_DIR** : Lokasi unduhan default di servermu
- **DOWNLOAD_STATUS_UPDATE_INTERVAL** : Lama waktu status download diupdate, default 5. Ga ngerti biarin aja  
- **OWNER_ID** : user ID Telegram pembuat (bukan username). Cek id? Pake aja bot https://t.me/myidbot
- **AUTO_DELETE_MESSAGE_DURATION** : Lama waktu untuk menghapus pesan yang dikirim ke bot, isi -1 biar ga kehapus.
- **IS_TEAM_DRIVE** : Isi "True" klo mau make Team Drive, klo ngga isi "False" atau kosongin aja (tanpa tanda ").
- **USE_SERVICE_ACCOUNTS**: Kalau ga paham kosongin aja.
- **INDEX_URL** : Link Google Drive Index, ga paham? Baca aja di sini https://github.com/maple3142/GDIndex/. Harus http dan tanpa / diakhir link. Ga paham? Kosongin aja wes.
- **API_KEY** : Buat download file dari telegram butuh API ini, dambil di https://my.telegram.org (tanpa "")
- **API_HASH** : Buat download file dari telegram butuh API ini, dambil di https://my.telegram.org
- **USER_SESSION_STRING** : Jalankan perintah ini untuk ngambil session string:
```
python3 generate_string_session.py
```
- **MEGA_API_KEY**: API Mega.nz buat download dari mega.nz. Ambil di [Mega SDK Page](https://mega.nz/sdk)
- **MEGA_EMAIL_ID**: Email mega.nz untuk make akun premium
- **MEGA_PASSWORD**: Password mega.nz . Ga ngerti? Kosongin aja.

Note: Kalian bisa atur maksimal proses download dalam 1 waktu di MAX_CONCURRENT_DOWNLOADS di aria.sh. Bawaannya itu 5
 
## Ambil API Google OAuth credential file

- Buka link [Google Cloud Console](https://console.developers.google.com/apis/credentials)
- Pergi ke OAuth Consent tab, isi terus simpan.
- Pergi ke Credentials tab terus klik Create Credentials -> OAuth Client ID
- Pilih Desktop dan Create.
- Download credentials yang barusan dibuat (ada icon download gitu).
- Pindahkan ke dalam folder projek ini terus rename jadi credentials.json
- Pergi ke [Google API page](https://console.developers.google.com/apis/library)
- Cari Drive terus enable klo sebelumnya disabled
- Jalankan perintah ini untuk membuat file token (token.pickle) untuk Google Drive:
```
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
python3 generate_drive_token.py
```
- Klo error, pastiin udah nginstall yang dibutuhkan


# Menggunakan akun di web yang support Youtube-dl
Klo mau make premium akun yang support di youtube-dl, ubah netrc file dengan format:
```
machine host login username password my_youtube_password
```
host ini adalah website tujuan, misalnya youtube, twitch, dll. 
klo mau lebih dari 2 akun tinggal tambahin aja di baris baru.

# Buat database di heroku
- Tambahin addon Heroku Postgres
```
heroku addons:create heroku-postgresql
```
- Salin DATABASE_URL value dari heroku app config vars
```
python3 create_table.py 
```
- Paste

## Deploying on Heroku

- Run the script to generate token file(token.pickle) for Google Drive:
```
python3 generate_drive_token.py
```
- Install [Heroku cli](https://devcenter.heroku.com/articles/heroku-cli)
- Login ke akun heroku:
```
heroku login
```
- Buat app heroku:
```
heroku create ISI-NAMA-APP-MU
```
- Pilih app di Heroku-cli: 
```
heroku git:remote -a ISI-NAMA-APP-MU
```
- Ubah Dyno Stack ke Docker Container:
```
heroku stack:set container
```
- Tambah database - [check here](https://github.com/glgapr/TorrentMega2GoogleDrive#buat-database-di-heroku) (kalau sudah buat abaikan)

- Tambahin file ini:
```
git add -f credentials.json token.pickle config.env heroku.yml
```
- Commit:
```
git commit -m "ScupidC0des."
```
- Push Code to Heroku:
```
git push heroku master --force
```
- Restart Worker:
```
heroku ps:scale worker=0
```
- Tunggu aja sampe selesai, nanti jalankan lagi
```
heroku ps:scale worker=1	 	
```

# Kalau mau make akun service, bisa ikutin cara ini. Ga ngerti? Kosongin aja gpp, lewatin aja.
For Service Account to work, you must set USE_SERVICE_ACCOUNTS="True" in config file or environment variables
Many thanks to [AutoRClone](https://github.com/xyou365/AutoRclone) for the scripts
## Generating service accounts
Step 1. Generate service accounts [What is service account](https://cloud.google.com/iam/docs/service-accounts)
---------------------------------
Let us create only the service accounts that we need. 
**Warning:** abuse of this feature is not the aim of autorclone and we do **NOT** recommend that you make a lot of projects, just one project and 100 sa allow you plenty of use, its also possible that overabuse might get your projects banned by google. 

```
Note: 1 service account can copy around 750gb a day, 1 project makes 100 service accounts so thats 75tb a day, for most users this should easily suffice. 
```

`python3 gen_sa_accounts.py --quick-setup 1 --new-only`

A folder named accounts will be created which will contain keys for the service accounts created

NOTE: If you have created SAs in past from this script, you can also just re download the keys by running:
```
python3 gen_sa_accounts.py --download-keys project_id
```

### Add all the service accounts to the Team Drive or folder
- Run:
```
python3 add_to_team_drive.py -d SharedTeamDriveSrcID
```

# THANKS TO
- Izzy12
- SVR666

