from behave import given


@given('I click play')
def step_given(context) :
    print(f'I clicked')