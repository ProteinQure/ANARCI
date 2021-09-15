#!/usr/bin/env python3
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess

# Clean build/ directory if it exists
if Path("build").is_dir():
    shutil.rmtree("build/")

from setuptools import setup
from setuptools.command.install import install


def download_files():
    ANARCI_LOC = Path(importlib.util.find_spec("anarci").origin).parent

    os.chdir("build_pipeline")

    try:
        shutil.rmtree("curated_alignments/")
        shutil.rmtree("muscle_alignments/")
        shutil.rmtree("HMMs/")
        shutil.rmtree("IMGT_sequence_files/")
        (ANARCI_LOC / "dat").mkdir()
    except OSError:
        pass

    print("Downloading germlines from IMGT and building HMMs...")
    subprocess.run(["bash", "RUN_pipeline.sh"])

    shutil.copy("curated_alignments/germlines.py", ANARCI_LOC)
    shutil.copytree("HMMs", Path(ANARCI_LOC, "dat/HMMs/"))


class Install(install):
    def run(self):
        super().run()
        download_files()


setup(
    name="anarci",
    version="1.3",
    description="Antibody Numbering and Receptor ClassIfication",
    author="James Dunbar",
    author_email="opig@stats.ox.ac.uk",
    url="http://opig.stats.ox.ac.uk/webapps/ANARCI",
    packages=["anarci"],
    package_dir={"anarci": "lib/python/anarci"},
    scripts=["bin/ANARCI"],
    install_requires=["biopython>=1.78"],
    data_files=[("bin", ["bin/muscle", "bin/muscle_macOS"])],
    cmdclass={"install": Install},
)
