# Gesture-Backend

## LivenessApp

### 1. Install conda and make conda env
`conda create --name liveness python=3.6`

### 2. Activate conda env
`conda activate liveness`

### 3. Install the requirements
`while read requirement; do conda install --yes $requirement; done < requirements.txt`

### 4. Install dlib
`conda config --add channels conda-forge`
`conda install dlib-cpp`
`conda install dlib`

### 5. Install gunicorn
`pip install gunicorn`

### 6. run app from gunicorn
`gunicorn run:app`
