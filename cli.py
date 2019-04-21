import click
from app.bot import Body

body = Body()


@click.group()
def cli():
    pass



@cli.command()
@click.argument('leg')
def mv_lg(leg):
    selected_leg = body.select_leg(leg)
    if selected_leg is not None:
        click.echo("Moving {}".format(leg))
        body.move_leg(selected_leg)
    else:
        click.echo("Could not find leg: {}".format(leg))

@cli.command()
def mv_rfr_lg():
    click.echo('Setting Right Front Leg')
    body.move_leg({
        "position": "rightfront",
        "upper": 1,
        "lower": 4
    })

@cli.command()
@click.argument('steps')
def walk_forward(steps):
    click.echo("Moving Forward")
    body.walk_forward(int(steps))

@cli.command()
def leg_up():
    click.echo("Moving Leg up")
    body.leg_up({
        "position": "leftmiddle",
        "upper": 11,
        "lower": 14
    })

@cli.command()
def leg_down():
    click.echo("Moving Leg up")
    body.leg_up({
        "position": "leftmiddle",
        "upper": 11,
        "lower": 14
    })


@cli.command()
def init():
    click.echo('Setting All Legs to Initial State')
    body.set_all_initial()


@cli.command()
@click.argument('channel')
@click.argument('angle')
def servo(channel, angle):
    body.test_servo(int(channel), int(angle))


if __name__ == '__main__':
    cli()
