from flask import Flask, request, render_template
import pickle
import requests
import json

app = Flask(__name__)
#model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return  render_template('index1.html')

@app.route('/input', methods=['GET','POST'])
def pred():
    gender = request.form.get('gender')
    ssc_p = request.form.get('ssc_p')
    ssc_b = request.form.get('ssc_b')
    hsc_p = request.form.get('hsc_p')
    hsc_s = request.form.get('hsc_s')
    degree_p = request.form.get('degree_p')
    degree_t = request.form.get('degree_t')
    workex = request.form.get('workex')
    etest_p = request.form.get('etest_p')
    specialisation = request.form.get('specialization')
    mba_p = request.form.get('mba_p')


    input = [[str(gender),float(ssc_p),str(ssc_b),float(hsc_p),str(hsc_s),float(degree_p),str(degree_t),str(workex),float(etest_p),str(specialisation),float(mba_p) ]]
    import requests
    # NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
    API_KEY = "qQVGFA6ql-II5nFU_F5JYqgji04OeSuUIWVj71EIU7zG"
    token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
    mltoken = token_response.json()["access_token"]

    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": [ "f0", "f1","f2", "f3","f4", "f5", "f6", "f7","f8","f9","f10"], "values": [[str(gender),float(ssc_p),float(hsc_p),str(hsc_s),float(degree_p),str(degree_t),str(ssc_b),str(workex),float(etest_p),str(specialisation),float(mba_p)] ]}]}
    response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/f1044a54-63b9-4590-95ce-2e49462af1da/predictions?version=2021-05-01', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())
    op = response_scoring.json()
    print(op)
    a = op['predictions'][0]
    b = a['values'][0][0]
    op = int(b)
    if op == 1:
        result_message = "Congratulations! You are placed."
    else:
        result_message = "Unfortunately, you are not placed."
    return render_template('index1.html',Output=result_message)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8000)
