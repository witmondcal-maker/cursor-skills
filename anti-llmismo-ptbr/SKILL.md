---
name: anti-llmismo-ptbr
description: Escreve e revisa textos em português do Brasil para que soem naturais, sem cara de texto gerado por IA nem de tradução do inglês. Use sempre que for escrever, traduzir, editar ou revisar texto em português (pt-BR), como textos de interface (UI copy, microcopy, botões, mensagens de erro, notificações, e-mails transacionais), documentação, README, comentários e docstrings, mensagens de commit, descrições de PR, changelogs e release notes, e-mails, posts de LinkedIn e redes sociais, artigos e landing pages. Use também quando o usuário pedir um texto mais natural, menos robótico ou sem cara de ChatGPT, ou pedir para humanizar um texto. Traz 19 padrões de LLMismo e calque com exemplos, regras fixas (sem travessão, emoji ou hashtag por padrão), checklist de 20 perguntas e um scanner em Python sem dependências. Brazilian Portuguese writing and review.
license: MIT
compatibility: O scanner opcional (scripts/check.py) requer Python 3.8 ou mais novo, só com a biblioteca padrão.
metadata:
  author: Ricardo Margalho Prins
  version: "1.0.0"
  language: pt-BR
---

# Anti-LLMismo em pt-BR

Guia para escrever e revisar texto em português do Brasil sem dois tipos de vício. O primeiro é a estrutura retórica que modelos de linguagem repetem em qualquer língua (antítese de enfeite, trinca, frase de efeito no fim). O segundo é a sintaxe e o vocabulário do inglês vestidos de português (passiva, pronome em toda frase, calques como `endereçar`).

Nenhum padrão daqui prova que um texto foi gerado por IA, e um padrão isolado pode passar. O problema é a soma. A meta é o texto soar como uma pessoa falando com outra.

## Quando usar

- Qualquer texto em pt-BR que outra pessoa vai ler: interface, mensagem de erro, documentação, README, commit, PR, changelog, e-mail, post.
- Revisão de texto que o usuário colou ou que já está no repositório.
- Tradução do inglês para o português.

Não se aplica a código, identificadores e saída de ferramentas. Jargão técnico estabelecido (deploy, merge, PR, churn, onboarding) fica quando o público é técnico; para público leigo, troque por português ou explique uma vez.

## Regras fixas

Valem sempre, a não ser que o usuário peça outra coisa de forma explícita.

1. Zero travessão. Isso inclui `—`, `–` usado como pausa e o hífen solto entre espaços no mesmo papel. Use vírgula (aposto curto), ponto (duas ideias), dois-pontos (a segunda parte explica a primeira) ou parênteses (comentário lateral). Intervalo numérico: "de 2019 a 2021" ou "2019-2021".
2. Zero emoji e zero hashtag em prosa, inclusive como marcador de lista.
3. Sem antítese de enfeite: `não é X, é Y`, `mais do que X`, `não apenas X, mas também Y`.
4. Sem frase de efeito no fim. Termine no fato mais concreto e pare.
5. Sem pergunta de engajamento (`O resultado?`, `E você?`). Pergunta só quando o autor quer mesmo a resposta, e específica.
6. Nada inventado. Cena, diálogo, número, nome, cliente ou citação só entram se o usuário forneceu. Faltou dado? Escreva `[FALTA DADO: ...]` e pergunte. Inventar detalhe para soar concreto é pior que a frase vaga. Texto técnico não abre com cena.
7. Sem negrito no corpo, sem rótulo em negrito com dois-pontos e sem Title Case. Títulos em caixa de frase.
8. Precisão técnica vem antes de estilo. Para público dev, "fila com retry e idempotência" não vira "um jeito de não duplicar".

## Fluxo de trabalho

