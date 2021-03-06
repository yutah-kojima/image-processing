# パソコンの前にいるのは何！？　〜YOLOX + openCV〜
カメラに映り込むターゲットを検知してSlack通知を行います。  

# Demo　　
```
python run.py
```  


###  開発環境  
- MacBook Pro M1(macOS Big Sur)
- python 3.9.7(anaconda)  
<br>

# 導入方法

## YOLOXのインストール　　

YOLOXのリポジトリをクローンします。  
```
git clone git@github.com:Megvii-BaseDetection/YOLOX.git
cd YOLOX
```
必要パッケージをインストールします。
```
pip install -U pip && pip install -r requirements.txt
pip install -v -e .
```  

<br>  

## 学習済みモデルの導入
YOLOX公式サイトより任意の学習済みモデルをダウンロードします。
https://yolox.readthedocs.io/en/latest/model_zoo.html  
<br>
赤枠の部分から任意のものを選びます。  
![例](/static/model_zoo.png)   
ダウンロードした[yolox_*.pth]ファイルを下記ディレクトリに移動します。（weightsフォルダを新たに作成します。）  
`YOLOX/weights/yolox_*.pth`  
<br>

##  設定
config/config.json  
で設定を行います。  
<br>
camera_num          :   アクセスするカメラの番号 ex.0 （特に指定がなければ[0]）  
target_class        :   ターゲットクラスの番号　ex.0 （static/Class_table.pngを参照してください。)　　
module_name         :   学習済みモデルのモジュール名  ex."yolox.exp.defalt.yolox_****"   
weight_file         :   学習済みモデルのパス ex.YOLOX/weights/yolox_tiny.pth  
set_timer           :   通知する際のターゲットの滞在時間 ex.5(ターゲットが５秒滞在すると通知されます。)  
allow_notification  :   Slack通知の有無（true:通知する, false:通知しない）  
token               :   Slackのbotトークン ex."xoxb-***********"  
channel             :   Slackの通知したいチャンネル名 ex."#notification"  
<br>  

##  起動
必要なモジュールをインストールします。
```
pip install -r requirements.txt
```  
<br>  

##  テスト  
実行場所は`image_processing`ディレクトリ上で行います。
```
pytest -v tests
```

