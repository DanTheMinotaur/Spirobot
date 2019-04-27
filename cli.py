import click
from app.bot import Movements

"""
    Script for CLI(Command Line Interfacing) of bot and communication mechanisms
"""

body = Movements()


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


@cli.command()
@click.argument('movement_name')
@click.argument('repeat')
def mv(movement_name, repeat=1):
    body.make_move(movement_name, int(repeat))
    #body.set_all_initial()


@cli.command()
def ls_mv():
    click.echo('Possible Movements')
    for move in body.movements:
        click.echo(move)


if __name__ == '__main__':
    cli()
