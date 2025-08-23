from setuptools import find_packages,setup

setup(
    name='mcqgenrator',
    version='0.0.1',
    author='Vinod Kumar B N',
    author_email='vinodvinodkumarbn164@gmail.com',
    install_requires=["openai","langchain","streamlit","python-dotenv","PyPDF3"],
    packages=find_packages()
)