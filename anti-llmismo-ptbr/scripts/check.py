#!/usr/bin/env python3
"""Varredura de LLMismos e calques do inglês em textos pt-BR.

Uso:
    python3 check.py arquivo.md [outro.txt ...]
    git log -1 --format=%B | python3 check.py
    python3 check.py --text "Vamos estar enviando o relatório."
    python3 check.py --list

Saída: arquivo:linha:coluna: [id] Nome: "trecho". Sugestão: ...
Código de saída: 0 sem ocorrências, 1 com ocorrências, 2 erro de uso ou leitura.

Por padrão, blocos de código cercados (``` ou ~~~), código inline, URLs e
destinos de link em Markdown são ignorados. Use --no-markdown para varrer tudo.

Para silenciar uma linha, coloque nela o marcador "anti-llmismo: ignore"
(por exemplo, num comentário HTML). Para silenciar um trecho, cerque-o com
"anti-llmismo: off" e "anti-llmismo: on".

Achar não é condenar: cada ocorrência é um ponto para olhar com atenção.
Só depende da biblioteca padrão do Python 3.8+.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from typing import Callable, Iterable, List, Optional, Tuple

FLAGS = re.IGNORECASE | re.UNICODE


@dataclass
class Rule:
    id: str
    name: str
    pattern: "re.Pattern[str]"
    hint: str
    keep: Optional[Callable[["re.Match[str]", str], bool]] = None


@dataclass
class Hit:
    path: str
    line: int
    col: int
    rule: Rule
    text: str
    hint: str = ""

    def as_dict(self) -> dict:
        return {
            "path": self.path,
            "line": self.line,
            "col": self.col,
            "rule": self.rule.id,
            "name": self.rule.name,
            "text": self.text,
            "hint": self.hint or self.rule.hint,
        }


def _r(rule_id: str, name: str, pattern: str, hint: str, keep=None, flags=FLAGS) -> Rule:
    return Rule(rule_id, name, re.compile(pattern, flags), hint, keep)


def _hashtag_keep(m: "re.Match[str]", line: str) -> bool:
    word = m.group("h")
    # cor hexadecimal (#fff, #fafafa) não é hashtag
    if re.fullmatch(r"[0-9a-fA-F]{3}|[0-9a-fA-F]{4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8}", word):
        return False
    return True


ABSTRATO = r"\w+(?:ção|ções|dade|dades|ência|ências|ância|âncias|ança|anças|eza|ezas|ismo|ismos|mento|mentos)"

EMOJI = (
    "["
    "\U0001F000-\U0001F2FF"  # mahjong, cartas, letras e flags
    "\U0001F300-\U0001F5FF"  # símbolos e pictogramas
    "\U0001F600-\U0001F64F"  # rostos
    "\U0001F680-\U0001F6FF"  # transporte e mapas
    "\U0001F700-\U0001FAFF"  # suplementares
    "\u2600-\u27BF"          # símbolos diversos e dingbats (✅ ✔ ✨ ❌ ⚡)
    "\u2B00-\u2BFF"          # setas e estrelas (⭐ ⬆)
    "\u2300-\u23FF"          # técnicos (⌛ ⏰)
    "\uFE0F"
    "]"
)

RULES: List[Rule] = [
    # ---------------------------------------------------------------- pontuação
    _r("travessao", "Travessão",
       r"—",
       "Zero travessão. Troque por vírgula (aposto curto), ponto (duas ideias), "
       "dois-pontos (explicação) ou parênteses (comentário lateral)."),
    _r("meia-risca", "Meia-risca usada como travessão",
       r"–",
       "Zero travessão, inclusive a meia-risca. Use vírgula, ponto, dois-pontos ou parênteses. "
       "Em intervalo numérico, escreva \"de 2019 a 2021\" ou use hífen sem espaço."),
    _r("hifen-travessao", "Hífen com espaços no lugar de travessão",
       r"(?<=[\w\)\"”'])\s(?:-{1,2})\s(?=[\w\(\"“'])",
       "Hífen solto entre espaços funciona como travessão. Troque por vírgula, ponto, "
       "dois-pontos ou parênteses."),
    _r("emoji", "Emoji",
       EMOJI + "+",
       "Sem emoji em prosa, nem como marcador de lista. Tire ou troque por texto."),
    _r("hashtag", "Hashtag",
       r"(?<![\w&/#\[(:=\"'])#(?P<h>[^\W\d_][\w-]*)",
       "Sem hashtag por padrão. Só use se o usuário pedir.",
       keep=_hashtag_keep),
    _r("negrito", "Negrito no corpo do texto",
       r"\*\*[^*\n]+?\*\*|(?<!\w)__[^_\n]+?__(?!\w)",
       "Evite negrito no corpo, sobretudo rótulo em negrito com dois-pontos. "
       "No máximo um destaque no texto inteiro, se for indispensável."),

    # ------------------------------------------------------ estrutura retórica
    _r("trinca-abstrata", "Trinca de substantivos abstratos",
       ABSTRATO + r",\s+" + ABSTRATO + r",?\s+e\s+" + ABSTRATO + r"\b",
       "Trinca de abstrações intercambiáveis soa a folder. Fique com o item que tem "
       "fato por trás, ou troque por um número ou caso."),
    _r("trinca-paralela", "Trinca de orações espelhadas",
       r"\b(\w{4})\w*\b[^,.;\n]{0,30},\s[^,.;\n]{0,30}\b\1\w*[^,.;\n]{0,30}\se\s[^,.;\n]{0,30}\b\1\w*",
       "Três orações com o mesmo molde viram slogan. Conte o fato mais concreto e corte o resto."),
    _r("nao-e-x-e-y", "Antítese \"não é X, é Y\"",
       r"\bnão\s(?:é|era|foi|são|se\strata)(?:\s(?:só|apenas|somente|sobre|de|do|da))?\s"
       r"(?!possível|necessári|permitid|obrigatóri|válid|suportad|compatível|recomendad|preciso|seguro)"
       r"[^.!?\n]{1,60}?(?:,\sé|[.;:]\sé|,\se\ssim|,\smas\ssim)\b",
       "A primeira metade nega algo que ninguém disse. Diga só a afirmação, com o fato que a sustenta."),
    _r("mais-do-que", "\"Mais do que X\" abrindo frase",
       r"(?:^[\s>*\-]*|[.!?]\s+)(?P<h>mais\s(?:do\s)?que)\b",
       "Abertura \"Mais do que X, Y\" é antítese de enfeite. Diga o que a coisa faz."),
    _r("nao-apenas", "\"Não apenas X, mas também Y\"",
       r"\bnão\s(?:apenas|só|somente)\b(?=[^.!?\n]{0,100}\bmas\s(?:também|ainda|sim)\b)",
       "Liste as duas coisas sem a moldura: \"emite o boleto e dá baixa sozinho\"."),
    _r("e-nao", "\"X, e não Y\"",
       r",\se\snão\b",
       "Confira se o leitor acredita mesmo no Y negado. Se não acredita, corte a negação."),
    _r("fecho-efeito", "Frase de efeito",
       r"\b(?:pense\snisso|simples\sassim|isso\smuda\studo|leia\s(?:de\snovo|outra\svez)|"
       r"menos\sé\smais|fica\sa\s(?:reflexão|dica)|reflita\ssobre\sisso)\b",
       "Termine no fato mais concreto e pare. Sem aforismo no fim."),
    _r("antes-depois", "Paralelismo simétrico",
       r"\bantes:[^\n]*\bdepois:|\bontem\b[^.!?\n]{0,60}[.!?]\s+hoje\b|\bmenos\s\w+,\s+mais\s\w+",
       "Estrutura espelhada tem ritmo de slogan. Conte o que mudou com números ou um caso."),
    _r("pergunta-engajamento", "Pergunta retórica de engajamento",
       r"\b(?:o\sresultado|e\so\smelhor|e\so\spior|o\smotivo|a\sresposta|o\ssegredo|a\ssolução|"
       r"o\sproblema|resultado)\?|\bvocê\sjá\s(?:parou\s(?:pra|para)\spensar|se\sperguntou)|"
       r"\be\svocê\?|\bcomenta\saí\b|\bdeixa\s(?:aqui\s)?nos\scomentários|\bconcorda\?|"
       r"\bvale\sa\spena\?\s*depende",
       "Afirme direto. Pergunta só se o autor quer mesmo ouvir a resposta, e específica."),
    _r("cena-inventada", "Cena ou detalhe dramático",
       r"\bo\scafé\s(?:já\s)?(?:tinha\s)?esfri\w*|\bvoz\strêmula|\beram\s\d{1,2}h\d{0,2}\sda\s(?:manhã|madrugada|noite)|"
       r"\bolhei\spara\sa\stela|\bnaquele\smomento,?\s(?:eu\s)?(?:entendi|percebi)|\be\sagora\?|"
       r"^[\s>]*(?:segunda|terça|quarta|quinta|sexta)(?:-feira)?,\s\d{1,2}h|^[\s>]*(?:sábado|domingo),\s\d{1,2}h",
       "Cena só se o autor contou o episódio, e só com os detalhes que ele deu. Vá direto ao fato."),
    _r("abertura-cerimonial", "Abertura cerimonial ou tom de newsletter",
       r"\b(?:no\scenário\satual|nos\sdias\sde\shoje|em\sum\s(?:mundo|cenário|mercado)\scada\svez\smais|"
       r"num\s(?:mundo|cenário|mercado)\scada\svez\smais|neste\spost|nesse\spost|neste\sartigo,?\svou|"
       r"bora\slá|vamos\spor\spartes|senta\sque\slá\svem|spoiler:|plot\stwist|salve\s(?:este|esse)\spost|"
       r"aqui\svai\so\sque\saprendi|lições\sque\saprendi|compartilha\scom\s(?:quem|alguém))",
       "Corte o aquecimento e comece pelo fato. Teste: tire a primeira frase e veja se fez falta."),
    _r("abstracao-vaga", "Abstração ou atribuição vaga",
       r"\b(?:estudos\s(?:mostram|indicam|apontam|comprovam)|especialistas\s(?:apontam|afirmam|dizem|garantem)|"
       r"pesquisas\s(?:indicam|mostram|apontam)|o\smercado\sjá\sentendeu|transformar\sa\seducação|"
       r"impacto\ssignificativo|alta\sperformance|papel\s(?:crucial|fundamental|essencial|importante)|cultura\sforte)",
       "Ponha caso, número ou nome ao lado. Estudo só com o estudo nomeado e linkado."),
    _r("meta-comentario", "Meta-comentário ou hedging",
       r"\b(?:o\sponto\s(?:aqui\s)?é|a\squestão\sé|o\sque\s(?:eu\s)?quero\sdizer|vale\solhar\scom\scarinho|"
       r"sendo\s(?:bem\s)?(?:honesto|sincero|honesta|sincera)|sinceramente[?:]|vou\sser\sdireto|"
       r"pode\sparecer\sóbvio|não\sestou\sdizendo\sque|de\scerta\sforma)",
       "Diga a coisa em vez de comentar o próprio texto. Ressalva só com conteúdo."),

    # ------------------------------------------------------------- sintaxe
    _r("passiva", "Voz passiva analítica",
       r"\b(?:foi|foram|será|serão|seria|seriam)\s(?:decidid|identificad|desenvolvid|criad|lançad|realizad|"
       r"implementad|disponibilizad|adicionad|removid|corrigid|atualizad|utilizad|feit|considerad|verificad|"
       r"constatad|observad|aprovad|definid)(?:o|a|os|as)\b",
       "Diga quem fez: \"lançamos\", \"a gente decidiu\", \"o script cria\"."),
    _r("impessoal", "Fórmula impessoal burocrática",
       r"\b(?:faz-se\snecessári\w*|fez-se\snecessári\w*|acredita-se|verificou-se|observou-se|constatou-se|"
       r"é\spossível\safirmar)",
       "Diga quem fez ou quem acha. \"Precisamos\", \"achamos\", \"vimos\"."),
    _r("gerundismo", "Gerundismo",
       r"\b(?:vou|vamos|vai|vão|irei|iremos|irá|irão)\sestar\s\w+ndo\b|"
       r"\b(?:estarei|estaremos|estará|estarão)\s\w+ndo\b",
       "Use o verbo direto: \"envio\", \"vamos enviar\", \"liberamos amanhã\"."),
    _r("gerundio-rabicho", "Gerúndio pendurado no fim da frase",
       r",\s(?:garantindo|permitindo|reforçando|destacando|evidenciando|promovendo|contribuindo|proporcionando|"
       r"possibilitando|assegurando|ressaltando|demonstrando|fortalecendo|consolidando|impulsionando|potencializando)\b",
       "Ponha ponto final e escreva uma frase nova com sujeito e um fato. Ou corte o gerúndio."),
    _r("pronome-denso", "Pronome ou possessivo em excesso",
       r"$^",  # tratado à parte, por frase
       "Português marca a pessoa no verbo e dispensa o possessivo óbvio. Corte \"eu\", \"você\", \"seu\", \"meu\" sobrando."),
    _r("molde-ingles", "Molde de frase do inglês",
       r"\bcomo\s(?:um\s|uma\s)?(?:fundador|fundadora|dev|desenvolvedor|desenvolvedora|ceo|cto|líder|gestor|gestora|"
       r"engenheiro|engenheira|programador|programadora|empreendedor|empreendedora|professor|professora),|"
       r"\baqui\s(?:está|vai)\so\sporquê|\bdeix[ae]\seu\ste\scontar|\bdeixe-me\s(?:te\s)?contar|"
       r"\buma\scoisa\sque\s(?:eu\s)?aprendi|\bisso\sdito,|\bdito\sisso,",
       "Molde traduzido (As a founder, Here's why, Let me tell you, That said). Reescreva com fato e data."),
    _r("e-sobre", "\"X é sobre Y\"",
       r"\b(?:é|são|era|foi)\ssobre\b",
       "\"X é sobre Y\" vem de \"X is about Y\". Diga o que X é ou faz, ou dê um caso."),
    _r("adjetivo-anteposto", "Adjetivo de valor anteposto",
       r"\b(?:um|uma)\s(?:incrível|enorme|importante|valios[oa]|poderos[oa]|verdadeir[oa]|imens[oa]|tremend[oa])\s"
       r"(?:experiência|aprendizado|lição|oportunidade|jornada|conquista|testemunho|marco|desafio|ferramenta|solução)",
       "Diga o que se aprendeu ou ganhou em vez de qualificar: \"aprendi que...\"."),
    _r("conectivo-redacao", "Conectivo de redação",
       r"\b(?:além\sdisso|ademais|vale\s(?:ressaltar|destacar|lembrar|mencionar|notar)|"
       r"é\simportante\s(?:destacar|ressaltar|notar|lembrar|mencionar|salientar)|cabe\s(?:salientar|ressaltar|destacar)|"
       r"nes[st]e\ssentido|nes[st]e\scontexto|des[st]a\sforma|diante\sdisso|sendo\sassim|em\ssuma|em\sresumo|por\sfim)\b",
       "Corte ou troque por \"e\", \"mas\", \"só que\", \"então\" ou ponto final."),

    # --------------------------------------------------------- vocabulário
    _r("enderecar", "Calque \"endereçar\" (address)",
       r"\bendereç(?:ar|ou|ando|amos|aram|ará|arão|aria|a|am|em|e|ei|ado|ada|ados|adas)\b",
       "Use resolver, tratar de, atacar, responder a. (\"Endereço\" de e-mail ou IP está certo.)"),
    _r("final-do-dia", "Calque \"no final do dia\" (at the end of the day)",
       r"\b(?:no|ao)\sfinal\sdo\sdia\b",
       "Se não é literal (horário), use \"no fim das contas\", \"no fundo\", ou corte."),
    _r("faz-sentido", "Bordão \"faz sentido\"",
       r"\b(?:faz|fazer|fazem|fez|faria|fará|fazia)(?:\stodo\so|\stodo|\smuito|\stotal|\smais)?\ssentido\b",
       "Diga a razão. \"Tem lógica\", \"concordo\", ou o argumento em si."),
    _r("jornada", "Palavra-muleta \"jornada\"",
       r"\bjornadas?\b",
       "Nomeie as etapas (\"do primeiro contato até a matrícula\") ou use trajetória."),
    _r("alavancar", "Verbo de consultoria",
       r"\b(?:alavanc|potencializ|impulsion)\w*",
       "Use usar, aproveitar, aumentar, ou dê o número."),
    _r("robusto", "Adjetivo-coringa \"robusto\"",
       r"\brobust(?:o|a|os|as|ez)\b",
       "Diga o que aguenta: \"aguenta 300 requisições por segundo\"."),
    _r("mergulhar", "Calque \"mergulhar\" (delve, deep dive)",
       r"\bmergulh\w*|\bdeep\sdive\b",
       "Use olhar em detalhe, destrinchar, ou comece logo o assunto."),
    _r("entregar-valor", "Calque \"entregar valor\" (deliver value)",
       r"\bentreg\w*\s(?:de\s)?(?:valor|resultados?|impacto)\b",
       "Diga o que o cliente ganhou, com número se houver."),
    _r("aprendizados", "Calque \"aprendizados\" (learnings)",
       r"\baprendizados\b",
       "Use \"o que aprendi\" ou \"lições\"."),
    _r("realizar-perceber", "Falso cognato \"realizar\" = perceber",
       r"\brealiz\w*\sque\b",
       "Use perceber, notar, cair a ficha."),
    _r("realizar", "Verbo burocrático \"realizar\"",
       r"\brealiz(?:ar|a|am|ou|ei|amos|aram|ará|ado|ada|ados|adas|ando|ação|ações|e|em)\b(?!\sque\b)",
       "Troque pelo verbo específico: pagar, fazer, rodar, entrar, cadastrar."),
    _r("eventualmente", "Falso cognato \"eventualmente\"",
       r"\beventualmente\b",
       "Em português é \"de vez em quando\". Se a ideia é \"no fim\", use \"no fim\", \"com o tempo\", \"acabou que\"."),
    _r("assumir", "Falso cognato \"assumir\" = supor",
       r"\bassum\w*\sque\b",
       "Use supor, partir do princípio, contar com."),
    _r("suportar", "Falso cognato \"suportar\" = ser compatível",
       r"\bsuport(?:a|am|ar|ado|ada|ados|adas|ará|amos)\b",
       "Use funciona em, é compatível com, aceita."),
    _r("corporatives", "Expressão de LinkedIn traduzida",
       r"\b(?:mover\sa\sagulha|dobr\w*\sa\saposta|ganha-ganha|divisor\sde\ságuas|game[\s-]?changer)\b",
       "Diga o efeito concreto."),
    _r("impactar", "Verbo vago \"impactar\"",
       r"\bimpact(?:ar|a|am|ou|ando|ado|ada|ados|adas|aram|ará|aria)\b",
       "Use melhorar, reduzir, aumentar, atrasar, mais o quê e quanto."),
    _r("vocabulario-inflado", "Vocabulário inflado",
       r"\b(?:crucial|cruciais|fundamental|fundamentais|essencial|essenciais|panorama|ecossistema\w*|sinergia\w*|"
       r"transformador\w*|inovador\w*|significativ\w*|evidenci\w*)\b",
       "No máximo uma palavra dessas no texto, e só se nenhuma palavra concreta couber."),
    _r("verbo-fuga", "Verbo que foge do \"é\" e do \"tem\"",
       r"\b(?:se\sconsolida\w*|atua\scomo|se\sposiciona\w*\scomo|representa\sum\smarco|um\sverdadeiro\stestemunho|"
       r"desempenha\w*\sum\spapel|reforça\sa\simportância)|(?<!\bsua\s)(?<!\buma\s)(?<!\bna\s)(?<!\bda\s)(?<!\bde\s)"
       r"(?<!\bem\s)(?<!\ba\s)(?<!\bsem\s)(?<!\bnova\s)(?<!\bmesma\s)(?<!\bessa\s)(?<!\besta\s)(?<!\bcada\s)\bconta\scom\b",
       "Use o verbo simples: \"é\", \"tem\", \"faz\"."),
    _r("sinonimo-gira", "Sinônimo que gira",
       r"$^",  # tratado à parte, por parágrafo
       "Escolha um nome para a coisa e repita sem medo."),
    _r("title-case", "Título em Title Case",
       r"$^",  # tratado à parte
       "Use caixa de frase: só a primeira letra e nomes próprios em maiúscula."),
]

RULES_BY_ID = {r.id: r for r in RULES}

PRONOMES = re.compile(r"\b(?:eu|você|vocês|seu|sua|seus|suas|meu|minha|meus|minhas)\b", FLAGS)
SENTENCA = re.compile(r"[^.!?;]+[.!?;]?")
SINONIMOS = re.compile(r"\b(?:plataforma|solução|ferramenta|sistema|produto|aplicação|aplicativo|software)\b", FLAGS)
PALAVRAS_FUNCAO = {
    "o", "a", "os", "as", "um", "uma", "uns", "umas", "de", "do", "da", "dos", "das", "e", "ou", "que",
    "para", "pra", "com", "em", "no", "na", "nos", "nas", "por", "pelo", "pela", "ao", "à", "se", "sem",
}

FENCE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
INLINE_CODE = re.compile(r"(`+)(?:(?!\1).)+?\1")
URL = re.compile(r"https?://\S+|www\.\S+|<[^>\s]+@[^>\s]+>|<https?:[^>]+>")
LINK_DEST = re.compile(r"\]\([^)\s]*(?:\s\"[^\"]*\")?\)")
HTML_COMMENT = re.compile(r"<!--.*?-->")
HEADING = re.compile(r"^\s{0,3}#{1,6}\s+(.*)$")
BOLD_LINE = re.compile(r"^[\s>]*[^\w*]*\*\*(.+)\*\*\s*$")


def mask(s: str, pattern: "re.Pattern[str]", keep_brackets: bool = False) -> str:
    """Troca os trechos por espaços, preservando as colunas."""
    def repl(m: "re.Match[str]") -> str:
        txt = m.group(0)
        if keep_brackets:
            return "]" + " " * (len(txt) - 1)
        return " " * len(txt)
    return pattern.sub(repl, s)


def title_case_hit(text: str) -> bool:
    words = re.findall(r"[^\W\d_][\w'-]*", text)
    if len(words) < 3:
        return False
    rest = words[1:]
    # palavra de função com maiúscula no meio do título: sinal forte
    for w in rest:
        if w.lower() in PALAVRAS_FUNCAO and w[0].isupper() and (len(w) == 1 or not w.isupper()):
            return True
    conteudo = [w for w in rest if len(w) >= 4 and not w.isupper() and not any(c.isupper() for c in w[1:])]
    return len(conteudo) >= 3 and all(w[0].isupper() for w in conteudo)


def scan_text(text: str, path: str = "<stdin>", markdown: bool = True,
              only: Optional[set] = None, ignore: Optional[set] = None) -> List[Hit]:
    active = [r for r in RULES if (not only or r.id in only) and (not ignore or r.id not in ignore)]
    active_ids = {r.id for r in active}
    hits: List[Hit] = []
    seen = set()

    def add(lineno: int, col0: int, rule: Rule, snippet: str, hint: str = "") -> None:
        key = (lineno, col0, rule.id)
        if key in seen:
            return
        seen.add(key)
        hits.append(Hit(path, lineno, col0 + 1, rule, snippet.strip(), hint))

    in_fence = False
    fence_marker = ""
    off = False
    para: List[Tuple[int, str]] = []

    def flush_para() -> None:
        if "sinonimo-gira" in active_ids and para:
            nomes = {}
            for ln, txt in para:
                for m in SINONIMOS.finditer(txt):
                    nomes.setdefault(m.group(0).lower(), (ln, m.start()))
            if len(nomes) >= 3:
                ln, c = min(nomes.values())
                add(ln, c, RULES_BY_ID["sinonimo-gira"], ", ".join(sorted(nomes)))
        para.clear()

    lines = text.splitlines()
    for i, raw in enumerate(lines, start=1):
        if "anti-llmismo: off" in raw:
            off = True
            flush_para()
            continue
        if "anti-llmismo: on" in raw:
            off = False
            continue
        if markdown:
            fm = FENCE.match(raw)
            if fm:
                marker = fm.group(1)
                if not in_fence:
                    in_fence, fence_marker = True, marker
                elif marker[0] == fence_marker[0] and len(marker) >= len(fence_marker):
                    in_fence = False
                flush_para()
                continue
            if in_fence:
                continue
        if off or "anti-llmismo: ignore" in raw:
            continue

        line = raw
        if markdown:
            line = mask(line, HTML_COMMENT)
            line = mask(line, INLINE_CODE)
            line = mask(line, LINK_DEST, keep_brackets=True)
        line = mask(line, URL)

        if not line.strip():
            flush_para()
            continue
        para.append((i, line))

        for rule in active:
            if rule.pattern.pattern == "$^":
                continue
            for m in rule.pattern.finditer(line):
                if rule.keep and not rule.keep(m, line):
                    continue
                if "h" in rule.pattern.groupindex and m.group("h") is not None:
                    start, end = m.span("h")
                    if rule.id == "hashtag":
                        start -= 1
                else:
                    start, end = m.span()
                hint = ""
                if rule.id == "meia-risca":
                    before, after = line[:start].rstrip(), line[end:].lstrip()
                    if before[-1:].isdigit() and after[:1].isdigit():
                        hint = ("Intervalo com meia-risca. Escreva \"de 2019 a 2021\" "
                                "ou use hífen sem espaço (2019-2021).")
                add(i, start, rule, raw[start:end], hint)

        if "pronome-denso" in active_ids:
            for sm in SENTENCA.finditer(line):
                found = list(PRONOMES.finditer(sm.group(0)))
                if len(found) >= 3:
                    c = sm.start() + found[0].start()
                    add(i, c, RULES_BY_ID["pronome-denso"],
                        " ".join(f.group(0) for f in found))

        if "title-case" in active_ids:
            hm = HEADING.match(line) if markdown else None
            bm = BOLD_LINE.match(line)
            target = hm.group(1) if hm else (bm.group(1) if bm else None)
            if target is not None and title_case_hit(target):
                c = line.find(target)
                add(i, max(c, 0), RULES_BY_ID["title-case"], target)

    flush_para()
    hits.sort(key=lambda h: (h.line, h.col, h.rule.id))
    return hits


def read_source(path: str) -> str:
    if path == "-":
        data = sys.stdin.buffer.read()
    else:
        with open(path, "rb") as fh:
            data = fh.read()
    return data.decode("utf-8", errors="replace")


def parse_ids(value: Optional[str]) -> Optional[set]:
    if not value:
        return None
    ids = {v.strip() for v in value.split(",") if v.strip()}
    unknown = ids - set(RULES_BY_ID)
    if unknown:
        raise SystemExit(f"check.py: regra desconhecida: {', '.join(sorted(unknown))} (veja --list)")
    return ids


def main(argv: Optional[Iterable[str]] = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
        except Exception:
            pass

    ap = argparse.ArgumentParser(
        prog="check.py",
        description="Varre textos pt-BR atrás de LLMismos e calques do inglês.",
    )
    ap.add_argument("files", nargs="*", help="arquivos para varrer (sem arquivos ou com '-', lê da entrada padrão)")
    ap.add_argument("-t", "--text", action="append", help="varre o texto passado na linha de comando")
    ap.add_argument("--only", help="só estas regras (ids separados por vírgula)")
    ap.add_argument("--ignore", help="ignora estas regras (ids separados por vírgula)")
    ap.add_argument("--no-markdown", action="store_true",
                    help="não pula blocos de código, código inline nem destinos de link")
    ap.add_argument("--json", action="store_true", help="saída em JSON")
    ap.add_argument("--summary", action="store_true", help="só a contagem por regra")
    ap.add_argument("--list", action="store_true", help="lista as regras e sai")
    args = ap.parse_args(list(argv) if argv is not None else None)

    if args.list:
        for r in RULES:
            print(f"{r.id:22} {r.name}")
        return 0

    try:
        only, ignore = parse_ids(args.only), parse_ids(args.ignore)
    except SystemExit as e:
        print(e, file=sys.stderr)
        return 2

    sources: List[Tuple[str, str]] = []
    for idx, t in enumerate(args.text or [], start=1):
        sources.append((f"<texto{idx}>", t))
    files = args.files or ([] if args.text else ["-"])
    for f in files:
        try:
            sources.append(("<stdin>" if f == "-" else f, read_source(f)))
        except OSError as e:
            print(f"check.py: não consegui ler {f}: {e.strerror}", file=sys.stderr)
            return 2

    all_hits: List[Hit] = []
    for path, content in sources:
        all_hits.extend(scan_text(content, path, markdown=not args.no_markdown, only=only, ignore=ignore))

    if args.json:
        print(json.dumps([h.as_dict() for h in all_hits], ensure_ascii=False, indent=2))
    elif args.summary:
        counts = {}
        for h in all_hits:
            counts[h.rule.id] = counts.get(h.rule.id, 0) + 1
        for rid, n in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):
            print(f"{n:5}  {rid}")
    else:
        for h in all_hits:
            print(f"{h.path}:{h.line}:{h.col}: [{h.rule.id}] {h.rule.name}: \"{h.text}\". "
                  f"Sugestão: {h.hint or h.rule.hint}")

    if not args.json:
        n_files = len({h.path for h in all_hits})
        if all_hits:
            print(f"\n{len(all_hits)} ocorrência(s) em {n_files} fonte(s). "
                  "Achar não é condenar: releia cada trecho e reescreva a frase, sem só trocar sinônimo.",
                  file=sys.stderr)
        else:
            print("Nenhuma ocorrência.", file=sys.stderr)
    return 1 if all_hits else 0


if __name__ == "__main__":
    sys.exit(main())