1. Junte o contexto: quem vai ler, que tipo de texto é, quais fatos existem. Se a frase precisa de um dado que não existe, marque `[FALTA DADO: ...]`.
2. Escreva direto. Comece pelo fato, use voz ativa, sujeito claro e verbo simples ("é", "tem", "faz"). Varie o tamanho das frases.
3. Rode o scanner no rascunho (seção abaixo).
4. Passe o checklist de 20 perguntas em [references/checklist.md](references/checklist.md). Ele pega o que regex não pega: trinca de ideias, afirmação sem caso, fato inventado, parágrafos todos do mesmo tamanho.
5. Reescreva cada trecho apontado. Mude a estrutura da frase ou corte. Trocar a palavra por um sinônimo não resolve: `Além disso` virando `Fora isso` dá no mesmo.
6. Rode o scanner de novo. Repita até sair limpo ou até cada ocorrência restante ter motivo (citação literal, nome próprio, termo técnico, uso literal como "o backup roda no final do expediente").
7. Releia como se fosse em voz alta. Se você não diria aquilo para um colega ou para o cliente, reescreva.

Ao entregar, não liste as regras aplicadas, a menos que o usuário peça. Se manteve uma ocorrência de propósito, diga qual e por quê em uma linha.

## Scanner

`scripts/check.py` usa só a biblioteca padrão do Python 3.8+. O caminho é relativo à pasta da skill; num projeto, costuma ser `.cursor/skills/anti-llmismo-ptbr/scripts/check.py`.

```bash
python3 scripts/check.py README.md docs/guia.md
git log -1 --format=%B | python3 scripts/check.py
python3 scripts/check.py --text "Vamos estar enviando o relatório amanhã."
python3 scripts/check.py --list
```

- Saída: `arquivo:linha:coluna: [id] Nome: "trecho". Sugestão: ...`. Sai com código 1 quando acha algo, 0 quando não acha e 2 em erro de uso.
- Pula blocos de código cercados, código inline, URLs e destinos de link. Com `--no-markdown`, varre tudo.
- `--ignore negrito,e-sobre` desliga regras, `--only travessao,emoji` roda só as escolhidas, `--json` serve para outras ferramentas e `--summary` mostra a contagem por regra.
- Para manter uma linha de propósito, ponha nela `anti-llmismo: ignore` (num comentário HTML, por exemplo). Para um trecho, cerque com `anti-llmismo: off` e `anti-llmismo: on`.
- Achar não é condenar. Algumas regras são heurísticas (pronome em excesso, trinca, sinônimo que gira) e erram para os dois lados.
- `references/guia-completo.md` acusa dezenas de ocorrências porque traz os exemplos ruins de propósito.

## Os 19 padrões

Cada item tem o que evitar, um exemplo ruim entre crases e uma versão melhor. Os números dos exemplos são ilustrativos. Explicação, nuances e fontes estão em [references/guia-completo.md](references/guia-completo.md).

### Estrutura retórica

1. Trinca automática. Três itens só quando cada um diz algo que os outros não dizem.
   - Ruim: `Construímos a plataforma com foco em simplicidade, escalabilidade e segurança.`
   - Melhor: "A plataforma roda num servidor só e aguentou as 3 mil rematrículas de janeiro sem cair."
2. Antítese de enfeite (`não é X, é Y`, `mais do que X`, `não apenas X, mas também Y`, `X, e não Y`). Só fica quando o X é uma crença que o leitor tem de fato.
   - Ruim: `Não é sobre código. É sobre pessoas.`
   - Melhor: "O bug ficou três semanas aberto porque ninguém sabia quem era dono do módulo de boletos."
3. Frase de efeito no fechamento.
   - Ruim: `Os chamados caíram pela metade. Às vezes, menos é mais.`
   - Melhor: "Os chamados caíram pela metade. O que sobrou é quase tudo sobre aluno transferido no meio do bimestre."
4. Paralelismo simétrico (antes e depois, ontem e hoje, menos isso e mais aquilo).
   - Ruim: `Antes: planilhas, retrabalho e caos. Depois: um painel, um clique e paz.`
   - Melhor: "A coordenação passava a segunda-feira conferindo frequência na planilha. Agora confere em uns 20 minutos."
