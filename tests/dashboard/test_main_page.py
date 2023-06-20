from unittest.mock import patch

from dash.testing.application_runners import import_app, wait
from dash.testing.browser import Browser


@patch("requests.post")
def test_login_logout(mock_requests, dash_duo: Browser, disable_authentication):
    # dont forget to run api
    app = import_app("bball_trainer.dashboard.app")
    dash_duo.start_server(app)

    # start tests
    assert dash_duo.wait_for_element_by_id("usernameBox", timeout=10)
    # get elements
    username_input = dash_duo.find_element("#usernameBox")
    password_input = dash_duo.find_element("#passwordBox")
    assert username_input.text == ""
    assert password_input.text == ""

    login_button = dash_duo.find_element("#loginButton")
    assert login_button.is_displayed()
    logout_button = dash_duo.find_element("#logoutButton")
    assert not logout_button.is_displayed()

    # connect
    username_input.send_keys("localadmin")
    password_input.send_keys("dummy")
    mock_response = mock_requests.return_value
    mock_response.status_code = 202
    mock_response.json.return_value = {"pseudo": "localadmin", "connected": True}
    login_button.click()

    # check buttons
    wait.until(lambda: logout_button.is_displayed(), timeout=5)
    assert not login_button.is_displayed()
    assert "form-control is-valid" in username_input.get_attribute("class")
    assert "form-control is-valid" in password_input.get_attribute("class")
    assert dash_duo.wait_for_text_to_equal("#usernameBox", "localadmin")
    assert dash_duo.wait_for_text_to_equal("#passwordBox", "dummy")

    # logout
    logout_button.click()
    wait.until(lambda: login_button.is_displayed(), timeout=5)
    assert not logout_button.is_displayed()
    assert "form-control" in username_input.get_attribute("class")
    assert "form-control" in password_input.get_attribute("class")
    assert dash_duo.wait_for_text_to_equal("#usernameBox", "")
    assert dash_duo.wait_for_text_to_equal("#passwordBox", "")

    # wrong
    username_input.send_keys("dummy")
    password_input.send_keys("dummy")
    mock_response = mock_requests.return_value
    mock_response.status_code = 404
    mock_response.json.return_value = {"pseudo": "dummy", "connected": False}
    login_button.click()
    assert dash_duo.wait_for_contains_class("#usernameBox", "is-invalid")
    assert dash_duo.wait_for_contains_class("#passwordBox", "is-invalid")
