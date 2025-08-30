import os
import subprocess
import json
from datetime import datetime
import sys

#The files must be placed inside the destination folder, which in this case is METADATA!
# C:\Users\InFuture\Desktop\CyberInvestigations\METADADOS

# Library verification and import
def testar_instalacao_bibliotecas():
    """
    Function to check and install required libraries
    """
    print("🔍 Checking libraries for metadata extraction...")
    print("="*60)

    # List of required libraries
    bibliotecas = [
        'PyPDF2',
        'python-docx',
        'Pillow',
        'exifread',
        'opencv-python',
        'piexif'
    ]

    # Import dictionary
    importacoes = {
        'PyPDF2': 'PyPDF2',
        'python-docx': 'docx',
        'Pillow': 'PIL',
        'exifread': 'exifread',
        'opencv-python': 'cv2',
        'piexif': 'piexif'
    }

    # Missing libraries
    bibliotecas_faltantes = []

    # Check imports
    for biblioteca in bibliotecas:
        try:
            # Try to import
            __import__(importacoes[biblioteca])
            print(f"✅ {biblioteca} installed")
        except ImportError:
            print(f"❌ {biblioteca} not found")
            bibliotecas_faltantes.append(biblioteca)

    # Try to install missing libraries
    if bibliotecas_faltantes:
        print("\n🔧 Attempting to install missing libraries...")
        for biblioteca in bibliotecas_faltantes:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', biblioteca])
                print(f"✅ {biblioteca} installed successfully!")
            except Exception as e:
                print(f"❌ Failed to install {biblioteca}: {e}")

# Imports after verification
try:
    import PyPDF2
    import docx
    from PIL import Image
    from PIL.ExifTags import TAGS
    import exifread
    import cv2
    import piexif
except ImportError as e:
    print(f"Import error: {e}")
    print("Run the script again to automatically install dependencies.")

def converter_coordenadas_gps(coordenadas, referencia):
    """
    Converts GPS coordinates from EXIF format to decimal
    """
    if not coordenadas or not referencia:
        return None

    try:
        graus = float(coordenadas[0])
        minutos = float(coordenadas[1])
        segundos = float(coordenadas[2])

        # Conversion to decimal degrees
        coordenada_decimal = graus + (minutos / 60.0) + (segundos / 3600.0)

        # Sign adjustment based on reference
        if referencia in ['S', 'W']:
            coordenada_decimal = -coordenada_decimal

        return coordenada_decimal
    except Exception as e:
        print(f"Error converting GPS coordinates: {e}")
        return None

def verificar_imagem(caminho_arquivo):
    """
    Image diagnostic function
    """
    print("\n🔬 Image Diagnostic:")
    print(f"File: {caminho_arquivo}")

    try:
        # Check with Pillow
        with Image.open(caminho_arquivo) as img:
            print(f"✅ Pillow: Image loaded successfully")
            print(f"Format: {img.format}")
            print(f"Mode: {img.mode}")
            print(f"Size: {img.size}")
    except Exception as e:
        print(f"❌ Pillow error: {e}")

    try:
        # Check with OpenCV
        imagem = cv2.imread(caminho_arquivo)
        if imagem is not None:
            print(f"✅ OpenCV: Image loaded successfully")
            print(f"Dimensions: {imagem.shape}")
        else:
            print("❌ OpenCV: Failed to load image")
    except Exception as e:
        print(f"❌ OpenCV error: {e}")

