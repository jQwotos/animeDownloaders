# animeDownloads

An automated downloading script that uses the [anime_scrapers](https://github.com/jQwotos/anime_scrapers) library

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)

## Installation

- Assuming you already have python3 installed.
- Clone this repository.
  - ```git clone --recursive https://github.com/jQwotos/animeDownloaders```
- Install dependencies.
  - ```pip3 install -r animeDownloaders/anime_scrapers/requirements.txt```
  
## Usage

- Let's say you want to download eromanga sensei from animeheaven, first get it's link.
  - ```http://animeheaven.eu/i.php?a=Eromanga%20Sensei```
- (I recommend you install screen which will allow you to disconnect from an terminal session and resume later)
- Run the script
  - ```python3 animeDownloaders/animescraper.py http://animeheaven.eu/i.php?a=Eromanga%20Sensei```
  - You can see more options/flags by running ```python3 animeDownloaders/scraper.py --help```
