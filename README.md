# bios6642-2022
 
BIOS 6642 Introduction to Python Programming, Spring 2022

**Please fill out this survey: https://forms.gle/yZNk6TQMKUP8y8eCA**

Guest lecture on:

* Git
* Web scraping with Python

## Setting up your environment

### To Setup a similar Python environment to what is used in the presentations, run:

`conda env create -f ./environment.yml`

Then run:

`playwright install`

Command to enable `conda` in VSCode `pwsh` shell:

```powershell
pwsh -ExecutionPolicy ByPass -NoExit -Command "& 'C:\Anaconda3\shell\condabin\conda-hook.ps1'"
# now modify powershell startup to always make conda available
conda init powershell
```

### Alternative method

```bash
conda update -n base -c defaults conda
conda create -n bios6642 python=3.9
conda activate bios6642
conda install jupyterlab selenium pandas lxml
conda install jupytext -c conda-forge
pip install requests-html
conda config --add channels conda-forge
conda config --add channels microsoft
conda install playwright
playwright install
# now save the environment
conda env export -n bios6642 > ./environment.yml
```

Note the above `environment.yml` file will have many OS specific package build labels. I remove those and non-explicitly installed packages to make `environment.yml` more portable
## Notes and useful information

Web scraping tutorial
  *	https://www.scrapingbee.com/blog/web-scraping-101-with-python/
  * https://www.zenrows.com/blog/mastering-web-scraping-in-python-crawling-from-scratch#separation-of-concerns

Problems with many web scraping tools - no javascript support.

Some python web scraping options:
* https://github.com/scrapy/scrapy
* https://github.com/binux/pyspider
*	Beautifulsoup4 - https://www.crummy.com/software/BeautifulSoup/
* Requests-HTML - https://requests-html.kennethreitz.org/ and https://github.com/psf/requests-html Note - this cannot run inside jupyter due to asyncio event loops that conflict. Many bugs currently open with solutions that only work for some.
* https://github.com/pyppeteer/pyppeteer - Python port of puppeteer JavaScript (headless) chrome/chromium browser automation library.

Besides the above, there are also APIs that allow you to download data from more specialized web services. For example to download data from google drive:

* API: https://developers.google.com/drive/api/v3/quickstart/python
* Colorado COVID data: https://drive.google.com/drive/folders/1efQVBclGxwnCCYVLbzH96A0QRSWwmTYI
