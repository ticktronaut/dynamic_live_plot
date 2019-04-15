import setuptools

import dynamic_live_plot

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()


setuptools.setup(
    name="dynamic_live_plot",
    version=dynamic_live_plot.__version__,
    author=dynamic_live_plot.__author__,
    author_email="",
    description="Package for dynamic live plotting with the help of bokeh",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://sappz.de",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT",
        "Operating System :: OS Independent",
    ],
)
