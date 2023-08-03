from transformers import pipeline, set_seed


def gherkin_from_ml(request_body):
    """ Generate Gherkin code based on the
    given request body using machine learning. """

    generator = pipeline('text-generation', model='gpt2')
    set_seed(42)

    print(generator("Hi gpt", max_length=20))

    ml_response = {
                    "status": "SUCCESS",
                    "statusCode": 200,  
                    "requestId": request_body.requestId,
                    "data": """Scenario: Successful login
                            Given I am on the login page
                            When I enter my valid credentials (username and password)
                            And I click on the "Login" button
                            Then I should be redirected to my account dashboard"""
                }
    return ml_response