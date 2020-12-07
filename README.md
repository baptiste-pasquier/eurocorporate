conda create -n py36 python=3.6
conda activate py36
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
fbs run
fbs freeze
fbs installer