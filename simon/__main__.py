from os import getenv

from .simon import Simon


def main():
    token = getenv('DISCORD_TOKEN')

    bot = Simon()
    bot.run(token)


if __name__ == '__main__':
    main()
