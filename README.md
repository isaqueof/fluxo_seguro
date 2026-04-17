# 🌊 Fluxo Seguro - Centro de Comando Logístico

**Fluxo Seguro** é uma plataforma de inteligência geoespacial B2B projetada para mitigar prejuízos operacionais causados por alagamentos urbanos. O sistema monitora frotas em tempo real, cruza dados com sensores pluviométricos e utiliza IA preditiva para sugerir rotas alternativas seguras, protegendo ativos e otimizando a logística urbana.

## 🚀 Funcionalidades de Alto Impacto

- **Dashboard Executivo (KPIs):** Visualização instantânea de caminhões em risco, patrimônio exposto e ROI estimado em tempo real.
- **Mapeamento Tático 2D:** Visualização de alta precisão de manchas de alagamento e localização da frota sobre logradouros reais de Niterói e Maricá (RJ).
- **Inteligência de Desvio:** Algoritmo que calcula automaticamente a rota alternativa mais segura (menor risco) e fornece instruções precisas para o despacho.
- **Previsão Dinâmica de Vazão:** Gráficos interativos que mostram a estimativa de escoamento da água por logradouro nos próximos 120 minutos.
- **Central de Despacho Live:** Painel interativo para notificação imediata de motoristas com protocolos de contingência.

## 🛠️ Stack Tecnológica de Engenharia

- **[Streamlit](https://streamlit.io/):** Interface reativa de alta performance.
- **[PyDeck](https://deckgl.readthedocs.io/):** Renderização geoespacial avançada com suporte a camadas de ícones e tooltips HTML.
- **[Pandas](https://pandas.pydata.org/):** Processamento e estruturação de dados em memória.
- **[Numpy](https://numpy.org/):** Simulações estatísticas e modelos de risco pluvial.
- **CSS Avançado:** Styling customizado para cards de KPI e design full-color.

## 📥 Instalação e Execução

1. **Clone o repositório:**
   ```bash
   git clone <url-do-repositorio>
   cd fluxo_seguro
   ```

2. **Instale as dependências (Ambiente Isolado recomendado):**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute o Centro de Comando:**
   ```bash
   streamlit run app.py
   ```

## 🗺️ Roadmap de Evolução B2B

- [ ] **Integração Telemetria:** Conexão direta com APIs de rastreamento (ex: Sascar, Omnilink).
- [ ] **Weather API Real:** Substituição da simulação pluviométrica por dados em tempo real (OpenWeather/Climatempo).
- [ ] **Multi-tenancy:** Sistema de login e isolamento de dados por empresa.
- [ ] **Alertas Push:** Integração nativa com WhatsApp Business API para envio automático de rotas de desvio.

---
*Este projeto é um MVP funcional focado em demonstrar o valor financeiro da prevenção logística inteligente.*
