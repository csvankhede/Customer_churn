from flask import Flask, jsonify, request
import findspark
findspark.init()
# import libraries
import pyspark 
from pyspark.ml import PipelineModel
from pyspark.sql.types import StructType
import pyspark as ps 
from pyspark import SQLContext
import traceback

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def predict():
    try:
        json = request.get_json(force=True)
        sample = sqlContext.createDataFrame(sc.parallelize([json]),schema=schema)
        pred = model.transform(sample)
        probability = pred.select('probability').collect()[0].asDict()['probability'][1]
        return jsonify({'probability':probability})
    except:
        return jsonify({'traceback':traceback.format_exc()})


if __name__=="__main__":
    """
    Run below command in terminal

    curl -X GET http://localhost:5000 -d '{"customerid": "6713-OKOMC", "gender": "Female", "seniorcitizen": 0, "partner": "No", "dependents": "No", "tenure": 10, "phoneservice": "No", "multiplelines": "No phone service", "internetservice": "DSL", "onlinesecurity": "Yes", "onlinebackup": "No", "deviceprotection": "No", "techsupport": "No", "streamingtv": "No", "streamingmovies": "No", "contract": "Month-to-month", "paperlessbilling": "No", "paymentmethod": "Mailed check", "monthlycharges": 29.75, "totalcharges": 301.9}'
    """
    sc = ps.SparkContext()
    sqlContext = SQLContext(sc)
    # print("Loading model...") 
    # load pipeline
    model = PipelineModel.load('pickled_obj/pipeline_v01')

    # load schema
    schema_rdd = sc.pickleFile('pickled_obj/schema.pickle')
    schema = StructType(schema_rdd.collect())

    # sample = '{"customerid": "6713-OKOMC", "gender": "Female", "seniorcitizen": 0, "partner": "No", "dependents": "No", "tenure": 10, "phoneservice": "No", "multiplelines": "No phone service", "internetservice": "DSL", "onlinesecurity": "Yes", "onlinebackup": "No", "deviceprotection": "No", "techsupport": "No", "streamingtv": "No", "streamingmovies": "No", "contract": "Month-to-month", "paperlessbilling": "No", "paymentmethod": "Mailed check", "monthlycharges": 29.75, "totalcharges": 301.9}'
    app.run(debug=True)
