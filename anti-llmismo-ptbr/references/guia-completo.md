# Guia anti-LLMismo e anti-calque para textos em PT-BR

Guia de revisão para textos em português do Brasil. Nasceu para revisar os posts de LinkedIn do Ricardo Margalho Prins (fundador e dev; escreve sobre engenharia de software, produto/SaaS e educação/escolas) e vale para qualquer texto em prosa: posts, e-mails, documentação, README, mensagens de commit, descrições de PR, changelogs e textos de interface.

Este arquivo traz os exemplos ruins de propósito. O scanner da skill (`scripts/check.py`) acusa todos eles, e isso é esperado. Os arquivos que o agente escreve é que precisam sair limpos.

Queixa que motivou o guia: o texto sai com cara de tradução literal do inglês. Quase sempre o problema está em dois lugares ao mesmo tempo. Um é a estrutura retórica que modelos de linguagem repetem em qualquer língua (antítese, trinca, frase de efeito no fim). O outro é a sintaxe e o vocabulário do inglês vestidos de português (passiva, pronome em toda frase, "endereçar", "no final do dia").

Três avisos antes de usar:

1. Nenhum item abaixo prova que um texto foi gerado por IA. A própria página da Wikipedia que serve de base lembra que esses padrões aparecem em texto humano e que um sinal sozinho não basta. O objetivo aqui é o texto soar como o autor, e não "enganar detector".
2. Um padrão isolado pode passar. O problema é a soma: trinca + antítese + travessão + fecho de efeito no mesmo post.
3. Os números e casos nos exemplos "melhor" são ilustrativos. No rascunho real, só entra fato, número, nome ou episódio que o autor (quem pediu o texto) forneceu. Se a frase precisa de um dado que não temos, marque `[FALTA DADO: ...]` e pergunte. Inventar detalhe para soar concreto é pior que a frase vaga.

---

## Parte 1. Estrutura retórica

### 1. Trinca automática (tricolon)

Por que soa artificial: o modelo fecha ideias em grupos de três porque soa "completo". Em português, a trinca de adjetivos ou de benefícios lembra folder de empresa. O sinal fica mais forte quando os três itens são abstratos e intercambiáveis, ou quando aparece três frases curtas seguidas de uma lição.

Ruim:
> Construímos a plataforma com foco em simplicidade, escalabilidade e segurança.

> A escola ganhou tempo, a secretaria ganhou autonomia e os pais ganharam tranquilidade.

Melhor:
> A plataforma roda num servidor só e aguentou as 3 mil rematrículas de janeiro sem cair.

> A secretaria parou de imprimir boleto. Os pais pagam pelo Pix do próprio e-mail de cobrança.

Regra prática: se são três, confira se cada item diz algo que os outros não dizem. Se não diz, fique com um ou dois. Três itens reais (três escolas, três bugs) podem ficar.

### 2. "Não é X, é Y" e antíteses de enfeite

Por que soa artificial: a primeira metade nega algo que ninguém afirmou, só para a segunda parecer maior. É o tique mais reconhecível de texto de IA hoje (a Wikipedia chama de *negative parallelism*). Variantes em PT-BR: "não é sobre X, é sobre Y", "mais do que X, é Y", "não se trata de X, e sim de Y", "não apenas X, mas também Y", "X, e não Y", e a versão picotada "Não é sorte. É processo."

Ruim:
> Não é sobre código. É sobre pessoas.

> Mais do que um sistema de gestão escolar, uma nova forma de pensar a educação.

> O sistema não apenas emite boletos, mas também concilia pagamentos.

Melhor:
> O bug ficou três semanas aberto porque ninguém sabia quem era dono do módulo de boletos.

> O sistema emite o boleto e dá baixa sozinho quando o pagamento cai.

Quando pode ficar: quando a metade negada corrige uma crença que o leitor de fato tem, e as duas metades trazem informação.
> Muita gente acha que escola troca de sistema por preço. Nas escolas que atendemos, quem decidiu foi a secretaria, pelo tempo que levava para fechar o mês.

### 3. Frase de efeito no fechamento

Por que soa artificial: o parágrafo termina com uma linha solta que repete a ideia em tom de aforismo. Em post de LinkedIn isso vira assinatura de IA: "Pense nisso.", "Simples assim.", "E isso muda tudo.", "Leia de novo.", "No fim, software é sobre confiança."

Ruim:
> Reescrevemos o módulo de notas em duas semanas e os chamados caíram pela metade.
>
> Às vezes, menos é mais.

Melhor:
> Reescrevemos o módulo de notas em duas semanas e os chamados caíram pela metade. O que sobrou é quase tudo sobre aluno transferido no meio do bimestre.

