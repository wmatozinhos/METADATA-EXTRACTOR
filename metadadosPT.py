import os
import subprocess
import json
from datetime import datetime
import sys

# Os arquivos devem ser colocados dentro da pasta de destino, que nesse caso é METADADOS!
# C:\Users\InFuture\Desktop\CyberInvestigations\METADADOS

# Verificação e importação de bibliotecas
def testar_instalacao_bibliotecas():
    """
    Função para verificar e instalar bibliotecas necessárias
    """
    print("🔍 Verificando bibliotecas para extração de metadados...")
    print("="*60)

    # Lista de bibliotecas necessárias
    bibliotecas = [
        'PyPDF2',
        'python-docx',
        'Pillow',
        'exifread',
        'opencv-python',
        'piexif'
    ]

    # Dicionário de importações
    importacoes = {
        'PyPDF2': 'PyPDF2',
        'python-docx': 'docx',
        'Pillow': 'PIL',
        'exifread': 'exifread',
        'opencv-python': 'cv2',
        'piexif': 'piexif'
    }

    # Bibliotecas faltantes
    bibliotecas_faltantes = []

    # Verificar importação
    for biblioteca in bibliotecas:
        try:
            # Tentar importar
            __import__(importacoes[biblioteca])
            print(f"✅ {biblioteca} instalado")
        except ImportError:
            print(f"❌ {biblioteca} não encontrado")
            bibliotecas_faltantes.append(biblioteca)

    # Tentar instalar bibliotecas faltantes
    if bibliotecas_faltantes:
        print("\n🔧 Tentando instalar bibliotecas faltantes...")
        for biblioteca in bibliotecas_faltantes:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', biblioteca])
                print(f"✅ {biblioteca} instalado com sucesso!")
            except Exception as e:
                print(f"❌ Falha ao instalar {biblioteca}: {e}")

# Importações após verificação
try:
    import PyPDF2
    import docx
    from PIL import Image
    from PIL.ExifTags import TAGS
    import exifread
    import cv2
    import piexif
except ImportError as e:
    print(f"Erro na importação: {e}")
    print("Execute o script novamente para instalar as dependências automaticamente.")

def converter_coordenadas_gps(coordenadas, referencia):
    """
    Converte coordenadas GPS no formato EXIF para decimal
    """
    if not coordenadas or not referencia:
        return None
    
    try:
        graus = float(coordenadas[0])
        minutos = float(coordenadas[1])
        segundos = float(coordenadas[2])
        
        # Conversão para graus decimais
        coordenada_decimal = graus + (minutos / 60.0) + (segundos / 3600.0)
        
        # Ajuste de sinal baseado na referência
        if referencia in ['S', 'W']:
            coordenada_decimal = -coordenada_decimal
        
        return coordenada_decimal
    except Exception as e:
        print(f"Erro na conversão de coordenadas GPS: {e}")
        return None

def verificar_imagem(caminho_arquivo):
    """
    Função de diagnóstico para imagens
    """
    print("\n🔬 Diagnóstico de Imagem:")
    print(f"Arquivo: {caminho_arquivo}")
    
    try:
        # Verificação com Pillow
        with Image.open(caminho_arquivo) as img:
            print(f"✅ Pillow: Imagem carregada com sucesso")
            print(f"Formato: {img.format}")
            print(f"Modo: {img.mode}")
            print(f"Tamanho: {img.size}")
    except Exception as e:
        print(f"❌ Erro no Pillow: {e}")
    
    try:
        # Verificação com OpenCV
        imagem = cv2.imread(caminho_arquivo)
        if imagem is not None:
            print(f"✅ OpenCV: Imagem carregada com sucesso")
            print(f"Dimensões: {imagem.shape}")
        else:
            print("❌ OpenCV: Falha ao carregar imagem")
    except Exception as e:
        print(f"❌ Erro no OpenCV: {e}")

