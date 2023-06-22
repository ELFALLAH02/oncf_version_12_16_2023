from st_aggrid import JsCode

BtnCellRenderer_Chemin = JsCode('''
    class BtnCellRenderer {
        init(params) {
            this.params = params;
            this.eGui = document.createElement('div');
            this.eGui.innerHTML = `
                <button id='btn-download'
                    style='
                        color: ${this.params.color};
                        background: ${this.params.background};
                        width: ${this.params.width};
                        height: ${this.params.height};
                        border: ${this.params.border};
                '>Télécharger</button>
            `;
            this.eButton = this.eGui.querySelector('#btn-download');
            this.btnClickedHandler = this.btnClickedHandler.bind(this);
            this.eButton.addEventListener('click', this.btnClickedHandler);
        }

        getGui() {
            return this.eGui;
        }

        refresh() {
            return true;
        }

        destroy() {
            if (this.eButton) {
                this.eGui.removeEventListener('click', this.btnClickedHandler);
            }
        }

        btnClickedHandler(event) {
            const videoPath = this.params.data.chemin;
            if (confirm('Êtes-vous sûr de vouloir ouvrir cette vidéo dans un nouvel onglet et la télécharger ?')) {
                const newTab = window.open('', '_blank');
                const htmlContent = `
                    <div style="width: 50%; margin: 0 auto;">
                        <video controls autoplay style="width: 100%;">
                            <source src="${videoPath}" type="video/mp4">
                            Your browser does not support the video tag.
                        </video>
                        <button id="download-btn" href="${videoPath}" download="${videoPath.substring(videoPath.lastIndexOf('/') + 1)}"
                            style="display: block; margin-top: 10px; text-align: center;
                            color: ${this.params.color};
                            background: ${this.params.background};
                            width: ${this.params.width};
                            height: ${this.params.height};
                            border: ${this.params.border};
                            padding: 10px;
                            cursor: pointer;
                            text-decoration: none;">
                            download
                        </button>
                    </div>
                `;
                newTab.document.body.innerHTML = htmlContent;

                const downloadButton = newTab.document.getElementById('download-btn');
                downloadButton.addEventListener('click', (event) => {
                    event.preventDefault();
                    const videoUrl = downloadButton.href;
                    const fileName = downloadButton.getAttribute('download');
                    const downloadLink = document.createElement('a');
                    downloadLink.href = videoUrl;
                    downloadLink.download = fileName;
                    downloadLink.click();
                    newTab.close();
                });
            }
        }
    };
''')
