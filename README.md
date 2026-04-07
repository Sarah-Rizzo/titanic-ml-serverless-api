# Titanic ML Serverless API
API serverless para predição de sobrevivência de passageiros do Titanic utilizando Machine Learning, construída com arquitetura baseada em serviços da AWS e provisionada via Terraform.

## Objetivo

* Expor um modelo de Machine Learning via API REST
* Utilizar arquitetura serverless na AWS
* Provisionar toda a infraestrutura como código (IaC)
* Persistir resultados em banco NoSQL

---
### Componentes:

* **API Gateway**: exposição dos endpoints HTTP
* **AWS Lambda**: processamento das requisições e inferência do modelo
* **DynamoDB**: armazenamento das predições
* **Lambda Layer**: gerenciamento de dependências (scikit-learn, pandas)
* **Terraform**: provisionamento da infraestrutura

---

## Tecnologias utilizadas

* Python 3.10
* Scikit-learn
* Pandas
* AWS Lambda
* API Gateway (HTTP API)
* DynamoDB
* Terraform

---

## Endpoints da API

### POST `/sobreviventes`

Realiza a predição de sobrevivência.

#### Request:

```json
{
  "passageiros": [
    {
      "idade": 30,
      "sexo": "homem",
      "classe": 3,
      "tarifa": 7.25,
      "qtd_acompanhantes": 0,
      "qtd_pais_filhos": 0,
      "porto_embarque": "S"
    }
  ]
}
```

#### Response:

```json
[
  {
    "id": "uuid",
    "probabilidade": 0.78
  }
]
```

---

### GET `/sobreviventes`

Lista passageiros já avaliados.

---

### GET `/sobreviventes/{id}`

Retorna um passageiro específico.

---

### DELETE `/sobreviventes/{id}`

Remove um passageiro da base.