5. Pergunta retórica de engajamento, que o próprio texto responde.
   - Ruim: `O resultado? 40% menos chamados no suporte.`
   - Melhor: "Os chamados no suporte caíram 40%."
6. Cena inventada e arco narrativo (cenário, crise, virada, lição) em assunto técnico.
   - Ruim: `Sexta-feira, 18h. O café já tinha esfriado. A diretora me ligou com a voz trêmula.`
   - Melhor: "Na sexta passada um job de geração de boletos rodou duas vezes e duplicou a cobrança de 112 famílias. O motivo foi um retry sem idempotência."
7. Abertura cerimonial e tom de newsletter. Teste: corte a primeira frase e veja se fez falta.
   - Ruim: `Em um cenário cada vez mais competitivo, a tecnologia se tornou essencial. Neste post, vou compartilhar 3 aprendizados.`
   - Melhor: "Três escolas cancelaram o contrato com a gente no ano passado. Duas pelo mesmo motivo: o app dos pais não funcionava em Android antigo."
8. Abstração vaga no lugar de fato. Afirmação geral pede caso, número ou nome ao lado. Estudo, só nomeado e com link.
   - Ruim: `Estudos mostram que times com autonomia entregam mais.`
   - Melhor: "Depois que cada dev passou a fazer deploy sem esperar aprovação, o tempo entre merge e produção caiu de dois dias para algumas horas."
9. Hedging e meta-comentário. Diga a coisa em vez de comentar o texto. Ressalva com conteúdo pode ficar, uma por afirmação.
   - Ruim: `O ponto aqui é que vale olhar com carinho para a dívida técnica.`
   - Melhor: "Adiamos a troca do ORM por um ano. Nesse ano, cada relatório novo levava o dobro do tempo."

### Sintaxe do inglês

10. Voz passiva traduzida e fórmula impessoal (`foi decidido`, `faz-se necessário`). Diga quem fez.
    - Ruim: `Uma nova versão do app foi lançada hoje.`
    - Melhor: "Lançamos hoje a versão nova do app."
11. Gerundismo e gerúndio pendurado no fim da frase (`, garantindo`, `, permitindo`).
    - Ruim: `Vamos estar liberando o acesso amanhã.` e `Migramos para o Postgres 16, garantindo mais performance.`
    - Melhor: "Amanhã liberamos o acesso." e "Migramos para o Postgres 16. O relatório de inadimplência, que levava 40 segundos, agora abre em 3."
12. Pronome sujeito em toda frase e possessivo em todo substantivo. O verbo já marca a pessoa. Cuidado com `seu/sua` ambíguo.
    - Ruim: `Abri meu notebook, revisei meu código e mandei meu PR.`
    - Melhor: "Abri o notebook, revisei o código e mandei o PR."
13. Molde de frase do inglês (`Como fundador, eu...`, `Aqui está o porquê:`, `Uma coisa que aprendi é`, `X é sobre Y`, `uma incrível experiência`).
    - Ruim: `Como desenvolvedor, uma coisa que eu aprendi é que testes são sobre confiança.`
    - Melhor: "Sem teste no módulo financeiro eu não durmo na véspera de fechamento de mês."
14. Conectivo de redação (`além disso`, `vale ressaltar`, `nesse sentido`, `em suma`, `por fim`). Troque por "e", "mas", "só que", "então" ou ponto final.
    - Ruim: `Além disso, vale ressaltar que o módulo de matrícula foi reescrito.`
    - Melhor: "Também reescrevemos a matrícula. Cadastrar um aluno levava 12 minutos; agora leva 4."

### Vocabulário