Regra prática: termine no fato mais concreto que você tem e pare. Se quiser terminar com pergunta, que seja uma pergunta que o autor queira mesmo ver respondida (ver item 5).

### 4. Paralelismo simétrico antes/depois

Por que soa artificial: estruturas espelhadas ("Antes: ... Depois: ...", "Ontem X. Hoje Y.", "Menos X, mais Y") têm ritmo de slogan. A simetria perfeita denuncia que a frase foi montada pela forma, e não pelo conteúdo. Parentes próximos: todos os bullets do mesmo tamanho, todos começando com verbo no infinitivo.

Ruim:
> Antes: planilhas, retrabalho e caos. Depois: um painel, um clique e paz.

> Ontem eu escrevia código. Hoje eu escrevo produto.

> Menos reunião, mais entrega.

Melhor:
> A coordenação passava a segunda-feira conferindo frequência na planilha. Agora confere em uns 20 minutos. O erro que sobrou é aluno transferido que ninguém baixou no sistema.

> Faz dois anos que programo menos de um dia por semana. O resto vai em conversa com escola e em decidir o que não fazer.

### 5. Pergunta retórica de engajamento

Por que soa artificial: a pergunta não é pergunta, é gancho. "O resultado? ...", "E o melhor? ...", "Você já parou pra pensar...?", "Vale a pena? Depende.", "E você, como lida com isso? Comenta aí 👇". O texto pergunta e responde sozinho.

Ruim:
> O resultado? 40% menos chamados no suporte.

> Você já parou pra pensar em quanto custa um deploy quebrado na semana de matrícula?

Melhor:
> Os chamados no suporte caíram 40%.

> Um deploy quebrado na semana de matrícula custou um dia inteiro de atendimento por telefone para duas escolas.

Quando pode ficar: pergunta final específica, que o autor quer de fato ouvir.
> Alguém já migrou base de alunos com CPF duplicado vindo de sistema antigo? Queria saber como vocês resolveram a fusão dos cadastros.

### 6. Cena inventada e arco narrativo em assunto técnico

Por que soa artificial: o modelo abre com uma cena ("Eram 3h da manhã quando o servidor caiu. Olhei para a tela e pensei: e agora?") e segue o arco padrão: cenário, crise, virada, lição. Em post técnico, isso atrasa o assunto e, pior, costuma trazer detalhes que não aconteceram.

Ruim:
> Sexta-feira, 18h. O café já tinha esfriado. A diretora me ligou com a voz trêmula: "Ricardo, os boletos sumiram." Naquele momento eu entendi tudo.

Melhor:
> Na sexta passada um job de geração de boletos rodou duas vezes e duplicou a cobrança de 112 famílias. O motivo foi um retry sem idempotência. Conto abaixo o que mudamos.

Regra: cena só se o autor contou o episódio, e só com os detalhes que ele deu. Nada de café esfriando, voz trêmula ou diálogo reconstruído.

### 7. Tom de newsletter e abertura cerimonial

Por que soa artificial: o texto aquece antes de dizer qualquer coisa ou anuncia o que vai fazer. "Bora lá.", "Vamos por partes.", "Neste post vou mostrar...", "Aqui vai o que aprendi:", "Senta que lá vem história", "Spoiler:", "3 lições que aprendi ao...", "Salve este post", "Se isso fez sentido pra você, compartilha". Há também a abertura de redação escolar: "No cenário atual...", "Nos dias de hoje...", "Em um mundo cada vez mais digital...".

Ruim:
> Em um cenário cada vez mais competitivo, a tecnologia se tornou essencial para as escolas. Neste post, vou compartilhar 3 aprendizados da nossa jornada.

Melhor:
> Três escolas cancelaram o contrato com a gente no ano passado. Duas pelo mesmo motivo: o app dos pais não funcionava em Android antigo.

Teste: corte a primeira frase. Se o post não perdeu nada, ela era aquecimento.

### 8. Abstração vaga no lugar de fato

Por que soa artificial: o modelo troca o detalhe específico (raro, portanto improvável estatisticamente) por uma afirmação genérica que serve para qualquer empresa. A Wikipedia descreve isso como a foto nítida virando esboço borrado enquanto o texto grita que aquilo é importante. Sintomas: "transformar a educação", "impacto significativo", "marco", "divisor de águas", "papel fundamental", "cultura forte", "times de alta performance", e atribuição vaga ("especialistas apontam", "estudos mostram", "o mercado já entendeu que").

Ruim:
> A tecnologia tem o poder de transformar a educação, e escolas que entendem isso saem na frente.

> Estudos mostram que times com autonomia entregam mais.

Melhor:
> Numa escola de 600 alunos, o fechamento mensal da secretaria caiu de cinco dias para um depois que a conciliação passou a ser automática.

