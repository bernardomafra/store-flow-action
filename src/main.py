from src.services.runner import Runner
from flask import Flask, Response, request
from src.database.db import initialize_db
from src.database.models import Flow
import json

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'flow_action',
    'host': 'mongodb+srv://root:root@storeflow.qblw6.mongodb.net/store-flow?retryWrites=true&w=majority'
}

db = initialize_db(app)


@app.route('/flows', methods=['GET'])
def get_flows():
  flows = Flow.objects(enabled=True).exclude('steps').to_json()
  return Response(flows, mimetype="application/json", status=200)


@app.route('/search', methods=['POST'])
def add_income():
  body = request.json
  enabled_flows = Flow.objects(enabled=True).to_json()
  
  if body.get('product'):
    try: 
      # data = {"product": body.get('product'), "size": "M", "contact": "tccstoreflow@gmail.com", "country": "Brazil", "first_name": "Bernardo", "last_name":"Mafra", "zip_code": "32545300", "street_and_number": "Rua Mário Machado, 83", "complement": "Casa 3", "city": "Sabará", "state":"MG", "min_price": 7000, "max_price": 8500}
      is_threads_set = Runner(enabled_flows).set_threads(body)
      if is_threads_set:
        return Response(json.dumps({'success': 'searching...'}), mimetype="application/json", status=200)
      else:
        return Response(json.dumps({'error': 'error setting threads'}), mimetype="application/json", status=500)
    except Exception as e:
      print(e)
      return Response(e, mimetype="application/json", status=500)
  else:
    return Response(json.dumps({'error': 'product is required'}), mimetype="application/json", status=400)

if __name__ == "__main__":
  app.run(debug=True)