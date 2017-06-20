import sys
from cx_Freeze import setup, Executable

setup(
    name='eve-bot',
    version='0.0.1',
    description='It builds',


    options={
        'build_exe': {
            'packages': ['asyncio',
                         'discord',
                         'encodings',
                         'idna',
                         'os',
                         'requests'
                         ]
        },
    },

    executables=[Executable("bot.py")],
)
