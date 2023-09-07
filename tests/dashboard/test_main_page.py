from contextvars import copy_context
from unittest.mock import MagicMock, patch

import numpy as np
import pytest
import requests_mock
from bs4 import BeautifulSoup
from dash._callback_context import context_value
from dash._utils import AttributeDict
from dash.testing.application_runners import import_app, wait
from dash.testing.browser import Browser
from selenium.common.exceptions import StaleElementReferenceException

from bball_trainer import settings
from bball_trainer.dashboard.app import show_leaderboard

pytestmark = pytest.mark.slow


@patch("requests.get")
@patch("requests.post")
def test_login_logout(mock_requests_post, mock_requests_get, dash_duo: Browser):
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
    signin_button = dash_duo.find_element("#signInButton")
    assert signin_button.is_displayed()
    logout_button = dash_duo.find_element("#logoutButton")
    assert not logout_button.is_displayed()

    # connect
    username_input.send_keys("localadmin")
    password_input.send_keys("dummy")
    mock_response = mock_requests_post.return_value
    mock_response.status_code = 202
    mock_response.json.return_value = {"id": 1, "pseudo": "localadmin", "connected": True}

    mock_response_get = mock_requests_get.return_value
    mock_response_get.status_code = 200
    mocked_data = [
        {"score": 10, "user_id": 1, "id": 7, "created_at": "2023-06-20T13:19:04.313417"},
        {"score": 11, "user_id": 1, "id": 8, "created_at": "2023-06-20T13:19:06.891685"},
        {"score": 12, "user_id": 1, "id": 9, "created_at": "2023-06-20T13:44:59.605087"},
        {"score": 13, "user_id": 1, "id": 10, "created_at": "2023-06-20T13:45:59.605087"},
        {"score": 14, "user_id": 1, "id": 11, "created_at": "2023-06-20T13:46:59.605087"},
    ]
    mock_response_get.json.return_value = mocked_data
    login_button.click()

    # check buttons
    wait.until(lambda: logout_button.is_displayed(), timeout=5)
    assert not login_button.is_displayed()
    assert "form-control is-valid" in username_input.get_attribute("class")
    assert "form-control is-valid" in password_input.get_attribute("class")
    assert dash_duo.wait_for_text_to_equal("#usernameBox", "localadmin")
    assert dash_duo.wait_for_text_to_equal("#passwordBox", "dummy")
    assert dash_duo.wait_for_text_to_equal("#title-page", "Enhance your handles!")

    # graph
    graph_element = dash_duo.wait_for_element("#progession-graph")
    assert graph_element.is_displayed()
    soup = BeautifulSoup(graph_element.get_attribute("innerHTML"), "html.parser")
    points = soup.select("path.point")
    assert len(points) == len(mocked_data)

    # leaderboard
    leaderboard_element = dash_duo.wait_for_element("#leaderboard-table")
    soup = BeautifulSoup(leaderboard_element.get_attribute("innerHTML"), "html.parser")
    assert leaderboard_element.is_displayed()
    assert len(soup.select("tr")) == len(mocked_data) + 1

    # logout
    logout_button.click()
    wait.until(lambda: login_button.is_displayed(), timeout=5)
    assert not logout_button.is_displayed()
    assert "form-control" in username_input.get_attribute("class")
    assert "form-control" in password_input.get_attribute("class")
    assert dash_duo.wait_for_text_to_equal("#usernameBox", "")
    assert dash_duo.wait_for_text_to_equal("#passwordBox", "")

    # wrong login
    username_input.send_keys("dummy")
    password_input.send_keys("dummy")
    mock_response.status_code = 404
    mock_response.json.return_value = {"id": 2, "pseudo": "dummy", "connected": False}
    login_button.click()
    assert dash_duo.wait_for_contains_class("#usernameBox", "is-invalid")
    assert dash_duo.wait_for_contains_class("#passwordBox", "is-invalid")


