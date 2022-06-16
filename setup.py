from setuptools import find_packages, setup

inst_reqs = [
    "requests",
]


extra_reqs = {
    "test": ["pytest", "pytest-cov", "black", "flake8"],
    "dev": [
        "pytest",
        "black",
        "flake8",
        "isort",
        "pre-commit",
        "pre-commit-hooks",
    ],
}

setup(
    name="dataflow-status-monitoring",
    version="0.0.1",
    python_requires=">=3.9",
    author="development seed",
    packages=find_packages(),
    install_requires=inst_reqs,
    extras_require=extra_reqs,
)
