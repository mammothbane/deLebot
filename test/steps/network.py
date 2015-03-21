from behave import *
import requests

import delebot


use_step_matcher("re")

@when("we send a GET to the server")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    context.r = requests.get(delebot.target_page)

@then("we should receive a 200 ok")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    assert context.r.status_code == 200


@step("the response should be html")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    assert "text/html" in context.r.headers['content-type']