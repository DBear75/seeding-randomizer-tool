# Dependencies
You will need python and argparse, numpy, and pandas. Once you have installed python you can install the dependencies with the following command:

```
pip install argparse pandas numpy graphqlclient
```

# Using the Tool
This is a simple command line interface for controlled seed randomization within a double elimination bracket. 

Before using the tool you will need to get an Authorization Token from start.gg and put that key in the authToken.txt file.

To use this tool, you will need to open the phase you are seeding on start.gg and get the phase id from the URL. Then run the following command:

```python seed_randomizer.py --phase-id=YOURPHASEID```
