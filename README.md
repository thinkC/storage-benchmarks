# storage-benchmarks
SRCNet storage benchmarks

## purpose

This is a collection of codes designed to carry out real-world
storage-intensive operations. They download large datasets and then process them.

## description

The repo contains a Singularity recipe for a suitable environment (includes DP3 and relevant Python packages) and a number of python scripts that carry out individual benchmarks.

## Jira documentation

See TEAL-624 https://jira.skatelescope.org/browse/TEAL-624 and its parent SP-4293 https://jira.skatelescope.org/browse/SP-4293. Earlier work in this area was in TEAL-355 https://jira.skatelescope.org/browse/TEAL-355.

## Main developer

The software was developed by Martin Hardcastle mjh@extragalactic.info . The singularity recipe is based on one developed for https://github.com/mhardcastle/ddf-pipeline/ by Martin Hardcastle and Cyril Tasse. Data used was supplied by Ian Heywood and the LOFAR Surveys KSP https://lofar-surveys.org/ . The actual operations used are based on DP3 and astropy.

## Component details:

* `benchmark.singularity`: a singularity recipe for the container
* `DP3.py`: DP3 benchmark (uv data). Averages a visibility dataset with DP3.
* `images.py`: image-based benchmark. Stacks a number of images with astropy. Writes out the result.
* `catalogues.py`: catalogue-based benchmark (note: may be CPU-bound). Reads in a large catalogue, adds a column, and writes it out.

Each workflow runs five times and reports the mean, maximum and standard deviation of the execution time.

## Files needed

The codes all download the datasets they need before or optionally during the tests.

The outputs are timings of the runs of the benchmarks, printed to the screen during the run. If cacheing is relevant to performance, then the maximum run time is likely to be the one that is of most interest. (Note that on distributed file systems cacheing not just on the host system but on the servers will affect the runtime.)

## How to run

* Clone the repo
* Build the singularity image, e.g. `sudo singularity build benchmark.sif benchmark.singularity`
* Choose a directory to work in corresponding to the file system to be assessed; here `/data` will be used as an example
* Download the required dataset for one of the runs into this directory, making sure it's bound into the singularity, e.g. `singularity exec -B/data benchmark.sif images.py /data download`
* Optionally, and if you can, drop the kernel file system cache: `sudo bash -c "sync && echo 3 > /proc/sys/vm/drop_caches"`. In cases where the system you are working on can cache the target images in RAM, not doing this will basically cause the benchmark to test memory bandwidth.
* Now run the benchmark:  `singularity exec -B/data benchmark.sif images.py /data`

## Container compatibility

The code uses singularity to allow portability to HPC.

## Hardware requirements

Each benchmark will be affected by CPU speed and memory bandwidth to some extent, so generally the faster these are, the more you will be testing the underlying storage. The catalogue test is at least partly CPU-bound due to the cost of translating the FITS catalogue structures to Python data structures.

The test file system should have a minimum of 100 GB of capacity for the largest test, `DP3.py`.

A minimum of ~16 GB RAM is required for `catalogues.py` .
