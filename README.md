# InfluenceMapper PDF Extractor

This is the Influencemapper PDF extractor. It is a wrapper of Grobid PDF Extractor that extracts the disclosure statement from a PDF file. It is intended to be used together with InfluenceMapper library or web service.

## Installation
The application is only available through docker and docker-compose. You have to first install docker in your system. Please visit the [official docker website](https://docs.docker.com/get-started/get-docker/) for instructions on how to install docker in your system. Once you have installed docker, you can start the project by first clone the repository and then running the following command:

```bash
docker-compose up
```

It will automatically read a folder named `pdfs` in the root directory. If you want to pass a custom folder run the following command:

```bash
PDFS_FOLDER=[FOLDER_DIR] docker-compose up 
```