> No nosso time, depois que cada dev passou a fazer deploy sem esperar aprovação, o tempo entre merge e produção caiu de dois dias para algumas horas.

Regra: toda afirmação geral precisa de um caso, número, nome (ou setor, se for confidencial) logo ao lado. Se não houver, corte a afirmação ou marque `[FALTA DADO]`. "Estudos mostram" só com o estudo nomeado e linkado.

### 9. Hedging e meta-comentário

Por que soa artificial: o texto comenta a si mesmo em vez de dizer a coisa. "O ponto aqui é...", "A questão é...", "O que eu quero dizer é...", "Vale olhar com carinho para...", "Sendo bem honesto:", "Sinceramente?", "Vou ser direto:", "Pode parecer óbvio, mas...", "Não estou dizendo que X, mas...", "De certa forma, talvez seja possível que...". Encenar franqueza ("sendo bem honesto") faz o leitor desconfiar do resto.

Ruim:
> O ponto aqui é que vale olhar com carinho para a dívida técnica. Não estou dizendo que refatorar é sempre a resposta, mas, de certa forma, ignorar isso pode trazer problemas.

Melhor:
> Adiamos a troca do ORM por um ano. Nesse ano, cada relatório novo para escola levava o dobro do tempo, porque toda consulta precisava de gambiarra.

Ressalva honesta pode ficar, uma por afirmação e com conteúdo: "Funcionou nas quatro escolas onde testamos. Não sei se funciona em rede com 40 unidades."

---

## Parte 2. Sintaxe do inglês em português

### 10. Voz passiva traduzida

Por que soa artificial: o inglês usa a passiva analítica (ser + particípio) bem mais que o português. Guimarães e Souza (UFMG, 2016), citando Duarte (1990), relatam que num corpus escrito o inglês tinha uma passiva para cada sete ativas, e o português brasileiro uma para cada vinte. O PB tem outras saídas para tirar o agente de cena (sujeito "a gente", indeterminado, ativa com sujeito genérico). Passiva em excesso vira relatório de repartição.

Ruim:
> Foi decidido pela equipe que a funcionalidade seria removida.

> O sistema foi desenvolvido para ser utilizado por professores em sala.

> Uma nova versão do app foi lançada hoje.

Melhor:
> A gente decidiu tirar a funcionalidade.

> Fiz o sistema pensando no professor que lança nota pelo celular no intervalo.

> Lançamos hoje a versão nova do app.

Também vale para a passiva burocrática com "se" e fórmulas impessoais: "foi identificado que", "faz-se necessário", "acredita-se que", "é possível afirmar que". Diga quem fez ou quem acha.

### 11. Gerundismo e o gerúndio-rabicho

Por que soa artificial: dois casos diferentes.

(a) Gerundismo clássico, de telemarketing: "vou estar enviando", "estaremos liberando". Há debate sobre a origem. José Augusto Carvalho (revista Língua Portuguesa) argumenta que não vem do inglês, e sim de um abuso da perífrase para ações pontuais, que não duram no tempo. Para o nosso check a origem não importa: soa a roteiro de call center.

Ruim:
> Vamos estar liberando o acesso para as escolas piloto amanhã.

Melhor:
> Amanhã liberamos o acesso para as escolas piloto.

(b) Gerúndio-rabicho, que é o calque de fato: a oração com "-ing" pendurada no fim da frase em inglês ("..., ensuring...", "..., highlighting...", "..., allowing..."). A Wikipedia lista isso como sinal forte de análise superficial: o gerúndio acrescenta uma interpretação genérica a um fato simples.

Ruim:
> Migramos o banco para o Postgres 16, garantindo mais performance e permitindo que as escolas acessem relatórios em tempo real, reforçando nosso compromisso com a qualidade.

Melhor:
> Migramos o banco para o Postgres 16. O relatório de inadimplência, que levava 40 segundos, agora abre em 3.

Regra: gerúndio no fim de frase com "garantindo", "permitindo", "reforçando", "destacando", "evidenciando", "contribuindo para", "promovendo" quase sempre pode virar ponto final + frase nova com sujeito, ou simplesmente sair.

### 12. Pronome sujeito em toda frase, possessivo em todo substantivo

Por que soa artificial: em inglês o sujeito é obrigatório ("I think", "you should") e o possessivo também ("my laptop", "your team"). O português marca a pessoa no verbo e dispensa o possessivo quando o dono é óbvio. Tradução literal enche o texto de "eu", "você", "seu", "sua", "meu".

