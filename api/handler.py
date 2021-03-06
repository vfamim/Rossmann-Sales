from flask import Flask, request, Response
import pandas as pd
from rossmann.Rossmann import Rossmann
import pickle

# loading model
model = pickle.load(
    open('/media/vfamim2/MEUS PROJETOS DS 2/Rossman/Rossman_sales/model/model_rossman.pkl', 'rb'))
# initialize API
app = Flask( __name__ )

@app.route( '/rossmann/predict', methods=['POST'] )
def rossmann_predict():
    test_json = request.get_json()
   
    # checking if there is data
    if test_json: # there is data
        if isinstance( test_json, dict ): # for unique example
            test_raw = pd.DataFrame( test_json, index=[0] )
            
        else: # for multiple examples
            test_raw = pd.DataFrame( test_json, columns=test_json[0].keys() )
            
        # Instantiate Rossmann class
        pipeline = Rossmann() # creating an Rossmann class object
        
        # data cleaning
        df1 = pipeline.data_cleaning( test_raw )
        
        # feature engineering
        df2 = pipeline.feature_engineering( df1 )
        
        # data preparation
        df3 = pipeline.data_preparation( df2 )
        
        # prediction
        df_response = pipeline.get_prediction( model, test_raw, df3 )
        
        return df_response
        
        
    else:
        return Reponse( '{}', status=200, mimetype='application/json' )

if __name__ == '__main__':
    app.run( '0.0.0.0' )