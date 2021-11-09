### ○開発環境
>* Raspberry Pi Zero
>* Python3

### ○実行環境
>* Flask
>* 仮想サーバー：ngrok

### **※本プログラムは各種モジュールのインストールが必要です**

### ○必要なコマンド(install)
>* pip3 install line-bot-sdk
>* pip3 install flask
>* wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip
>* unzip ngrok-stable-linux-arm.zip
>* sudo mv ngrok /usr/local/bin/
>* curl -sL https://github.com/Seeed-Studio/grove.py/raw/master/install.sh | sudo bash -s
>* git clone https://github.com/Seeed-Studio/Seeed_Python_DHT.git
>* cd Seeed_Python_DHT
>* sudo python3 setup.py install
>* "$ sudo raspi-config" からSPI通信を有効化
>* sudo apt install pigpio
>* sudo service pigpiod start
>* sudo systemctl enable pigpiod.service
>* python3 -m venv env
>* source env/bin/activate
>* pip3 install pigpio
>* pip3 install gpiozero

### ○実行方法
>* "$ which ngrok" でngrokのファイル場所を確認（コマンドで/usr/local/bin/に移動してある）
>* "$ ファイルパス ngrok http 使用したいポート番号" でngrokが起動
>* httpsから始まるURLに/callbackをつけてLINEBotのwebhookとして設定する
>* ngrok起動後に本pythonコードを実行

###  ○参考文献
>**LINEBot関連**<br>
>* LINEのメッセージでRaspberryPIのLEDをON／OFFしてみる（その１）設定<br>
>https://note.com/khe00716/n/n34bb4c087fdc<br>
>**温度湿度センサ**<br>
>* RaspberryPi ZeroでGroveセンサのテスト<br>
>https://tiblab.net/blog/2020/11/grove_sensor_with_raspberrypi-zero/<br>
>**土壌湿度センサ**<br>
>* ラズパイを使って、土壌湿度センサーからデータを取得するよ<br>
>https://zenn.dev/kotaproj/articles/a3466109420da9de0454

以上