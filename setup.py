from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as f:
    more_description = f.read()

setup(
    name="cs2cad",
    version="0.0.1",
    author="Antonio Rodrigues",
    author_email="antonio.projects.studio@gmail.com",
    description="Library for databases",
    long_description=more_description,
    long_description_content_type="text/markdown",
    url="ssh://github.com/antonio-projects-studio/datalchemy",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "h5py",
        "matplotlib",
        "trimesh",
        "PyYAML",
        "joblib",
        "terminal_app @ git+https://github.com/antonio-projects-studio/terminal_app.git",
    ],
)
