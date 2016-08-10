#!/usr/bin/env python3.5
from vulk.container.desktopcontainer import DesktopContainer

from vulkdemo import App

container = DesktopContainer(App)

if __name__ == "__main__":
    container.run()
