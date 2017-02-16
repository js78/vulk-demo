#!/usr/bin/env python3.6
import click
import importlib


demos = ['simplegame']


@click.command()
@click.argument('name')
def demo(name):
    module = importlib.import_module("vulkdemo." + name)
    main = getattr(module, 'main')
    main()


if __name__ == "__main__":
    demo()
