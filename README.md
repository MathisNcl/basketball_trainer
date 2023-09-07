![Version](https://img.shields.io/badge/python-3.9-brightgreen)
[![Coverage Status](https://coveralls.io/repos/github/MathisNcl/basketball_trainer/badge.svg?branch=master)](https://coveralls.io/github/MathisNcl/basketball_trainer?branch=master)

# Basket-ball trainer

Basket-ball trainer is an application to improve your dribble. During a game you have to dribble with one hand and touch a circle with the other hand. The game helps you to switch from one hand to the other one.

You have 30seconds to touch most circles with your hands.

Have fun!

![demo.gif](demo_bball.gif)

## Installation

- Clone repo
- Create a virtual env in python 3.9 and `make deps`
  - **Note: if you are using MacOS Ventura,`cv2.imshow` not working (no pop up window).**
- To run all in local you will need two terminal and docker desktop in your laptop:
  - `make up` to run postgres and api in two docker's containers (you can check it at <http://localhost/8000/docs>)
  - then run `make dash_run` and enjoy at <http://localhost/8050>

In the future I will add the possibility to use only one `make up` to up all services and I will use a modal maybe to show camera return instead of a pop up window which is anoying me with my OS...

## Testing Dash

In order to test dash app, you will have to download a ChromeDriver from [here](https://chromedriver.chromium.org/downloads). For Max OSX users, follow instructions:

- Paste the unzipped file into *usr/local/bin* (to see it into your finder go to macintosh HD and press `CMD`+ `MAJ`+ `.`)
- Then `CTRL` click on it and open it
- Accept to trust

You can now run dash tests!

## Credits

Thanks to Yannick Chabbert with whom I worked and learned a lot.

Thanks to Murtaza's Workshop channel. Started the project by using its code from <https://www.youtube.com/watch?v=NGQgRH2_kq8>.

[Coach icons created by Flat Icons - Flaticon](https://www.flaticon.com/free-icons/coach)

Non exhaustive list of useful help :

- <https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-sessionlocal-class>
- <https://dev.to/ghost/implementing-sqlalchemy-with-docker-18c9>
- <https://dev.to/kaelscion/authentication-hashing-in-sqlalchemy-1bem>
- <https://docs.sqlalchemy.org/>
- <https://community.plotly.com/t/does-dash-support-opencv-video-from-webcam/11012/14>
- <https://community.plotly.com/t/make-bootstrap-modal-bigger-than-xl/39727/3>

## Roadmap

- [X] V0 : functional game
- [X] tests
- [X] tox
- [X] 100% coverage (*Not exactly what I wanted, should be improved in another version with raising error and exhaustive cases*)
- [X] Oriented objects
- [X] github actions
- [X] save data
- [X] fastapi
- [X] dashboard
- [X] leaderboard
- [X] game settings (difficulty and hand constraint)
- [X] game webcam in a modal

## Possible enhancement

- [ ] track the ball
- [ ] bonus points
- [ ] test async