class MetadataExtractor:
    def __init__(self, diretorio_base):
        self.diretorio_base = diretorio_base
        self.diretorio_resultados = os.path.join(diretorio_base, "RESULTADOS_METADADOS")
        os.makedirs(self.diretorio_resultados, exist_ok=True)

    def extrair_metadados_imagem(self, caminho_arquivo):
        """
        Extracts detailed metadata from images
        """
        try:
            # Image diagnostic
            verificar_imagem(caminho_arquivo)

            # Extraction with Pillow
            imagem_pil = Image.open(caminho_arquivo)

            # Extraction with ExifRead
            with open(caminho_arquivo, 'rb') as img_file:
                exif_tags = exifread.process_file(img_file, details=False)

            # Analysis with OpenCV - with error handling
            try:
                imagem_cv2 = cv2.imread(caminho_arquivo)
                if imagem_cv2 is not None:
                    altura, largura, canais = imagem_cv2.shape
                else:
                    altura, largura, canais = 0, 0, 0
            except Exception as e:
                print(f"Error reading image with OpenCV: {e}")
                altura, largura, canais = 0, 0, 0

            # GPS coordinates processing
            coordenadas_gps = None
            try:
                gps_latitude = exif_tags.get('GPS GPSLatitude')
                gps_longitude = exif_tags.get('GPS GPSLongitude')

                if gps_latitude and gps_longitude:
                    latitude = converter_coordenadas_gps(
                        gps_latitude.values,
                        str(exif_tags.get('GPS GPSLatitudeRef', 'N'))
                    )
                    longitude = converter_coordenadas_gps(
                        gps_longitude.values,
                        str(exif_tags.get('GPS GPSLongitudeRef', 'E'))
                    )

                    if latitude and longitude:
                        coordenadas_gps = {
                            "latitude": latitude,
                            "longitude": longitude,
                            "link_maps": f"https://www.google.com/maps?q={latitude},{longitude}"
                        }
            except Exception as e:
                print(f"Error processing GPS: {e}")

            # Metadata dictionary assembly
            info_imagem = {
                "tipo": "Imagem",
                "formato": imagem_pil.format,
                "modo": imagem_pil.mode,
                "tamanho_pixels": imagem_pil.size,
                "dimensoes": {
                    "altura": altura,
                    "largura": largura,
                    "canais_cor": canais
                },
                "exif_tags": {str(k): str(v) for k, v in exif_tags.items()}
            }

            # Add GPS coordinates if found
            if coordenadas_gps:
                info_imagem["coordenadas_gps"] = coordenadas_gps

            return info_imagem
        except Exception as e:
            return {"erro": str(e)}

    def extrair_metadados_pdf(self, caminho_arquivo):
        """
        Extracts metadata from PDF files
        """
        try:
            with open(caminho_arquivo, 'rb') as arquivo:
                leitor_pdf = PyPDF2.PdfReader(arquivo)
                metadados = leitor_pdf.metadata or {}

                info_pdf = {
                    "tipo": "PDF",
                    "número_páginas": len(leitor_pdf.pages),
                    "metadados": {
                        k.strip('/'): v for k, v in metadados.items() if v is not None
                    }
                }
                return info_pdf
        except Exception as e:
            return {"erro": str(e)}

    def extrair_metadados_docx(self, caminho_arquivo):
        """
        Extracts metadata from DOCX files
        """
        try:
            documento = docx.Document(caminho_arquivo)
            propriedades = documento.core_properties

            info_docx = {
                "tipo": "DOCX",
                "autor": propriedades.author,
                "criado_em": str(propriedades.created),
                "modificado_em": str(propriedades.modified),
                "categoria": propriedades.category,
                "palavras_chave": propriedades.keywords
            }
            return info_docx
        except Exception as e:
            return {"erro": str(e)}

    def processar_diretorio(self):
        """
        Processes all files in a directory
        """
        resultados = {
            "data_processamento": datetime.now().isoformat(),
            "arquivos_processados": []
        }

        # Supported file extensions
        extensoes_suportadas = [
            '.pdf', '.docx', '.doc',
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'
        ]

        # Recursive directory scan
        for pasta_raiz, _, arquivos in os.walk(self.diretorio_base):
            for arquivo in arquivos:
                caminho_completo = os.path.join(pasta_raiz, arquivo)
                extensao = os.path.splitext(arquivo)[1].lower()

                # Process only supported files
                if extensao in extensoes_suportadas:
                    try:
                        # Basic file info
                        info_arquivo = {
                            "nome_arquivo": arquivo,
                            "caminho_arquivo": caminho_completo,
                            "tamanho_bytes": os.path.getsize(caminho_completo),
                            "data_criacao": datetime.fromtimestamp(os.path.getctime(caminho_completo)).isoformat(),
                            "data_modificacao": datetime.fromtimestamp(os.path.getmtime(caminho_completo)).isoformat()
                        }

                        # Type-specific metadata extraction
                        if extensao == '.pdf':
                            metadados = self.extrair_metadados_pdf(caminho_completo)
                        elif extensao in ['.docx', '.doc']:
                            metadados = self.extrair_metadados_docx(caminho_completo)
                        elif extensao in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']:
                            metadados = self.extrair_metadados_imagem(caminho_completo)
                        else:
                            continue

                        # Combine information
                        info_arquivo.update(metadados)
                        resultados["arquivos_processados"].append(info_arquivo)
                    except Exception as e:
                        print(f"Error processing {arquivo}: {e}")

        # Save results to JSON
        arquivo_saida = os.path.join(
            self.diretorio_resultados,
            f"relatorio_metadados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )

        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            json.dump(resultados, f, indent=4, ensure_ascii=False)

        print(f"\n📄 Report saved to: {arquivo_saida}")
        return resultados

def main():
    # Directory path for analysis
    diretorio_base = r"C:\Users\InFuture\Desktop\CyberInvestigations\METADADOS"

    # Check directory existence
    if not os.path.exists(diretorio_base):
        print(f"❌ Directory not found: {diretorio_base}")
        print("Create the directory or check the path.")
        return

    # Test library installation
    testar_instalacao_bibliotecas()

    print("\n🚀 Starting Advanced Metadata Extraction")
    print("="*50)

    # Create extractor
    extrator = MetadataExtractor(diretorio_base)

    # Process directory
    resultados = extrator.processar_diretorio()

    # Print summary
    print("\n📊 Summary of Extracted Metadata:")
    print(f"Total files processed: {len(resultados['arquivos_processados'])}")

    # Details of each file (limited to avoid overloading output)
    for i, arquivo in enumerate(resultados['arquivos_processados'][:5]):  # Shows only the first 5
        print(f"\n🔍 File {i+1}: {arquivo['nome_arquivo']}")
        print(f"Type: {arquivo.get('tipo', 'Unknown')}")
        print(f"Size: {arquivo['tamanho_bytes']} bytes")

        # Highlight GPS coordinates if present
        if arquivo.get('tipo') == 'Imagem' and 'coordenadas_gps' in arquivo:
            print("🌍 GPS Coordinates found:")
            gps = arquivo['coordenadas_gps']
            print(f"   Latitude: {gps['latitude']}")
            print(f"   Longitude: {gps['longitude']}")
            print(f"   Google Maps: {gps['link_maps']}")

    if len(resultados['arquivos_processados']) > 5:
        print(f"\n... and {len(resultados['arquivos_processados']) - 5} more files (see full JSON report)")

if __name__ == "__main__":
    main()