class MetadataExtractor:
    def __init__(self, diretorio_base):
        self.diretorio_base = diretorio_base
        self.diretorio_resultados = os.path.join(diretorio_base, "RESULTADOS_METADADOS")
        os.makedirs(self.diretorio_resultados, exist_ok=True)

    def extrair_metadados_imagem(self, caminho_arquivo):
        """
        Extrai metadados detalhados de imagens
        """
        try:
            # Diagnóstico de imagem
            verificar_imagem(caminho_arquivo)
            
            # Extração com Pillow
            imagem_pil = Image.open(caminho_arquivo)
            
            # Extração com ExifRead
            with open(caminho_arquivo, 'rb') as img_file:
                exif_tags = exifread.process_file(img_file, details=False)
            
            # Análise com OpenCV - com tratamento de erro
            try:
                imagem_cv2 = cv2.imread(caminho_arquivo)
                if imagem_cv2 is not None:
                    altura, largura, canais = imagem_cv2.shape
                else:
                    altura, largura, canais = 0, 0, 0
            except Exception as e:
                print(f"Erro ao ler imagem com OpenCV: {e}")
                altura, largura, canais = 0, 0, 0

            # Processamento de coordenadas GPS
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
                print(f"Erro ao processar GPS: {e}")

            # Montagem do dicionário de metadados
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

            # Adicionar coordenadas GPS se encontradas
            if coordenadas_gps:
                info_imagem["coordenadas_gps"] = coordenadas_gps

            return info_imagem
        except Exception as e:
            return {"erro": str(e)}

    def extrair_metadados_pdf(self, caminho_arquivo):
        """
        Extrai metadados de arquivos PDF
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
        Extrai metadados de arquivos DOCX
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
        Processa todos os arquivos em um diretório
        """
        resultados = {
            "data_processamento": datetime.now().isoformat(),
            "arquivos_processados": []
        }

        # Extensões de arquivo suportadas
        extensoes_suportadas = [
            '.pdf', '.docx', '.doc', 
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'
        ]

        # Varredura recursiva do diretório
        for pasta_raiz, _, arquivos in os.walk(self.diretorio_base):
            for arquivo in arquivos:
                caminho_completo = os.path.join(pasta_raiz, arquivo)
                extensao = os.path.splitext(arquivo)[1].lower()
                
                # Processar apenas arquivos suportados
                if extensao in extensoes_suportadas:
                    try:
                        # Informações básicas do arquivo
                        info_arquivo = {
                            "nome_arquivo": arquivo,
                            "caminho_arquivo": caminho_completo,
                            "tamanho_bytes": os.path.getsize(caminho_completo),
                            "data_criacao": datetime.fromtimestamp(os.path.getctime(caminho_completo)).isoformat(),
                            "data_modificacao": datetime.fromtimestamp(os.path.getmtime(caminho_completo)).isoformat()
                        }

                        # Extração de metadados específica por tipo
                        if extensao == '.pdf':
                            metadados = self.extrair_metadados_pdf(caminho_completo)
                        elif extensao in ['.docx', '.doc']:
                            metadados = self.extrair_metadados_docx(caminho_completo)
                        elif extensao in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']:
                            metadados = self.extrair_metadados_imagem(caminho_completo)
                        else:
                            continue

                        # Combinar informações
                        info_arquivo.update(metadados)
                        resultados["arquivos_processados"].append(info_arquivo)
                    except Exception as e:
                        print(f"Erro ao processar {arquivo}: {e}")

        # Salvar resultados em JSON
        arquivo_saida = os.path.join(
            self.diretorio_resultados, 
            f"relatorio_metadados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            json.dump(resultados, f, indent=4, ensure_ascii=False)
        
        print(f"\n📄 Relatório salvo em: {arquivo_saida}")
        return resultados

def main():
    # Caminho do diretório para análise
    diretorio_base = r"C:\Users\InFuture\Desktop\CyberInvestigations\METADADOS"
    
    # Verificar existência do diretório
    if not os.path.exists(diretorio_base):
        print(f"❌ Diretório não encontrado: {diretorio_base}")
        print("Crie o diretório ou verifique o caminho.")
        return

    # Testar instalação de bibliotecas
    testar_instalacao_bibliotecas()

    print("\n🚀 Iniciando Extração Avançada de Metadados")
    print("="*50)

    # Criar extrator
    extrator = MetadataExtractor(diretorio_base)
    
    # Processar diretório
    resultados = extrator.processar_diretorio()
    
    # Imprimir resumo
    print("\n📊 Resumo dos Metadados Extraídos:")
    print(f"Total de arquivos processados: {len(resultados['arquivos_processados'])}")
    
    # Detalhes de cada arquivo (limitado para não sobrecarregar a saída)
    for i, arquivo in enumerate(resultados['arquivos_processados'][:5]):  # Mostra apenas os primeiros 5
        print(f"\n🔍 Arquivo {i+1}: {arquivo['nome_arquivo']}")
        print(f"Tipo: {arquivo.get('tipo', 'Desconhecido')}")
        print(f"Tamanho: {arquivo['tamanho_bytes']} bytes")
        
        # Destacar coordenadas GPS se existirem
        if arquivo.get('tipo') == 'Imagem' and 'coordenadas_gps' in arquivo:
            print("🌍 Coordenadas GPS encontradas:")
            gps = arquivo['coordenadas_gps']
            print(f"   Latitude: {gps['latitude']}")
            print(f"   Longitude: {gps['longitude']}")
            print(f"   Google Maps: {gps['link_maps']}")
    
    if len(resultados['arquivos_processados']) > 5:
        print(f"\n... e mais {len(resultados['arquivos_processados']) - 5} arquivos (veja o relatório JSON completo)")

if __name__ == "__main__":
    main()
