# CSM Viewer

Visualizador de arquivos Motion Capture (`.CSM` e `.TXT`) desenvolvido em Python utilizando PyQt5 e Matplotlib.

O objetivo do projeto é permitir a inspeção visual de nuvens de pontos animadas provenientes de sistemas de captura de movimento, oferecendo ferramentas de navegação, filtragem e análise espacial.

## Funcionalidades

### Reprodução

- Reprodução da animação
- Pausa da animação
- Controle de FPS
- Navegação por frame
- Seleção de arquivos durante a execução

### Navegação 3D

- Rotação da câmera com o mouse
- Pan da câmera com o botão do meio
- Zoom utilizando a roda do mouse
- Controles X+, X-, Y+, Y-, Z+, Z-
- Vista ISO
- Fit All
- Fit Frame

### Câmera

- Câmera estável baseada em:
  - Centro (`camera_center`)
  - Raio (`camera_radius`)
  - Elevação (`elev`)
  - Azimute (`azim`)
  - Roll (`roll`)

### Filtro de pontos

- Ocultar pontos temporariamente estáticos
- Definir quantidade de frames analisados
- Definir tolerância mínima de movimento
- Cache de movimento para melhorar desempenho

### Vistas salvas (planejado)

- Salvar múltiplas vistas
- Restaurar vistas rapidamente
- Atalhos de teclado para acesso rápido

## Estrutura do Projeto

```text
csm_viewer/

main.py

controllers/
    camera_controller.py
    animation_controller.py

models/
    mocap_data.py
    view_manager.py

ui/
    canvas_3d.py
    main_window.py

utils/
    mocap_loader.py

requirements.txt
README.md
```

## Instalação

Clone o repositório:

```bash
git clone https://github.com/jounishida/csm_viewer.git
cd csm_viewer
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Dependências

```text
PyQt5
matplotlib
numpy
```

Ou manualmente:

```bash
pip install PyQt5 matplotlib numpy
```

## Execução

```bash
python main.py
```

## Atalhos de Teclado

| Tecla | Função |
|---------|---------|
| Espaço | Play / Pause |
| Home | Vista ISO |
| R | Reset Zoom |
| Shift + R | Reset completo da câmera |
| F | Fit Frame |
| A | Fit All |

## Formatos Suportados

### TXT

Arquivos contendo:

```text
frame x1 y1 z1 x2 y2 z2 ...
```

### CSM

Arquivos exportados por sistemas de Motion Capture compatíveis com o formato CSM.

## Roadmap

### Próximas Funcionalidades

- Vistas salvas (1 a 5)
- Exportação de vídeo MP4
- Trilhas de movimento
- Persistência de frames
- Seleção individual de pontos
- Destacar marcadores específicos
- Auto-rotação da câmera
- Medições de distância
- Suporte a grandes conjuntos de dados

## Licença

Projeto distribuído para fins de estudo, pesquisa e desenvolvimento de ferramentas de visualização para Motion Capture.

## Autor

Jonathan Nishida
