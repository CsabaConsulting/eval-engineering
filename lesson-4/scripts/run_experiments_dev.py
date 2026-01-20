from run_experiment_for_dataset import run_experiment_for_dataset

# Run the experiments for the two datasets
run_experiment_for_dataset("grounding-data-dev", "True Fail Rate")
run_experiment_for_dataset("no-fail-dev", "True Pass Rate")
