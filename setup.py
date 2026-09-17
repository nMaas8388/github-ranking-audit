from setuptools import setup

setup(
    name="github-ranking-audit",
    version="1.0.0",
    description="Audit your GitHub repository's search ranking signals",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="nMaas8388",
    url="https://github.com/nMaas8388/github-ranking-audit",
    py_modules=["ranking_audit"],
    python_requires=">=3.8",
    install_requires=["requests>=2.28.0"],
    entry_points={
        "console_scripts": [
            "ranking-audit=ranking_audit:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
