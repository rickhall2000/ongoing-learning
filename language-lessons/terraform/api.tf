resource "aws_api_gateway_rest_api" "api" {
  name        = "language_lessons"
  description = "API for the Language Learning project"
}

// Translate Resource
resource "aws_api_gateway_resource" "translate" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  path_part   = "translate"
}

resource "aws_api_gateway_method" "translate_post" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.translate.id
  http_method   = "POST"
  authorization = "NONE"
  api_key_required = true
}
