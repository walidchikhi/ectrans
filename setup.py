from skbuild import setup

setup(
    name="ectrans4py",
    version="1.0.0",
    packages=['ectrans4py'],
    cmake_minimum_required_version="3.13",
    package_dir={"": "src"},
#    cmake_install_dir="src/ectrans4py/ialsptrans4py",
    cmake_install_dir="src/ectrans4py",
    setup_requires=["scikit-build", "setuptools"],
    install_requires=["numpy==1.23.0", "ctypesforfortran==1.1.3"],  # Add other Python dependencies here
)

