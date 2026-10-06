"""Testes do scanner. Rode na raiz do repositório: python3 -m unittest discover -s tests -v"""
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "anti-llmismo-ptbr"
SCRIPT = SKILL / "scripts" / "check.py"
sys.path.insert(0, str(SCRIPT.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import check  # noqa: E402
import examples  # noqa: E402


def ids(text, **kw):
    return {h.rule.id for h in check.scan_text(text, **kw)}


class ExemplosDoGuia(unittest.TestCase):
    def test_todo_exemplo_ruim_e_acusado(self):
        ruins = [t for k, _, t in examples.extract() if k == "ruim"]
        self.assertGreaterEqual(len(ruins), 29)
        for t in ruins:
            with self.subTest(t=t[:60]):
                self.assertTrue(check.scan_text(t), "exemplo ruim passou sem ocorrência")

    def test_nenhum_exemplo_melhor_e_acusado(self):
        bons = [t for k, _, t in examples.extract() if k == "melhor"]
        self.assertGreaterEqual(len(bons), 25)
        for t in bons:
            with self.subTest(t=t[:60]):
                hits = check.scan_text(t)
                self.assertEqual([], [(h.rule.id, h.text) for h in hits])


class Calques(unittest.TestCase):
    CASOS = {
        "enderecar": "Precisamos endereçar esse problema.",
        "final-do-dia": "No final do dia, o cliente quer resultado.",
        "faz-sentido": "Isso faz todo o sentido.",
        "jornada": "Conto aqui a minha jornada.",
        "alavancar": "Queremos alavancar as vendas.",
        "robusto": "Uma solução robusta.",
        "mergulhar": "Vamos mergulhar no tema.",
        "entregar-valor": "O foco é entregar valor ao cliente.",
        "aprendizados": "Meus aprendizados do ano.",
        "realizar-perceber": "Só então realizei que estava errado.",
        "realizar": "Erro ao realizar o pagamento.",
        "eventualmente": "Eventualmente migramos tudo para o Postgres.",
        "assumir": "Assumi que o campo era opcional.",
        "suportar": "O app suporta Android 8.",
        "corporatives": "Isso vai mover a agulha.",
        "impactar": "A mudança vai impactar positivamente o time.",
        "conectivo-redacao": "Além disso, o deploy ficou mais rápido.",
        "gerundismo": "Vou estar enviando o relatório.",
        "travessao": "A migração — enfim — acabou.",
        "meia-risca": "Funciona de 2019–2021.",
        "hifen-travessao": "A migração - que parecia simples - levou meses.",
        "emoji": "Lançamos hoje 🚀",
        "hashtag": "Novidade no ar #SaaS",
        "e-sobre": "Liderança é sobre escutar.",
        "title-case": "## Como Reduzimos O Churn",
    }

    def test_cada_calque(self):
        for rule_id, txt in self.CASOS.items():
            with self.subTest(rule=rule_id):
                self.assertIn(rule_id, ids(txt))


class FalsosPositivos(unittest.TestCase):
    LIMPOS = [
        "Não é possível salvar o arquivo. É preciso estar conectado.",
        "Informe seu endereço de e-mail.",
        "Corrige #123 e fecha #45.",
        "Veja a seção [instalação](#instalacao).",
        "A cor padrão é #fafafa e o destaque é #0af.",
        "Crie sua conta com o Google.",
        "O arquivo tem mais do que 10 MB.",
        "O servidor deve estar funcionando agora.",
        "Pode estar acontecendo um erro de rede.",
        "Esta função retorna o total da conta com desconto.",
        "Escrevo em C# e F# nas horas vagas.",
        "Adiciona suporte a Pix no checkout.",
        '<a href="#topo">Voltar ao topo</a>',
        "Acesse https://exemplo.com/a-b#secao-final para detalhes.",
        "Use o e-mail da segunda-feira.",
        "## Como instalar no Windows",
        "- item de lista\n  - subitem",
        "| coluna | outra |\n|---|---|",
    ]

    def test_frases_limpas(self):
        for t in self.LIMPOS:
            with self.subTest(t=t):
                self.assertEqual(set(), ids(t))


class Markdown(unittest.TestCase):
    def test_pula_bloco_de_codigo(self):
        txt = "Texto limpo.\n\n```python\nprint('Além disso — robusto')\n```\n\n~~~\njornada\n~~~\n"
        self.assertEqual(set(), ids(txt))

    def test_pula_codigo_inline(self):
        self.assertEqual(set(), ids("Evite `endereçar` e `—` no texto."))

    def test_no_markdown_varre_tudo(self):
        self.assertIn("enderecar", ids("Evite `endereçar`.", markdown=False))

    def test_marcadores_ignore(self):
        self.assertEqual(set(), ids("Além disso, ok. <!-- anti-llmismo: ignore -->"))
        txt = "<!-- anti-llmismo: off -->\nAlém disso, jornada.\n<!-- anti-llmismo: on -->\nTexto limpo."
        self.assertEqual(set(), ids(txt))

    def test_linha_e_coluna(self):
        hits = check.scan_text("Linha limpa.\nUm texto — com travessão.")
        self.assertEqual((2, 10), (hits[0].line, hits[0].col))


class Cli(unittest.TestCase):
    def run_cli(self, *args, stdin=""):
        return subprocess.run([sys.executable, str(SCRIPT), *args], input=stdin.encode("utf-8"),
                              capture_output=True)

    def test_codigos_de_saida(self):
        self.assertEqual(0, self.run_cli(stdin="Texto limpo.\n").returncode)
        r = self.run_cli(stdin="Vamos estar liberando amanhã.\n")
        self.assertEqual(1, r.returncode)
        self.assertIn("<stdin>:1:1: [gerundismo]", r.stdout.decode("utf-8"))
        self.assertEqual(2, self.run_cli("--only", "nao-existe", stdin="x").returncode)
        self.assertEqual(2, self.run_cli("/caminho/que/nao/existe.md").returncode)

    def test_text_e_json(self):
        r = self.run_cli("--json", "--text", "Além disso, ok.")
        self.assertEqual(1, r.returncode)
        self.assertIn('"rule": "conectivo-redacao"', r.stdout.decode("utf-8"))


class ArquivosDaSkill(unittest.TestCase):
    def test_textos_proprios_sem_ocorrencias(self):
        for p in [SKILL / "SKILL.md", SKILL / "references" / "checklist.md", ROOT / "README.md"]:
            with self.subTest(arquivo=p.name):
                hits = check.scan_text(p.read_text(encoding="utf-8"), str(p))
                self.assertEqual([], [(h.line, h.rule.id, h.text) for h in hits])

    def test_frontmatter(self):
        import re
        txt = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        fm = re.match(r"^---\n(.*?)\n---\n", txt, re.S).group(1)
        name = re.search(r"^name: (.+)$", fm, re.M).group(1).strip()
        desc = re.search(r"^description: (.+)$", fm, re.M).group(1).strip()
        self.assertEqual(SKILL.name, name)
        self.assertRegex(name, r"^[a-z0-9]+(-[a-z0-9]+)*$")
        self.assertLessEqual(len(name), 64)
        self.assertTrue(0 < len(desc) <= 1024)


if __name__ == "__main__":
    unittest.main()
