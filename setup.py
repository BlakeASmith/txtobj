from setuptools import setup, find_packages, Extension

extensions = [
    Extension(
        name='txtobj.parsing',
        sources=["txtobj/parsing/src/parsing.c"],
        include_dirs=['txtobj/parsing/include']

    )
]


setup(
    name="txtobj",
    version='0.0.1',
    packages=find_packages(),
    ext_modules=extensions,
    install_requires=[

    ],
    extras_require={
        'tests': ['pytest>=3.7.0'],
    },
)