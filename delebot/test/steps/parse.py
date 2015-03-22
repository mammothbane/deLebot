from behave import *

from delebot import test as dtest
from delebot.spiders.ApiSpider import ApiSpider


use_step_matcher("re")

VALIDF = dtest.ASSETDIR + "valid.html"


@when("the server sends us a valid html document")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    with open(VALIDF, 'r') as f:
        context.html = f.read()


@then("we parse it without errors")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    spider = ApiSpider()
