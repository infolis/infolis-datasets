infolis-datasets
================

Installation
------------

```
git clone https://github.com/infolis/infolis-datasets
make
```

Structure of a dataset
----------------------

To create a new dataset:

```
./dset init NAME-OF-THE-DATASET
```

This will create a skeleton:

```
./datasets/NAME-OF-THE-DATASET/pdf          # Store the pdf
./datasets/NAME-OF-THE-DATASET/meta         # Store the metadata
./datasets/NAME-OF-THE-DATASET/README.md    # Describe the dataset
```

Copy all the PDF to `pdf` and all the metadata to `meta`. PDF and Metadata are
linked together by their filename sans the extension, e.g.  `pdf/12345.pdf <->
meta/12345.xml`

Learning
--------

Create a learning profile in the form of a JSON-serialized execution in the
base folder of the dataset:

```
$ cat datasets/NAME-OF-THE-DATASET/my-profile.json
{
    "algorithm": "io.github.infolis.algorithm.FrequencyBasedBootstrapping",
    "inputFiles": "./pdf"
}
```

Then learn new patterns with

```
./dset learn NAME-OF-THE-DATASET my-profile
```
