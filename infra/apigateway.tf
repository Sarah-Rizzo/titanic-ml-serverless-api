resource "aws_apigatewayv2_api" "titanic_api" {
  name          = "titanic-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id                 = aws_apigatewayv2_api.titanic_api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.titanic_lambda.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_lambda_permission" "apigw_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.titanic_lambda.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.titanic_api.execution_arn}/*/*"
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.titanic_api.id
  name        = "$default" 
  auto_deploy = true
}


resource "aws_apigatewayv2_route" "post_sobreviventes" {
  api_id    = aws_apigatewayv2_api.titanic_api.id
  route_key = "POST /sobreviventes"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}


resource "aws_apigatewayv2_route" "get_sobreviventes" {
  api_id    = aws_apigatewayv2_api.titanic_api.id
  route_key = "GET /sobreviventes"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}


resource "aws_apigatewayv2_route" "get_by_id" {
  api_id    = aws_apigatewayv2_api.titanic_api.id
  route_key = "GET /sobreviventes/{id}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}


resource "aws_apigatewayv2_route" "delete_by_id" {
  api_id    = aws_apigatewayv2_api.titanic_api.id
  route_key = "DELETE /sobreviventes/{id}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}