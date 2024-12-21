## DICODING DATA ANALYSIS FINAL PROJECT

# Setup Environtment - Anaconda
conda create --name main-ds python=3.12
conda activate main-ds
pip install -r requirements.txt

# Setup Environment - Shell/Terminal
mkdir Submission
cd Submission
pipenv install
pipenv shell
pip install -r requirements.txt

# Run streamlit app
streamlit run Visualize_AirCond.py