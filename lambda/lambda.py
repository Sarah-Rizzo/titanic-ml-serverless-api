import json
import pickle
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("sobreviventes")

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

def response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }

def create_passengers(event):
    body = json.loads(event.get("body", "{}"))

    passageiros = body.get("passageiros")

    if len(passageiros) == 0:
        return response(400, {"erro": "Campo 'passageiros' precisa ter pelo menos um passageiro"})

    resultados = []
    required_fields = [
        "idade", 
        "sexo", 
        "classe",
        "tarifa",
        "qtd_acompanhantes", 
        "qtd_pais_filhos", 
        "porto_embarque"
    ]

    for p in passageiros:
        try:
            missing = [f for f in required_fields if f not in p]
            if missing:
                resultados.append({
                    "erro": f"Campos ausentes: {missing}",
                    "input": p
                })
                continue

            age = float(p["idade"])
            parch = int(p["qtd_pais_filhos"])
            sibsp = int(p["qtd_acompanhantes"])
            fare = float(p["tarifa"])
            pclass = int(p["classe"])

            sexo = p["sexo"].lower()
            if sexo not in ["homem", "mulher"]:
                raise ValueError("sexo inválido")

            sex_male = 1 if sexo == "homem" else 0

            embarked = p["porto_embarque"].upper()
            if embarked not in ["C", "Q", "S"]:
                raise ValueError("porto_embarque inválido")

            embarked_Q = 1 if embarked == "Q" else 0
            embarked_S = 1 if embarked == "S" else 0

            features = [
                age,
                parch,
                sibsp,
                fare,
                pclass,
                sex_male,
                embarked_Q,
                embarked_S
            ]

            prob = model.predict_proba([features])[0][1]

            passenger_id = str(uuid.uuid4())

            item = {
                "id": passenger_id,
                "probabilidade": float(prob)
            }

            table.put_item(Item=item)

            resultados.append(item)

        except Exception as e:
            resultados.append({
                "erro": str(e),
                "input": p
            })

    return response(200, resultados)


def get_all():
    result = table.scan()
    return response(200, result.get("Items", []))


def get_by_id(passenger_id):
    result = table.get_item(Key={"id": passenger_id})

    if "Item" not in result:
        return response(404, {"erro": "Passageiro não encontrado"})

    return response(200, result["Item"])


def delete(passenger_id):
    table.delete_item(Key={"id": passenger_id})
    return response(200, {"mensagem": "Deletado com sucesso"})


def lambda_handler(event):
    method = event["requestContext"]["http"]["method"]
    path = event["rawPath"]

    try:
        
        if method == "POST" and path == "/sobreviventes":
            return create_passengers(event)

        
        if method == "GET" and path == "/sobreviventes":
            return get_all()

       
        if method == "GET" and path.startswith("/sobreviventes/"):
            passenger_id = path.split("/")[-1]
            return get_by_id(passenger_id)

        
        if method == "DELETE" and path.startswith("/sobreviventes/"):
            passenger_id = path.split("/")[-1]
            return delete(passenger_id)

        return response(404, {"erro": "Rota não encontrada"})

    except Exception as e:
        return response(500, {"erro": str(e)})