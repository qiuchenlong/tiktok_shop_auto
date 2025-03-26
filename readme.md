


- mac
python3 -m venv .
source bin/activate

pip3 freeze > requirements.txt
pip3 install -r requirements.txt


- window
python -m venv .
cd Scripts
activate

pip freeze > requirements.txt
pip install -r requirements.txt


pip install DrissionPage




pip3 freeze > requirements.txt

pip3 install -r requirements.txt





pyinstaller -F -w main.py

-F: 单个可执行文件
-w: 不带命令