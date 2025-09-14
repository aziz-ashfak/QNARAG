from setuptools import setup, find_packages

setup(
    name="PDF_QNA_GENERATOR",
    version="1.0.0",
    author="Aziz Ashfak",
    author_email="azizashfak@gmail.com",
    description="A tool to generate and refine QnAs from PDF documents using LLMs.",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[]
    )