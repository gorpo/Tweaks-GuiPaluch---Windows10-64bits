# Tweaks GuiPaluch

Painel portátil para Windows 10 64 bits com atalhos de manutenção, downloads úteis, backups de Minecraft e rotinas rápidas pós-formatação.

## Recursos

- Interface dark em Tkinter.
- Executável único e portátil.
- Solicita administrador ao abrir.
- Ações para Microsoft Defender, limpeza de temporários, rede, SFC, DISM, energia e ferramentas do Windows.
- Botão de limpeza rápida para `C:\Windows\Temp`, `%TEMP%` e `C:\Windows\Prefetch`.
- Aba de rede sem renovação de IP, pensada para uso com IP fixo.
- Atalhos para espelhar tela em TV/dispositivo sem fio, abrir projeção do Windows e configurar telas.
- Aba `Pastas` com atalhos para Menu Iniciar, Inicializar com Windows, AppData, ProgramData, Temp, Prefetch, hosts e pastas comuns.
- Atalho para abrir a raiz do disco `C:\`.
- Botão para atualizar o Menu Iniciar reiniciando o Explorer.
- Aba de downloads com drivers AMD RX 580, DDU, Java, Minecraft, Forge, NeoForge, Fabric, Git, VS Code e 7-Zip.
- Backup completo ou parcial da pasta `.minecraft`.
- Pasta padrão de backup em `D:\TweaksGuiPaluchBackups`, com opção de escolher outro caminho.
- Exportação de perfil pós-formatação com hardware, drivers, rede, Java, plano de energia e links essenciais.

## Drivers AMD salvos

- `AMD RX580 primeiro estavel - 23.11.1 Polaris/Vega`
- `AMD RX580 estavel para Forza6 - 23.10.01.14`

Os botões abrem páginas oficiais da AMD, em vez de links diretos para `.exe`, porque alguns downloads diretos da AMD redirecionam para `Download Not Complete` fora do fluxo normal do site.

O driver `23.10.01.14` foi mantido como opção específica para o caso de uso com Forza6. A página oficial da AMD lista esse pacote como DirectX 12 Agility SDK.

## Como usar

Baixe o executável em Releases e execute:

```text
Tweaks GuiPaluch.exe
```

O Windows deve mostrar o pedido de administrador. Isso é esperado porque várias ações precisam de permissão elevada.

## Backups

A pasta padrão é:

```text
D:\TweaksGuiPaluchBackups
```

Pela aba `Meu PC`, você pode:

- Mostrar a pasta atual.
- Mudar a pasta de backup.
- Voltar para o padrão no disco `D:`.
- Abrir a pasta de backups.

A preferência fica salva em:

```text
%APPDATA%\TweaksGuiPaluch\settings.json
```

## Build local

Instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

Gere o executável:

```powershell
.\build_exe.ps1
```

O arquivo final será criado em:

```text
dist\Tweaks GuiPaluch.exe
```

## Aviso

Use com atenção. Algumas ações alteram configurações do Windows, limpam caches, reiniciam serviços ou mexem em drivers e rede. Faça backup antes de mudanças grandes.
