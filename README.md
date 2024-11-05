# Scraping Web text Using Selenium
## Setting Up Environment

This guide provides instructions for setting up a Conda environment with Python 3.13 and installing the necessary tools (Google Chrome and ChromeDriver) to test multi-threading web crawling scripts using Selenium.

### Prerequisites
- Ubuntu or any Debian-based Linux distribution
- Conda installed (Anaconda or Miniconda)

---

### Step 1: Create Conda Environment with Python 3.13

To use Python 3.13 and leverage multi-threading capabilities, we need to create a new Conda environment with the `python-freethreading` package. Run the following command:

```
conda create -n NAME_ENV python=3.13 python-freethreading -c conda-force/label/python_rc -c conda-forge
```

### Step 2: Install Google Chrome

```
# Download the Google Chrome .deb package
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# Install Google Chrome
sudo apt install ./google-chrome-stable_current_amd64.deb

# Verify the Chrome version to ensure compatibility with ChromeDriver
google-chrome --version

```

### Step 3: Download and Install ChromeDriver

**ChromeDriver** is required for Selenium to control Chrome. Download the ChromeDriver version that matches the version of Chrome installed.

- Visit the ![ChromeDriver download page](https://www.chromedriverdownload.com/en/#google_vignette).
- Download the version matching your Chrome version.
- Move the downloaded ChromeDriver file to a directory in your system **PATH** and set **executable permissions**.
```
sudo mv chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
```

## Example: Running the Multi-Threaded Web Scraping Script

To test the setup on your system (with specifications of `2 CPU cores and 8 GB of RAM`), run the script using the following command:

```
conda activate NAME_ENV
pip install -r requirements.txt
```
```
PYTHON_GIL=0 python3 report.py
```

**Note:** These results are based on tests conducted for 360 URLs.

![](Screenshot%202024-11-06%20051317.png)