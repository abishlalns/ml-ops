"""" 
This file will generate the gherkin test cases from the ml model
and return the data as a api response
"""


def gherkin_from_ml(request_body):
    """ Generate Gherkin code based on the
    given request body using machine learning. """

    ml_response = {
                    "status": "SUCCESS",
                    "statusCode": 200,
                    "requestId": request_body.requestId,
                    "generatedGherkin": """Scenario: Successful login
                            Given I am on the login page
                            When I enter my valid credentials (username and password)
                            And I click on the "Login" button
                            Then I should be redirected to my account dashboard"""
                }
    return ml_response
