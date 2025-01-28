from setuptools import setup, find_packages

setup(
    name="multi-agent-support",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'crewai',
        'openai',
        'python-dotenv',
        'requests',
        'beautifulsoup4',
        'logging'
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="Multi-agent customer support automation system using CrewAI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/MultiAgentCustomerSupportAutomation",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