Nuance honesta: o PB falado vem preenchendo cada vez mais o sujeito, sobretudo "eu" e "você" (Duarte e Marins, 2021, mostram essa mudança em curso). Então "eu" não é erro. O problema é a densidade: "eu" abrindo três frases seguidas e "seu/sua" em todo objeto soam como o inglês por baixo. Para o possessivo, Wielgosz (2013) descreve que em português o possessivo costuma ser omitido quando a posse é óbvia (partes do corpo, coisas pessoais), ao contrário do inglês, onde ele normalmente fica.

Ruim:
> Eu acredito que você deveria revisar seu processo de deploy antes de você contratar mais pessoas para seu time.

> Abri meu notebook, revisei meu código e mandei meu PR.

Melhor:
> Antes de contratar mais gente, revise o processo de deploy.

> Abri o notebook, revisei o código e mandei o PR.

Atenção extra ao "seu/sua" ambíguo: "O diretor falou com o professor sobre seu atraso" (de quem?). Prefira "o atraso dele" ou reescreva.

### 13. Ordem e moldes de frase do inglês

Por que soa artificial: a frase segue o molde inglês mesmo com palavras portuguesas. Casos comuns:

- Abertura com aposto de identidade: "Como fundador, eu aprendi que..." (*As a founder, I...*). Melhor: "Fundei a empresa em 2019 e só fui entender X em 2022."
- Adjetivo de valor anteposto em série: "uma incrível experiência", "um enorme aprendizado", "uma importante lição". A anteposição existe em português, mas marca ênfase ou registro literário. Em série, é o molde inglês. Melhor: "aprendi muito", "foi um aprendizado grande", ou dizer o que se aprendeu.
- Fórmulas traduzidas: "Aqui está o porquê:" (*Here's why*), "Deixa eu te contar" (*Let me tell you*), "Uma coisa que aprendi é que..." (*One thing I learned is*), "Isso dito," (*That said*), "Spoiler:", "Plot twist:".
- "X é sobre Y" (*X is about Y*): "Liderança é sobre escutar". Sérgio Rodrigues, na Folha, trata o "é sobre isso" como modismo importado. Melhor: "Liderar, para mim, é principalmente escutar" ou, de novo, um caso.

Ruim:
> Como desenvolvedor, uma coisa que eu aprendi é que testes são sobre confiança. Aqui está o porquê:

Melhor:
> Sem teste no módulo financeiro eu não durmo na véspera de fechamento de mês. Foi isso que me fez escrever os primeiros, em 2021.

### 14. Conectivos de redação

Por que soa artificial: "além disso", "ademais", "vale ressaltar", "vale destacar", "é importante destacar", "cabe salientar", "nesse sentido", "nesse contexto", "dessa forma", "diante disso", "sendo assim", "em suma", "em resumo", "por fim". São conectivos de redação do Enem e de relatório. O equivalente em inglês ("Additionally", "It's important to note") aparece nas listas de palavras super-representadas em texto de LLM (Kobak et al. incluíram "additionally" no grupo de dez palavras comuns que usaram para estimar o uso de LLM em resumos científicos de 2024). Em post curto, quase sempre dá para cortar ou trocar por "e", "mas", "só que", "então", "aí" ou ponto final.

Ruim:
> Além disso, vale ressaltar que o módulo de matrícula foi reescrito. Nesse sentido, é importante destacar que o tempo de cadastro caiu. Em suma, a experiência melhorou.

Melhor:
> Também reescrevemos a matrícula. Cadastrar um aluno levava 12 minutos; agora leva 4.

---

## Parte 3. Vocabulário

### 15. Calques lexicais e corporativês traduzido

Por que soa artificial: palavra portuguesa com sentido inglês, ou expressão inglesa traduzida palavra por palavra. Sérgio Rodrigues chama isso de "tradução preguiçosa": a que não considera as características da língua de destino. Algumas acabam pegando ("dar-se conta" foi galicismo condenado em 1938 e hoje ninguém nota). Para os textos deste guia, a pergunta é se a expressão ainda soa a tradução para um leitor brasileiro. As abaixo soam.

| Evitar | Vem de | Por que incomoda | Usar no lugar |
|---|---|---|---|
| endereçar um problema | *address* | Em português, endereça-se carta. Sérgio Rodrigues: "anglicismo tosco" do corporativês. | resolver, tratar de, atacar, responder a |
| no final do dia | *at the end of the day* | Calque que virou bordão corporativo; em PT literal, quer dizer "às 18h". | no fim das contas, no fundo, ou cortar |
| fazer sentido / faz todo o sentido | *make sense* | Está dicionarizado e é correto (Ciberdúvidas, citando o Houaiss). O problema é o uso como bordão sem argumento, como o próprio Ciberdúvidas observa sobre "não faz sentido". | dizer a razão; "tem lógica", "concordo", "bate com o que vi na escola X" |
| jornada (do cliente, de transformação, "minha jornada") | *journey* | Palavra-muleta de LLM e de marketing; esconde as etapas. | trajetória, os anos de...; ou nomear as etapas: "do primeiro contato até a matrícula" |
| alavancar, potencializar, impulsionar | *leverage, boost* | Verbo de apresentação de consultoria. | usar, aproveitar, aumentar, ou o número |
| robusto | *robust* | Adjetivo-coringa (está nas listas da Wikipedia e de detectores). | dizer o que aguenta: "aguenta 300 requisições por segundo", "não cai quando o gateway de pagamento cai" |
| mergulhar, mergulho profundo | *delve, deep dive* | "Delve" é o marcador de LLM mais estudado (Kobak et al.). | olhar em detalhe, destrinchar, ou só começar o assunto |
| entregar valor, entregar resultado | *deliver value* | Sérgio Rodrigues mostra o "entregar" ampliado vindo do *deliver*; antes usávamos dar, trazer, oferecer. | dizer o que o cliente ganhou |
| aprendizados | *learnings* | Plural contável é molde inglês. | o que aprendi, lições |
| realizar (= perceber) | *realize* | Falso cognato. | perceber, notar, cair a ficha |
| eventualmente (= no fim) | *eventually* | Em português, "eventualmente" é "de vez em quando". Muda o sentido. | no fim, com o tempo, acabou que |
| assumir (= supor) | *assume* | Em português, assumir é tomar para si. | supor, partir do princípio |
| suportar (= ser compatível) | *support* | Ambíguo: "o app suporta Android 8" parece "tolera". | funciona em, é compatível com, aceita |
| mover a agulha, dobrar a aposta, divisor de águas, ganha-ganha | *move the needle, double down, game changer, win-win* | Expressões traduzidas que só existem no LinkedIn. | dizer o efeito concreto |
| impactar positivamente | *positively impact* | Verbo vago de relatório. | melhorar, reduzir, aumentar + o quê |

Jargão técnico estabelecido (deploy, PR, merge, escalar no sentido de infraestrutura, churn, onboarding) pode ficar quando o público é dev ou SaaS. Em post para gestor de escola, troque por português ou explique uma vez.

### 16. Vocabulário inflado e verbo que foge do "é"

Por que soa artificial: estudos de corpus mostram que LLMs usam certas palavras de estilo muito acima do normal. Kobak et al. analisaram 14 milhões de resumos do PubMed e acharam um salto em 2024 de palavras como *delves*, *showcasing*, *underscores*, *crucial*, *potential*, *additionally*. As listas da Wikipedia e da Pangram têm os equivalentes. Em PT-BR, os mais comuns são: crucial, fundamental, essencial, robusto, panorama, cenário, ecossistema, sinergia, transformador, inovador, significativo, destacar, ressaltar, evidenciar, reforçar ("o que reforça a importância de"), "desempenha um papel crucial", "um verdadeiro testemunho de".

Junto vem a fuga do verbo simples: em vez de "é" e "tem", o texto usa "se consolida como", "atua como", "se posiciona como", "conta com", "oferece", "representa um marco". A Wikipedia registra a queda de "is/are" em texto revisado por IA.

Ruim:
> A plataforma se consolida como uma solução robusta e conta com um ecossistema de integrações que desempenha um papel crucial na transformação digital das escolas.

Melhor:
> A plataforma integra com os três ERPs que as escolas da nossa base mais usam e com o Pix do Banco do Brasil.

Regra prática: no máximo uma palavra dessa lista por post, e só se nenhuma palavra concreta couber no lugar.

### 17. Sinônimo que gira

Por que soa artificial: o modelo evita repetir palavra e troca o mesmo referente a cada frase: "a plataforma", "a solução", "a ferramenta", "o sistema", "o produto". O leitor fica procurando a diferença entre cinco coisas que são uma só.

Ruim:
> A plataforma emite boletos. A solução também concilia pagamentos, e a ferramenta ainda manda lembrete aos pais.

Melhor:
> O sistema emite o boleto, dá baixa quando o pagamento cai e manda lembrete aos pais.

Escolha um nome por coisa e repita sem medo.

---

## Parte 4. Pontuação e formatação

### 18. Travessão (regra: zero)

Por que soa artificial: o travessão existe na norma do português e escritor bom usa. O problema é a frequência e o uso como pausa dramática ("O resultado — inesperado — foi..."), ou colado no estilo inglês ("deploy—e caiu"). A Wikipedia registra o excesso como sinal (e anota que alguns modelos recentes passaram a evitá-lo, enquanto outros ainda abusam), e o repositório unslop, com camada específica para PT-BR, o trata como o sinal número um em texto brasileiro, porque quase ninguém digita travessão no teclado ABNT2.

Ruim:
> A migração — que parecia simples — levou três meses. E a lição — dolorosa — foi clara: medir antes de prometer.

Melhor:
> A migração parecia simples e levou três meses. Prometi um prazo antes de medir o tamanho da base.

Regra: zero travessão, sem exceção. Vale para o travessão (—), para a meia-risca usada como travessão (–) e para o hífen solto entre espaços, que faz o mesmo papel. Troque por vírgula (aposto curto), ponto (duas ideias que se sustentam sozinhas), dois-pontos (a segunda parte explica a primeira) ou parênteses (comentário lateral de verdade). Em intervalo numérico, escreva "de 2019 a 2021" ou use hífen sem espaço (2019-2021). Hífen de palavra composta (e-mail, segunda-feira) continua normal.

### 19. Negrito, emoji, hashtag e formatação de LinkedIn

Por que soa artificial: negrito em três expressões por parágrafo, emoji como marcador de lista (🚀 ✅ 💡 👇), bloco de hashtags no fim, título em Title Case ("Como Reduzimos O Churn"), bullet com rótulo em negrito e dois-pontos ("**Velocidade:** ..."), e uma frase por linha com quebra dupla entre todas. Tudo isso está documentado como padrão de chatbot na Wikipedia e nos guias de humanizer. No LinkedIn, a WIRED relatou estimativa da Originality AI de que mais da metade dos posts longos em inglês já eram provavelmente gerados por IA no fim de 2024; o leitor está calejado com esse visual.

Ruim:
> 🚀 **3 Lições Que Aprendi Escalando Um SaaS Para Escolas**
>
> ✅ **Foco:** menos é mais.
>
> ✅ **Cliente:** escute antes de construir.
>
> ✅ **Time:** cultura come estratégia no café da manhã.
>
> #SaaS #Educação #Liderança #Startups #Tecnologia #Inovação

Melhor:
> No primeiro ano, fizemos tudo que as escolas pediram. Em dezembro tínhamos 40 telas que só uma escola usava. Em 2024 cortamos 22 delas, e o suporte caiu pela metade.

Regras: sem negrito no corpo (no máximo um destaque no texto inteiro, se for indispensável); zero emoji por padrão (nem como marcador, nem no fim da frase); zero hashtag por padrão, só se o usuário pedir; título e frases em caixa de frase (só a primeira letra e nomes próprios em maiúscula); parágrafos curtos podem, mas com frases completas e tamanhos variados.

---

## Como reescrever sem criar outro vício

- Não troque um tique por outro. Tirar o "Além disso" e pôr "Fora isso" no começo de toda frase dá no mesmo.
- "Mais humano" não quer dizer mais gíria. Nada de "mano", "papo reto", "bagulho" para compensar. O registro padrão (o do Ricardo) é de fundador falando com colega: direto, em primeira pessoa quando é experiência dele, com termo técnico exato.
- Precisão técnica vem antes de estilo. Não troque "fila com retry e idempotência" por "um jeito de não duplicar" se o público é dev.
- Varie o tamanho das frases. Uma longa, uma curta, outra média. Texto todo em frases de oito palavras também soa a máquina.
- Leia em voz alta. Se você não diria aquilo numa conversa com um dev do time ou com a diretora de uma escola cliente, reescreva.
- Repetir palavra é permitido. Repetir estrutura é que cansa.

---

## Checklist de revisão (rodar antes de entregar)

Responda sim ou não. Qualquer "sim" nas perguntas 1 a 16 pede correção, a não ser que haja motivo explícito para manter.

1. Alguma frase segue o molde "não é X, é Y", "mais do que X", "não apenas X, mas também Y" ou "X, e não Y" sem que o X seja uma crença real do leitor?
2. Há trinca de adjetivos, benefícios ou frases curtas que não precisava ser trinca?
3. O post termina com frase de efeito, aforismo ou linha solta que repete o parágrafo anterior?
4. Há estrutura espelhada tipo "Antes/Depois", "Ontem/Hoje", "Menos X, mais Y"?
5. Há pergunta que o próprio texto responde logo em seguida, ou pergunta final genérica tipo "E você?"?
6. Há cena, diálogo ou detalhe sensorial que o autor não forneceu?
7. A primeira frase pode ser cortada sem perda (aquecimento, "no cenário atual", "neste post vou")?
8. Alguma afirmação geral está sem caso, número ou nome ao lado? Há "estudos mostram" sem estudo citado?
9. Há meta-comentário ("o ponto aqui é", "vale olhar com carinho", "sendo bem honesto", "não estou dizendo que") ou ressalva empilhada?
10. Há passiva analítica ou fórmula impessoal ("foi decidido", "foi identificado", "faz-se necessário") onde dava para dizer quem fez?
11. Há gerundismo ("vou estar + -ndo") ou gerúndio pendurado no fim da frase ("garantindo", "permitindo", "reforçando")?
12. "Eu", "você" ou "seu/sua" aparecem em quase toda frase? Algum "seu/sua" está ambíguo?
13. Há molde inglês: "Como fundador, eu...", "Aqui está o porquê", "Uma coisa que aprendi é", "X é sobre Y"?
14. Há conectivo de redação ("além disso", "vale ressaltar", "nesse sentido", "em suma", "é importante destacar")?
15. Há algum termo da tabela de calques (endereçar, no final do dia, jornada, alavancar, robusto, mergulhar, entregar valor, eventualmente, realizar = perceber) ou mais de uma palavra inflada (crucial, fundamental, ecossistema, transformador...)?
16. Há travessão (— ou –, ou hífen solto fazendo papel de travessão), negrito no corpo, emoji, hashtag ou Title Case?
17. O mesmo referente aparece com três ou mais nomes diferentes?
18. Todos os parágrafos ou bullets têm o mesmo tamanho e a mesma estrutura?
19. Algum fato, número, nome ou episódio entrou no texto sem ter vindo do autor? (Se sim, remover ou marcar `[FALTA DADO]`.)
20. Lido em voz alta, o texto soa como o autor falando com um colega? (Este é o único em que a resposta esperada é "sim".)

### Varredura mecânica

Busca literal para rodar no rascunho antes da leitura atenta. O caminho principal é o scanner da skill: `python3 scripts/check.py rascunho.md` (só biblioteca padrão do Python, pula blocos de código e código inline, mostra linha, coluna, padrão e sugestão; `--list` mostra as regras). Ele cobre as linhas abaixo e mais algumas heurísticas (trinca de abstrações, pronome em excesso, sinônimo que gira, Title Case).

Sem Python, salve as linhas abaixo em `padroes.txt` e rode `rg -n -i -f padroes.txt rascunho.md` (testado com ripgrep). Uma ocorrência não condena a frase; mostra onde olhar.

```
—|–|\w - \w
\b(vou|vamos|vai|estarei|estaremos|estará) estar \w+ndo\b|\bestarei \w+ndo\b
, (garantindo|permitindo|reforçando|destacando|evidenciando|promovendo|contribuindo)
não é (só |apenas )?\w+.{0,40}(, é|\. É)|mais do que|não apenas|mas também|não se trata de
além disso|ademais|vale (ressaltar|destacar|lembrar)|é importante (destacar|ressaltar|notar)|cabe salientar|nesse sentido|nesse contexto|em suma|em resumo|sendo assim|diante disso
no cenário atual|nos dias de hoje|em um mundo cada vez mais|neste post|bora lá|vamos por partes|spoiler
o ponto (aqui )?é|a questão é|vale olhar com carinho|sendo (bem )?honesto|sinceramente\?|não estou dizendo
foi (decidido|identificado|desenvolvido|criado|lançado|realizado)|faz-se necessário|acredita-se
endereç(ar|ou|ando|amos|ado)\b|no final do dia|faz (todo o )?sentido|jornada|alavanc|potencializ|impulsion|robust|mergulh|entregar valor|aprendizados|eventualmente|divisor de águas|mover a agulha
crucial|fundamental|essencial|panorama|ecossistema|sinergia|transformador|inovador|significativ|papel (crucial|fundamental)|se consolida|conta com
estudos mostram|especialistas (apontam|afirmam)|pesquisas indicam
\*\*|#\w+|🚀|✅|💡|👇|🔥|🧵
O resultado\?|E o melhor\?|Você já parou
é sobre|aqui está o porquê|como (fundador|dev|desenvolvedor), eu
```

---

## Fontes consultadas

Todas abertas durante a pesquisa (6 de outubro de 2026).

Sinais de escrita de IA (geral)

- Wikipedia, "Wikipedia:Signs of AI writing" (WikiProject AI Cleanup). Base para antítese (*negative parallelism*), regra de três, vocabulário de IA por "era" de modelo, fuga do "is/are", gerúndio de análise superficial (*-ing*), excesso de negrito, travessão, emoji, Title Case, atribuição vaga e ênfase inflada. https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
- Kobak, González-Márquez, Horvát e Lause, "Delving into ChatGPT usage in academic writing through excess vocabulary" (arXiv 2406.07016). Excesso de palavras de estilo em 14 milhões de resumos do PubMed; lista de marcadores (*delves*, *showcasing*, *underscores*, *crucial*, *additionally*...). https://arxiv.org/html/2406.07016v4
- Pangram (Bradley Emi), "Guia completo para identificar padrões de escrita da IA" (versão em português). Listas de palavras e padrões de estrutura, tom e especificidade. https://www.pangram.com/pt/blog/comprehensive-guide-to-spotting-ai-writing-patterns
- WIRED, "Yes, That Viral LinkedIn Post You Read Was Probably AI-Generated" (26/11/2024). Estimativa da Originality AI sobre posts longos no LinkedIn. https://www.wired.com/story/linkedin-ai-generated-influencers/

Skills e prompts públicos de "humanizer"

- blader/humanizer, SKILL.md (v3.1.0), baseado na página da Wikipedia. Antítese, fecho de uma linha, "frases que soam profundas", aquecimento encenado, discutir com ninguém, trincas, travessão, regra de não inventar fato. https://raw.githubusercontent.com/blader/humanizer/main/SKILL.md (repositório: https://github.com/blader/humanizer)
- badmuriss/unslop, camada `references/ptbr.md`. Padrões específicos de PT-BR: travessão, aberturas cerimoniais, gerúndio de call center, vocabulário-muleta, corporativês traduzido, rotação de sinônimos, varredura mecânica. (Contém também regras de uma agência específica, que não foram adotadas aqui.) https://github.com/badmuriss/unslop/blob/a952141f/references/ptbr.md

Anglicismos e calques no português brasileiro

- Sérgio Rodrigues, "Endereçando a anglofilia", Folha de S.Paulo, 03/03/2021. "Endereçar" como anglicismo do corporativês e tradução preguiçosa; "realizar", "é sobre". https://www1.folha.uol.com.br/colunas/sergio-rodrigues/2021/03/enderecando-a-anglofilia.shtml
- Sérgio Rodrigues, "Por que estamos entregando tanto", Folha de S.Paulo, 26/07/2023. Estrangeirismo semântico em "entregar" (*deliver*) e outros do papo corporativo e tecnológico. https://www1.folha.uol.com.br/colunas/sergio-rodrigues/2023/07/por-que-estamos-entregando-tanto.shtml
- Sérgio Rodrigues, "Testei positivo para anglicismo", Folha de S.Paulo, 12/01/2022. Sintaxe decalcada do inglês; como alguns calques acabam incorporados. https://www1.folha.uol.com.br/colunas/sergio-rodrigues/2022/01/testei-positivo-para-anglicismo.shtml
- José Augusto Carvalho, "O 'gerundismo' é fruto de influência do inglês?", Revista Ensino Superior (da revista Língua Portuguesa), 08/03/2017. Argumenta contra a origem inglesa do gerundismo e explica quando a perífrase com gerúndio é legítima. https://revistaensinosuperior.com.br/2017/03/08/o-gerundismo-e-fruto-de-influencia-do-ingles/
- Mara Passos Guimarães e Ricardo Augusto Souza (UFMG), "Divergências entre a construção passiva no português brasileiro e no inglês: evidências de corpus oral", Scripta (PUC Minas), 2016. Diferença de distribuição da passiva entre PB e inglês; o dado de 1:7 contra 1:20 é de Duarte (1990), citado no artigo. https://periodicos.pucminas.br/index.php/scripta/article/view/P.2358-3428.2016v20n38p262
- Maria Eugenia Lamoglia Duarte e Juliana Esposito Marins, "Português brasileiro: língua de sujeito nulo 'parcial'?", Cadernos de Estudos Linguísticos (Unicamp), 2021. Mudança do PB em direção a sujeitos pronominais expressos. https://periodicos.sbu.unicamp.br/ojs/index.php/cel/article/view/8661660
- Małgorzata Wielgosz, "Algumas observações sobre os possessivos em português", Studia Romanica Posnaniensia 40/1, 2013. Omissão do possessivo na posse inalienável em português, ao contrário do inglês (estudo sobre o português europeu). https://pressto.amu.edu.pl/index.php/srp/article/download/570/493/959
- Ciberdúvidas da Língua Portuguesa, "«Ter sentido», «fazer sentido»" (Carlos Rocha, 2016). As duas formas são corretas e sinônimas; nota sobre "não faz sentido" usado como simples bordão. https://ciberduvidas.iscte-iul.pt/consultorio/perguntas/ter-sentido-fazer-sentido/33967
- Ciberdúvidas, "A expressão «faz todo o sentido»" (Carla Marques, 2021). https://ciberduvidas.iscte-iul.pt/consultorio/perguntas/a-expressao-faz-todo-o-sentido/36191
- Rosângela Villa Real, post no LinkedIn sobre "crucial", "robusto" e "no final do dia" como muletas associadas à IA (fonte de opinião, usada só como termômetro do incômodo do público brasileiro no LinkedIn). https://pt.linkedin.com/posts/rosangelavillarealpersonalbranding_personalbranding360-autenticidade-marcapessoal-activity-7267869939758231553-zC7E
