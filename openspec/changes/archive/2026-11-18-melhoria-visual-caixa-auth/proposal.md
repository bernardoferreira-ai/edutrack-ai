# Change Proposal: melhoria-visual-caixa-auth

## Why
A caixa de formulário onde o usuário realiza o login e o cadastro na página de perfil (`pages/3_👤_Perfil.py`) atualmente ocupa uma largura excessivamente ampla em telas largas e utiliza o estilo padrão do Streamlit para o contêiner `st.form`. Aprimorar o enquadramento, bordas, sombras, espaçamento e estilização dos botões e campos dessa caixa específica confere um aspecto elegante de portal de autenticação moderno, sem alterar nenhuma funcionalidade ou opção.

## What Changes
- Refinar visualmente a caixa de autenticação (Login e Cadastro) em `pages/3_👤_Perfil.py`:
  - Centralizar a caixa na tela através de colunas balanceadas para evitar estiramento visual em telas largas.
  - Estilizar o contêiner do formulário (`[data-testid="stForm"]`) com cantos arredondados (`18px`), fundo branco limpo, borda suave e sombra moderna.
  - Aprimorar o estilo dos botões de submissão ("Entrar" e "Cadastrar") com gradiente refinado e cantos arredondados.
  - Aprimorar os inputs de texto com foco suave e espaçamento confortável.
- Preservar rigorosamente todos os campos (`name`, `email`, `password`), validações, textos de mensagens e fluxos de autenticação com o backend.

## Impact
- **Interface e Usabilidade:** Caixa de login e cadastro centralizada, harmoniosa e com estética profissional.
- **Backend:** Nenhuma alteração nas rotas, endpoints ou serviços (`AuthService` permanece idêntico).
- **Escopo:** Estritamente limitado ao design e posicionamento da caixa de login/cadastro em `pages/3_👤_Perfil.py`.
