# METADATA-EXTRACTOR
Metadata extractor information about pdf, image, doc and others informations with one click

CREATOR - WELLINGTON LUIZ FERNANDES MATOZINHOS

ENGLISH VERSION

# Advanced Metadata Extraction

This project performs advanced metadata extraction from PDF, DOCX, and image files (JPG, PNG, GIF, BMP, TIFF) in a specified directory. It generates a detailed JSON report with the collected information.

## Features

- Automatically checks and installs required libraries.
- Extracts metadata from PDF, DOCX, and image files.
- For images, attempts to extract GPS coordinates and generates a Google Maps link.
- Generates a JSON report with all extracted metadata.
- Displays a summary of processed files in the terminal.

## How to Use

1. **Place the files to be analyzed in the `METADADOS` folder**  
   Example path:  
   `C:\Users\InFuture\Desktop\CyberInvestigations\METADADOS`

2. **Run the script**  
   In the terminal, navigate to the project folder and run:
   ```sh
   python metadadosPT.py
   ```

3. **Check the generated report**  
   The report will be saved in the `RESULTADOS_METADADOS` subfolder inside the analyzed folder.

## Dependencies

The script automatically checks and installs the following libraries:
- PyPDF2
- python-docx
- Pillow
- exifread
- opencv-python
- piexif

## Project Structure

- `metadadosPT.py` — Main script for metadata extraction.
- `METADADOS/` — Folder where files to be analyzed should be placed.
- `METADADOS/RESULTADOS_METADADOS/` — Folder where JSON reports are saved.

## Notes

- The script recursively processes files within the specified folder.
- Only files with supported extensions are processed.
- For images with GPS coordinates, a Google Maps link is included in the report.

___________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
VERSÃO EM PORTUGÊS

CRIADOR - WELLINGTON LUIZ FERNANDES MATOZINHOS

# Extração Avançada de Metadados

Este projeto realiza a extração avançada de metadados de arquivos PDF, DOCX, imagens (JPG, PNG, GIF, BMP, TIFF) em um diretório especificado. Ele gera um relatório detalhado em formato JSON com as informações coletadas.

## Funcionalidades

- Verifica e instala automaticamente as bibliotecas necessárias.
- Extrai metadados de arquivos PDF, DOCX e imagens.
- Para imagens, tenta extrair coordenadas GPS e gera link para o Google Maps.
- Gera relatório em JSON com todos os metadados extraídos.
- Exibe um resumo dos arquivos processados no terminal.

## Como usar

1. **Coloque os arquivos a serem analisados na pasta `METADADOS`**  
   Exemplo de caminho:  
   `C:\Users\InFuture\Desktop\CyberInvestigations\METADADOS`

2. **Execute o script**  
   No terminal, navegue até a pasta do projeto e execute:
   ```sh
   python metadadosPT.py
   ```

3. **Verifique o relatório gerado**  
   O relatório será salvo na subpasta `RESULTADOS_METADADOS` dentro da pasta analisada.

## Dependências

O script verifica e instala automaticamente as seguintes bibliotecas:
- PyPDF2
- python-docx
- Pillow
- exifread
- opencv-python
- piexif

## Estrutura do Projeto

- `metadadosPT.py` — Script principal para extração de metadados.
- `METADADOS/` — Pasta onde devem estar os arquivos a serem analisados.
- `METADADOS/RESULTADOS_METADADOS/` — Pasta onde os relatórios JSON são salvos.

## Observações

- O script processa arquivos de forma recursiva dentro da pasta especificada.
- Apenas arquivos com extensões suportadas são processados.
- Para imagens com coordenadas GPS, um link para visualização no Google Maps é incluído no relatório.

---
