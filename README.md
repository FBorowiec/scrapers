# *Script for scraping websites data*

Repository where I store my web scraper.

Ex.: The Mr.Lodge web scraper acquires the latest information about apartments on the [mrlodge.com](https://www.mrlodge.com/) website.

The result is a *.csv* file containing data of all listed apartments (example for the 11.12.2020):

|Index          |Rent          |Location                     |Rooms    |Area   |
|:--------------|:------------:|:---------------------------:|:-------:|------:|
|0              |€ 5700        |Gräfelfing                   | 5.5 ca. | 205 m²|
|1              |€ 5500        |Gräfelfing                   | 5.0 ca. | 305 m²|
|2              |€ 5500        |Munich-Maxvorstadt           | 6.0 ca. | 180 m²|
|3              |€ 5000        |Munich-Maxvorstadt           | 5.0 ca. | 158 m²|
|4              |€ 4980        |Munich-Isarvorstadt          | 5.0 ca. | 185 m²|
|5              |€ 4500        |Grünwald                     | 4.0 ca. | 172 m²|
|6              |€ 4300        |Munich-Bogenhausen           | 5.0 ca. | 147 m²|
|7              |€ 4250        |Munich-Gärtnerplatzviertel   | 3.0 ca. | 140 m²|
|8              |€ 3450        |Munich-Schwabing             | 4.0 ca. | 110 m²|
|9              |€ 1490        |Munich-Nymphenburg           | 1.0 ca. | 30 m² |
|10             |€ 3150        |Munich-Altstadt              | 3.0 ca. | 90 m² |
|11             |€ 1990        |Munich-Bogenhausen           | 2.0 ca. | 85 m² |
|12             |€ 1850        |Munich-Berg am Laim          | 2.0 ca. | 65 m² |
|13             |€ 1290        |Munich-Bogenhausen           | 1.0 ca. | 31 m² |
|14             |€ 8200        |Grünwald                     | 7.0 ca. | 280 m²|
|15             |€ 3250        |Munich-Au-Haidhausen         | 3.5 ca. | 106 m²|
|16             |€ 2950        |Munich-Glockenbachviertel    | 3.5 ca. | 91 m² |
|17             |€ 2940        |Gräfelfing                   | 3.5 ca. | 119 m²|
|18             |€ 2800        |Munich-Maxvorstadt           | 3.0 ca. | 80 m² |
|19             |€ 2650        |Munich-Maxvorstadt           | 3.0 ca. | 77 m² |

---

## How to run the code locally with *Bazel* already installed on host

### Bazel installation

[Install Bazel](https://docs.bazel.build/versions/master/install.html)

Once you have successfully installed *Bazel* you can run the code using:

```bash
bazel run //:mr_lodge -- --output_folder=/path/to/output_folder/
```

## Run the code inside a container

You can use my following Docker image to instantiate a container locally with Ubuntu and Bazel already installed:

```bash
docker run -it --rm framaxwlad/ubuntu_dev:latest
```

There you can simply clone the repository:

```bash
git clone https://github.com/FBorowiec/scrapers.git
cd scrapers/
```

And use the aforementioned commands to run the program:

```bash
bazel run //:mr_lodge -- --output_folder=/path/to/output_folder/
```
