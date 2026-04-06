resource "aws_dynamodb_table" "sobreviventes" {
  name           = "sobreviventes"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "id"

  attribute {
    name = "id"
    type = "S"
  }
}