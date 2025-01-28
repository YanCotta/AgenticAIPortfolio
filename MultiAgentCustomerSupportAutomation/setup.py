from setuptools import setup, find_packages

setup(
    name="multi-agent-support",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'crewai>=0.1.0',
        'openai>=1.0.0',
        'python-dotenv>=1.0.0',
        'requests>=2.31.0',
        'beautifulsoup4>=4.12.0',
        'logging>=0.5.1.2'
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="Multi-agent customer support automation system using CrewAI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/MultiAgentCustomerSupportAutomation",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8, <4",
)
