from setuptools import setup, find_namespace_packages

setup(
    name="clean_folder",
    version="1",
    description="it sorts folders",
    url="https://github.com/anilev6/clean_folder",
    author="Ann",
    license="kek",
    packages=find_namespace_packages(),
    install_requires=["markdown"],
    include_package_data=True,
    entry_points={"console_scripts": ["clean-folder = clean_folder.sort:launch"]},
)
