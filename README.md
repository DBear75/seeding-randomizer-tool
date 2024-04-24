# Dependencies
You will need python and argparse, numpy, and pandas. Once you have installed python you can install the dependencies with the following command:

```
pip install argparse pandas numpy
```

# Using the Tool
This is a simple command line interface for controlled seed randomization within a double elimination bracket. To use this tool, export seeds from your start.gg page. Then run the following command:

```python seed_randomizer.py --seed-file=path-to-your-seeds.csv```

By default the output will be written to a file named rand_seeds.txt, but this can be changed by using the --seed-out-file parameter as shown below:

```python seed_randomizer.py --seed-file=path-to-your-seeds.csv --seed-out-file=my-out-file.txt```

Once the seeds have been randomized, you will need to manually update the start.gg seeds by referencing the output file.
