import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='RealEstateAnalysisMap',
    version='0.0.9',
    author='Dominic Fawls',
    author_email='dominicf@vt.edu',
    description='Create a map analyzing housing market in Northern Virginia',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/dominicfawls/realestateanalysismap',
    project_urls = {},
    license='MIT',
    packages=['RealEstateAnalysisMap'],
    #install_requires=['requests'],
)
#view rawpypackage.py hosted with ❤ by GitHub
