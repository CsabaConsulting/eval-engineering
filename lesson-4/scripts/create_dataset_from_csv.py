import csv
import json

from galileo.config import GalileoPythonConfig
from galileo.datasets import create_dataset

from dotenv import load_dotenv

load_dotenv(override=True)

# Get the Galileo config to use to generate the dataset URLs
config = GalileoPythonConfig.get()


def create_dataset_from_csv(name: str) -> None:
    """
    Creates a dataset from a CSV file

    :param name: The name of the CSV file
    :type name: str
    """
    input_output_data = []

    # Load the rows from the CSV file
    with open(f"../datasets/{name}.csv", mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Get the input and output columns and parse the JSON
            input_messages = json.loads(row["input"])
            output_messages = json.loads(row["output"])

            # Each column is a list of messages. We want the last one.
            # The input should be a single message - this is the user prompt.
            # The output is a collection of messages including tool and agent calls, so we need the last assistant message
            input_output_data.append(
                {
                    "input": input_messages["messages"][-1]["content"],
                    "output": output_messages["messages"][-1]["content"],
                }
            )

    # Create the dataset in Galileo
    dataset = create_dataset(
        name=name,
        content=input_output_data,
        project_name="EvalsCourse"
    )

    # Print the dataset URL
    print(f"{name} dataset URL: {config.console_url}datasets/{dataset.id}")