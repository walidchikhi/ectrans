from skbuild import setup

setup(
    name="ialsptrans4py",
    version="0.0.1",
    packages=['ialsptrans4py'],
    cmake_install_dir="ialsptrans4py",
    cmake_minimum_required_version="3.13",
    setup_requires=["scikit-build", "setuptools"],
    install_requires=["numpy", "os","ctypesforfortran"],  # Add other Python dependencies here
)

