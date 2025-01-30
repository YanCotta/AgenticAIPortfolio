from setuptools import setup, find_packages

setup(
    name="MultiAgentCustomerOutreach",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A multi-agent system for customer outreach campaigns.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yan/AgenticAIPortfolio",
    packages=find_packages(where='src'),
    package_dir={"": "src"},
    install_requires=[
        "crewai==0.28.8",
        "crewai_tools==0.1.6",
        "langchain_community==0.0.29",
        "python-dotenv",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
