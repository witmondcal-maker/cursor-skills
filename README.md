# cursor-skills

Coleção pessoal de Agent Skills para o Cursor. Cada pasta na raiz é uma skill independente, no formato aberto do [Agent Skills](https://agentskills.io/specification): uma pasta com um `SKILL.md` (frontmatter YAML com `name` e `description`) e, se precisar, as pastas `references/`, `scripts/` e `assets/`. O mesmo formato é lido pelo Cursor e por outros agentes compatíveis.

| Skill | Para que serve |
|---|---|
| [anti-llmismo-ptbr](anti-llmismo-ptbr/SKILL.md) | Escrever e revisar texto em pt-BR sem cara de IA nem de tradução do inglês: interface, mensagens de erro, documentação, README, commits, PRs, changelogs, e-mails e posts. Traz 19 padrões com exemplos, checklist de 20 perguntas e um scanner em Python. |

## Estrutura

```text
cursor-skills/
├── anti-llmismo-ptbr/
│   ├── SKILL.md                  # instruções que o agente carrega
│   ├── references/
│   │   ├── guia-completo.md      # guia detalhado, com fontes
│   │   └── checklist.md          # 20 perguntas de revisão
│   └── scripts/
│       └── check.py              # scanner (Python 3, sem dependências)
├── tests/                        # testes do scanner
├── LICENSE
└── README.md
```

## Como instalar

O Cursor procura skills nestas pastas ([documentação](https://cursor.com/docs/context/skills)):

| Pasta | Alcance |
|---|---|
| `.cursor/skills/` ou `.agents/skills/` | só o projeto |
| `~/.cursor/skills/` ou `~/.agents/skills/` | todos os projetos da máquina |

Ele também lê `.claude/skills/` e `.codex/skills/`, por compatibilidade. A pasta `.agents/skills/` é a mais neutra para quem usa mais de um agente.

O nome da pasta da skill precisa ser igual ao campo `name` do `SKILL.md`. Por isso, ao copiar ou criar link, mantenha o nome `anti-llmismo-ptbr`.

### Num projeto, copiando

A cópia entra no repositório do projeto e funciona para todo mundo que clonar.

```bash
mkdir -p .cursor/skills
cp -R /caminho/para/cursor-skills/anti-llmismo-ptbr .cursor/skills/
git add .cursor/skills/anti-llmismo-ptbr
```

Para atualizar, copie de novo por cima.

### Num projeto, com link simbólico

O link aponta para um clone local deste repositório, então toda atualização aparece na hora. Serve para uso pessoal: quem clonar o projeto não tem o destino do link.

```bash
mkdir -p .cursor/skills
ln -s /caminho/para/cursor-skills/anti-llmismo-ptbr .cursor/skills/anti-llmismo-ptbr
```

No Windows, use `mklink /D .cursor\skills\anti-llmismo-ptbr C:\caminho\para\cursor-skills\anti-llmismo-ptbr` num terminal com permissão de administrador ou com o modo de desenvolvedor ativo.

### Num projeto, como submódulo do git

O submódulo fixa uma versão deste repositório dentro do projeto. O Cursor varre a pasta de skills de forma recursiva e usa a pasta que contém o `SKILL.md` como identidade da skill, então o repositório inteiro pode ficar numa subpasta.

```bash
git submodule add https://github.com/witmondcal-maker/cursor-skills.git .cursor/skills/cursor-skills
git commit -m "Adiciona cursor-skills como submódulo"
```

Quem clonar o projeto precisa rodar `git submodule update --init`. Para trazer a versão mais nova:

```bash
git submodule update --remote .cursor/skills/cursor-skills
```

### Para todos os projetos da máquina

Clone o repositório num lugar fixo e crie links em `~/.cursor/skills/`:

```bash
git clone https://github.com/witmondcal-maker/cursor-skills.git ~/code/cursor-skills
mkdir -p ~/.cursor/skills
ln -s ~/code/cursor-skills/anti-llmismo-ptbr ~/.cursor/skills/anti-llmismo-ptbr
```

Um `git pull` no clone atualiza todas as skills de uma vez. Skills em `~/.cursor/skills/` ficam só na máquina local; para usá-las em Cloud Agents, ative Sync Skills for Cloud Agents em Settings, Agents.

### Conferindo

No Cursor, abra Customize na barra lateral e vá em Skills. A skill aparece pelo nome. O agente decide sozinho quando usar a skill a partir da `description`; para chamar na mão, digite `/anti-llmismo-ptbr` no chat do Agent.

## Scanner de texto

`anti-llmismo-ptbr/scripts/check.py` procura os padrões do guia em arquivos ou na entrada padrão e mostra linha, coluna, padrão e sugestão. Usa só a biblioteca padrão do Python 3.8+.

```bash
S=anti-llmismo-ptbr/scripts/check.py

python3 $S README.md docs/*.md            # arquivos
git log -1 --format=%B | python3 $S       # mensagem do último commit
python3 $S --text "Vamos estar enviando o relatório."
python3 $S --list                         # regras disponíveis
python3 $S --ignore negrito,e-sobre texto.md
python3 $S --json texto.md                # saída para outras ferramentas
```

O código de saída é 0 sem ocorrências, 1 com ocorrências e 2 em erro. Isso permite usar o scanner num hook de commit ou no CI. Blocos de código, código inline, URLs e destinos de link são ignorados; `--no-markdown` desliga esse filtro. Uma linha com o marcador `anti-llmismo: ignore` fica de fora, e um trecho entre `anti-llmismo: off` e `anti-llmismo: on` também.

O arquivo `references/guia-completo.md` acusa dezenas de ocorrências de propósito, porque reúne os exemplos ruins.

Para rodar os testes:

```bash
python3 -m unittest discover -s tests -v
```

## Como adicionar outra skill

1. Crie uma pasta na raiz com o nome da skill: letras minúsculas, números e hífens, até 64 caracteres, sem hífen no começo, no fim ou repetido (`--`).
2. Dentro dela, crie o `SKILL.md`:

   ```markdown
   ---
   name: nome-da-skill
   description: O que a skill faz e quando usar, com as palavras que o usuário diria ao pedir esse tipo de tarefa. Até 1024 caracteres.
   ---

   # Nome da skill

   Instruções para o agente.
   ```

3. Mantenha o `SKILL.md` curto (a especificação recomenda menos de 500 linhas). Material longo vai para `references/`, código executável para `scripts/` e modelos ou dados para `assets/`. Aponte para esses arquivos com caminho relativo à pasta da skill e não crie cadeias de referência com vários níveis.
4. Campos opcionais aceitos pelo Cursor: `paths` (limita a skill a arquivos que casam com os globs), `disable-model-invocation: true` (só roda quando chamada com `/nome`), `license`, `compatibility` e `metadata`.
5. Para validar o frontmatter, use o [skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref): `skills-ref validate ./nome-da-skill`.
6. Acrescente a skill na tabela do topo deste README.

## Licença

MIT. Veja [LICENSE](LICENSE).
