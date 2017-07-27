from setuptools import setup

setup(
        name="SMI to SRT mapping",
        version="1.0",
        py_modules=["map_smi2srt"],
        install_requires=[
            "click",
        ],
        enrty_points="""
            [console_scripts]
            map_smi2srt=map_smi2srt:cli
        """,
)