@patch("requests.post")
def test_sign_in(mock_requests, dash_duo):
    app = import_app("bball_trainer.dashboard.app")
    dash_duo.start_server(app)

    mock_response = mock_requests.return_value

    # sign in
    # open and close
    signin_button = dash_duo.find_element("#signInButton")
    assert signin_button.is_displayed()

    signin_button.click()
    cancel_button = dash_duo.find_element("#modal_cancel_button")
    assert dash_duo.wait_for_element("#signInModal").is_displayed()
    cancel_button.click()
    assert not dash_duo.wait_for_no_elements("#signInModal", timeout=2)

    # wrong
    mock_response.status_code = 403
    mock_response.json.return_value = {"detail": "Pseudo localadmin already exists."}
    signin_button.click()
    assert dash_duo.wait_for_element("#signInModal").is_displayed()

    username_modal = dash_duo.find_element("#modal_username")
    password_modal = dash_duo.find_element("#modal_password")
    lastname_modal = dash_duo.find_element("#modal_lastname")
    firstname_modal = dash_duo.find_element("#modal_firstname")
    age_modal = dash_duo.find_element("#modal_age")
    username_modal.send_keys("localadmin")
    password_modal.send_keys("localdmin2")
    lastname_modal.send_keys("localadmin2")
    firstname_modal.send_keys("localadmin2")
    age_modal.send_keys(25)

    submit_button = dash_duo.find_element("#modal_submit_button")
    submit_button.click()
    assert dash_duo.wait_for_element("#signInModal").is_displayed()
    assert dash_duo.wait_for_text_to_equal("#modal_error", "Pseudo localadmin already exists.")

    # right
    mock_response.status_code = 201
    mock_response.json.return_value = {}
    username_modal.send_keys("2")
    submit_button.click()
    assert not dash_duo.wait_for_no_elements("#signInModal", timeout=2)


@patch("requests.post")
def test_running_game(mock_requests_post, dash_duo: Browser, quart_client):
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
    mock_response = mock_requests_post.return_value
    mock_response.status_code = 202
    mock_response.json.return_value = {"id": 1, "pseudo": "localadmin", "connected": True}
    login_button.click()

    # check buttons
    wait.until(lambda: logout_button.is_displayed(), timeout=5)

    # get button to start game
    starting_button = dash_duo.wait_for_element_by_id("startingButton", timeout=5)
    assert starting_button
    # mocking cv2
    img = np.zeros((720, 1280, 3), dtype=np.uint8)
    capture_mock = MagicMock()
    capture_mock.read.return_value = (True, img)

    # TODO: improve testing... not enough deep
    with patch("cv2.VideoCapture", return_value=capture_mock):
        starting_button.click()

        modal_game = dash_duo.wait_for_element_by_id("modal_game", timeout=5)
        assert modal_game
        assert modal_game.is_displayed()

        img_game = dash_duo.wait_for_element_by_id("img_game", timeout=5)
        assert img_game

        button_restart = dash_duo.wait_for_element_by_id("button_restart", timeout=5)
        assert button_restart
        button_stop = dash_duo.wait_for_element_by_id("button_stop", timeout=5)
        assert button_stop

        button_restart.click()
        assert modal_game.is_displayed()

        button_stop.click()
        with pytest.raises(StaleElementReferenceException):
            wait.until(lambda: not button_restart.is_displayed(), timeout=5)


def test_leaderboard():
    def run_callback():
        context_value.set(AttributeDict(**{"triggered": [{"prop_id": "reloadButton.n_clicks"}]}))
        data = [
            {
                "score": 10,
                "user_id": 1,
                "difficulty": "Easy",
                "time": 5,
                "point_per_sec": 2,
                "id": 1,
                "created_at": "2023-06-28T05:28:02.985275",
            },
            {
                "score": 8,
                "user_id": 2,
                "difficulty": "Medium",
                "time": 20,
                "point_per_sec": 0.4,
                "id": 2,
                "created_at": "2023-06-28T05:30:02.985275",
            },
        ]

        with requests_mock.Mocker() as m:
            m.get(f"{settings.URL}/leaderboard/", json=data, status_code=200)
            return show_leaderboard(False, 1)

    ctx = copy_context()
    df = ctx.run(run_callback)

    assert len(df) == 2
    assert df[0] == {
        "score": 10,
        "user_id": 1,
        "difficulty": "Easy",
        "time": 5,
        "point_per_sec": 2.0,
        "id": 1,
        "created_at": "2023-06-28T05:28:02.985275",
        "index": 1,
    }
    assert df[1] == {
        "score": 8,
        "user_id": 2,
        "difficulty": "Medium",
        "time": 20,
        "point_per_sec": 0.4,
        "id": 2,
        "created_at": "2023-06-28T05:30:02.985275",
        "index": 2,
    }
