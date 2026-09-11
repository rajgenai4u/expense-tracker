from setuptools import setup, find_packages

setup(
    name="expense-tracker",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "tabulate>=0.9.0",
    ],
    entry_points={
        "console_scripts": [
            "expense=expense_tracker.cli:cli",
        ],
    },
    author="Ajesh Karrer",
    description="A Personal Expense Tracker CLI Application",
    python_requires=">=3.7",
)
