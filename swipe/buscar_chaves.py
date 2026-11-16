# Swipe Purge: busca no admin as chaves que esta maquina usa (cifradas la) e imprime
# "export NOME='valor'" para o shell. Sem ADMIN_URL/POSTIZ_ADMIN_TOKEN nao faz nada.
import json, os, re, sys, urllib.request

url = os.getenv("ADMIN_URL")
token = os.getenv("POSTIZ_ADMIN_TOKEN")
if not url or not token:
    print("[swipe] sem ADMIN_URL/POSTIZ_ADMIN_TOKEN: chaves nao carregadas", file=sys.stderr)
    sys.exit(0)
PERMITIDAS = re.compile(r"^(DEEPSEEK|PEXELS)_API_KEY$")
try:
    req = urllib.request.Request(url.rstrip("/") + "/api/postiz/chaves",
                                 headers={"Authorization": "Bearer " + token,
                                          "User-Agent": "swipe-ferramentas/1.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        chaves = json.load(r)
    n = 0
    for k, v in chaves.items():
        if PERMITIDAS.match(k) and isinstance(v, str):
            print("export %s='%s'" % (k, v.replace("'", "'\''")))
            n += 1
    print("[swipe] %d chaves carregadas do admin" % n, file=sys.stderr)
except Exception as e:
    print("[swipe] falha ao buscar chaves no admin: %s" % (type(e).__name__ + " " + str(getattr(e, "code", ""))), file=sys.stderr)
