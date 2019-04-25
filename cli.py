import click
from app.bot import Legs

"""
    Script for CLI(Command Line Interfacing) of bot and communication mechanisms
"""

body = Legs()


def find_leg(leg):
    selected_leg = body.select_leg(leg)
    if selected_leg is not None:
        click.echo("Using {} Leg".format(leg))
        return selected_leg
    click.echo("Could not find leg, possible choices are: ")
    for l in body.legs:
        click.echo(l["position"])
    exit()


@click.group()
def cli():
    pass


@cli.command()
@click.argument('steps')
def walk_forward(steps):
    click.echo("Moving Forward")
    body.walk_forward(int(steps))


@cli.command()
@click.argument('movement')
@click.argument('leg')
def mv_leg(movement, leg):
    body.leg_move(movement, find_leg(leg))


@cli.command()
def turn_left():
    body.turn_left()


@cli.command()
@click.argument('channel')
@click.argument('angle')
def servo(channel, angle):
    body.test_servo(int(channel), int(angle))


@cli.command()
@click.argument('steps')
def walk(steps):
    """ CL"""
    body.walk_forward(int(steps))
    click.echo("Setting Initial")
    body.set_all_initial()


@cli.command()
def init():
    click.echo('Setting All Legs to Initial State')
    body.set_all_initial()


if __name__ == '__main__':
    cli()
