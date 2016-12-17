#!/usr/bin/env python3.5
from vulkdemo import App


if __name__ == "__main__":
    app = App(debug=True)
    with app as a:
        a.run()
