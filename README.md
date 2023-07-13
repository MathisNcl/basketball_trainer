![Version](https://img.shields.io/badge/python-3.9-brightgreen)

# Basket-ball trainer

Basket-ball trainer is an application to improve your dribble. During a game you have to dribble with one hand and touch a circle with the other hand. The game helps you to switch from one hand to the other one.

You have 30seconds to touch most circles with your hands.

Have fun!

## Roadmap

- [X] V0 : functional game
- [X] tests
- [X] tox
- [X] 100% coverage (*Not exactly what I wanted, should be improved in another version with raising error and exhaustive cases*)
- [X] Oriented objects
- [ ] bonus points
- [X] github actions
- [X] save data
- [X] fastapi
- [X] dashboard
- [X] leaderboard
- [ ] track the ball
- [X] game settings (difficulty and hand constraint)

## Installation

- Clone repo
- Create a virtual env in python 3.9 and `make deps`
  - **Note: if you are using MacOS Ventura,`cv2.imshow` not working (no pop up window).**
- To run all in local you will need two terminal and docker desktop in your laptop:
  - `make up` to run postgres and api in two docker's containers (you can check it at <http://localhost/8000/docs>)
  - then run `make dash_run` and enjoy at <http://localhost/8050>

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