15. Calque lexical e corporativês traduzido. Tabela completa no guia.

    | Evitar | Usar no lugar |
    |---|---|
    | `endereçar` um problema | resolver, tratar de, atacar |
    | `no final do dia` | no fim das contas, no fundo, ou cortar |
    | `faz todo o sentido` como bordão | dizer a razão |
    | `jornada` | nomear as etapas, ou trajetória |
    | `alavancar`, `potencializar`, `impulsionar` | usar, aproveitar, aumentar, ou o número |
    | `robusto` | dizer o que aguenta |
    | `mergulhar`, `deep dive` | olhar em detalhe, destrinchar |
    | `entregar valor` | dizer o que o cliente ganhou |
    | `aprendizados` | o que aprendi, lições |
    | `realizar` no sentido de perceber | perceber, notar |
    | `eventualmente` no sentido de "no fim" | no fim, com o tempo |
    | `assumir` no sentido de supor | supor, partir do princípio |
    | `suportar` no sentido de ser compatível | funciona em, é compatível com |
    | `impactar positivamente` | melhorar, reduzir, aumentar, mais o quê |
    | `mover a agulha`, `divisor de águas`, `ganha-ganha` | dizer o efeito concreto |

    - Ruim: `Precisamos endereçar esse problema para entregar valor ao cliente.`
    - Melhor: "Precisamos resolver a cobrança duplicada antes de janeiro."
16. Vocabulário inflado e verbo que foge do "é" (`crucial`, `fundamental`, `ecossistema`, `se consolida como`, `desempenha um papel`). No máximo uma palavra dessas por texto.
    - Ruim: `A plataforma se consolida como uma solução robusta e conta com um ecossistema de integrações.`
    - Melhor: "A plataforma integra com os três ERPs que as escolas da nossa base mais usam."
17. Sinônimo que gira. Escolha um nome por coisa e repita sem medo.
    - Ruim: `A plataforma emite boletos. A solução também concilia pagamentos, e a ferramenta ainda manda lembrete.`
    - Melhor: "O sistema emite o boleto, dá baixa quando o pagamento cai e manda lembrete aos pais."

### Pontuação e formatação

18. Travessão: zero, conforme a regra fixa 1.
    - Ruim: `A migração — que parecia simples — levou três meses.`
    - Melhor: "A migração parecia simples e levou três meses."
19. Negrito, emoji, hashtag e formatação de LinkedIn (uma frase por linha, bullets todos iguais, Title Case).
    - Ruim: `🚀 **3 Lições Que Aprendi** ✅ **Foco:** menos é mais. #SaaS #Liderança`
    - Melhor: "No primeiro ano, fizemos tudo que as escolas pediram. Em dezembro tínhamos 40 telas que só uma escola usava."

## Ajustes por tipo de texto

- Interface e mensagem de erro: frase curta, diga o que houve e o que fazer ("Não foi possível salvar. Verifique a conexão e tente de novo."). Sem `Ops!`, sem culpar o usuário. A mesma coisa tem o mesmo nome em todas as telas.
- Commit, PR e changelog: siga a convenção do repositório (idioma, Conventional Commits, tempo verbal). A primeira linha diz o que muda e o corpo diz por quê, em voz ativa ("Corrige cálculo de juros quando a parcela vence no sábado"). PR: o que muda, por quê e como testar. Sem adjetivo de venda.
- Documentação e README: comece pelo que a coisa faz e como usar. Instrução no imperativo ("Instale", "Rode"), com comandos testados.
- E-mail: assunto específico e o pedido ou a informação principal na primeira frase. Sem abertura de enchimento traduzida (`Espero que este e-mail o encontre bem`).
- Post de LinkedIn e redes: registro de fundador falando com colega, primeira pessoa quando é experiência própria, final no fato.

## Para não criar outro vício

- Não troque um tique por outro. Repetir palavra pode; repetir estrutura cansa.
- Mais humano não quer dizer mais gíria. Nada de "mano" ou "papo reto" para compensar.
- Frases todas com oito palavras também soam a máquina. Alterne longa, curta e média.

## Arquivos

- [references/guia-completo.md](references/guia-completo.md): os 19 padrões em detalhe, a tabela completa de calques, nuances e fontes com links.
- [references/checklist.md](references/checklist.md): as 20 perguntas de revisão.
- [scripts/check.py](scripts/check.py): o scanner.
