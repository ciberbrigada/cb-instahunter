#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
#   CB-INSTAHUNTER v2.0 — Ciberbrigada OSINT Suite
#   Instagram OSINT — Datos reales en terminal, sin login
#   Uso exclusivo para fines legales y educativos
# ═══════════════════════════════════════════════════════════════════════════════

import sys
import os
import re
import json
import time
import random
import hashlib
import datetime
from collections import Counter

try:
    import requests
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    os.system("pip install requests colorama --break-system-packages -q")
    import requests
    from colorama import init, Fore, Style
    init(autoreset=True)

C  = Fore.CYAN;  Y = Fore.YELLOW; G = Fore.GREEN
R  = Fore.RED;   W = Fore.WHITE;  D = Fore.WHITE + Style.DIM
M  = Fore.MAGENTA; B = Style.BRIGHT; RS = Style.RESET_ALL

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Version/17.0 Mobile/15E148 Safari/604.1",
]

def get_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,*/*;q=0.9",
        "Accept-Language": "es-AR,es;q=0.9,en-US;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

def get_api_headers():
    return {
        "User-Agent": USER_AGENTS[3],
        "Accept": "*/*",
        "Accept-Language": "es-AR,es;q=0.9",
        "X-IG-App-ID": "936619743392459",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.instagram.com/",
        "Origin": "https://www.instagram.com",
    }

# ══════════════════════════════════════════════════════════════════════════════
# BANNER
# ══════════════════════════════════════════════════════════════════════════════
def banner():
    os.system("cls" if os.name == "nt" else "clear")
    CYAN='\033[96m'; ORAN='\033[38;5;208m'; DIM='\033[2m\033[37m'
    BOLD='\033[1m';  YEL='\033[33m';        RST='\033[0m'
    logo = [
        "              ...::::...               ",
        "              ..:::+: ....             ",
        "        .:...:::::::.  ..:....... ..   ",
        "       :+  .:::::::    ::::::::::.     ",
        "      .+. .::::::::    +::::::::++::   ",
        "    . ::.:+:.          :::       ::+:  ",
        "   .: :::+.            +:+       .+++  ",
        "   .+ .+::             +:+.    .:+++.  ",
        "    +: :+.             ++++++++++++:   ",
        "     +:.:+             +++:......:+++: ",
        "   :. :++++.           +++         ++%:",
        "    ::  .::+++:::::    +++        .++%:",
        "     .:::....::++++   .+++:.....::+++: ",
        "   ... ..:+::+::+++:. ::++++++++++:.   ",
        "     :+:. :+.:+:.:++::......  ...      ",
        "       :+: :+..++...::::.......         ",
        "         .. :+:..:+:.........           ",
    ]
    print()
    for line in logo:
        mid = len(line) // 2
        print(f"       {CYAN}{BOLD}{line[:mid]}{ORAN}{line[mid:]}{RST}")
    print(f"                          {DIM}by: Fgunther{RST}")
    print()
    print(f"  {CYAN}{BOLD}Ciber{ORAN}brigada{RST} {CYAN}OSINT Suite{RST}  {DIM}─────────────────────{RST}")
    print(f"  {BOLD}╔══════════════════════════════════════════╗{RST}")
    print(f"  {BOLD}║  📸  CB-INSTAHUNTER  v2.0               ║{RST}")
    print(f"  {BOLD}║  Instagram OSINT — Datos en terminal    ║{RST}")
    print(f"  {BOLD}╚══════════════════════════════════════════╝{RST}")
    print(f"  {DIM}[ ciberbrigada.com ]  [ OSINT Suite ]{RST}")
    print(f"  {YEL}⚠  Solo para uso legal, ético y educativo  ⚠{RST}")
    print()

def sep(t=""):
    if t:
        pad = (56 - len(t)) // 2
        print(f"\n{C}{'─'*pad} {B}{t}{RS}{C} {'─'*pad}{RS}")
    else:
        print(f"{D}{'─'*60}{RS}")

def ok(m):    print(f"  {G}{B}[✓]{RS} {W}{m}{RS}")
def warn(m):  print(f"  {Y}[!]{RS} {Y}{m}{RS}")
def fail(m):  print(f"  {R}[✗]{RS} {D}{m}{RS}")
def info(m):  print(f"  {C}[i]{RS} {W}{m}{RS}")
def dato(k,v):print(f"  {C}  ▸ {D}{k}:{RS} {W}{B}{v}{RS}")

def fmt_num(n):
    try:
        n = int(n)
        if n >= 1_000_000: return f"{n/1_000_000:.1f}M"
        if n >= 1_000:     return f"{n/1_000:.1f}K"
        return str(n)
    except: return str(n)

def ts_to_date(ts):
    try: return datetime.datetime.fromtimestamp(int(ts)).strftime("%Y-%m-%d %H:%M")
    except: return "—"

# ══════════════════════════════════════════════════════════════════════════════
# EXTRACTOR — múltiples métodos
# ══════════════════════════════════════════════════════════════════════════════
def extraer_perfil(username):
    data = {}

    # Método 1: API ?__a=1 con sesión
    try:
        s = requests.Session()
        s.get("https://www.instagram.com/", headers=get_headers(), timeout=10)
        time.sleep(random.uniform(0.8, 1.5))
        r = s.get(
            f"https://www.instagram.com/{username}/?__a=1&__d=dis",
            headers=get_api_headers(), timeout=12
        )
        if r.status_code == 200:
            d = r.json()
            user = (d.get("graphql", {}).get("user") or
                    d.get("data", {}).get("user") or
                    d.get("user", {}))
            if user and user.get("username"):
                data["source"]       = "API Instagram"
                data["id"]           = user.get("id", "—")
                data["username"]     = user.get("username", "—")
                data["full_name"]    = user.get("full_name", "—")
                data["biography"]    = user.get("biography", "—")
                data["followers"]    = user.get("edge_followed_by", {}).get("count", 0)
                data["following"]    = user.get("edge_follow", {}).get("count", 0)
                data["posts"]        = user.get("edge_owner_to_timeline_media", {}).get("count", 0)
                data["is_private"]   = user.get("is_private", False)
                data["is_verified"]  = user.get("is_verified", False)
                data["is_business"]  = user.get("is_business_account", False)
                data["business_cat"] = user.get("business_category_name", "")
                data["external_url"] = user.get("external_url", "")
                data["profile_pic"]  = user.get("profile_pic_url_hd") or user.get("profile_pic_url", "")
                data["highlights"]   = user.get("highlight_reel_count", 0)
                data["igtv"]         = user.get("edge_felix_video_timeline", {}).get("count", 0)

                # Posts recientes
                edges = user.get("edge_owner_to_timeline_media", {}).get("edges", [])
                if edges:
                    data["recent_posts"] = []
                    for e in edges[:9]:
                        node = e.get("node", {})
                        caption_edges = node.get("edge_media_to_caption", {}).get("edges", [])
                        caption_text  = caption_edges[0].get("node", {}).get("text", "") if caption_edges else ""
                        data["recent_posts"].append({
                            "shortcode": node.get("shortcode", ""),
                            "likes":     node.get("edge_liked_by", {}).get("count", 0),
                            "comments":  node.get("edge_media_to_comment", {}).get("count", 0),
                            "timestamp": node.get("taken_at_timestamp", 0),
                            "type":      node.get("__typename", "GraphImage"),
                            "caption":   caption_text[:120],
                            "hashtags":  re.findall(r'#(\w+)', caption_text),
                            "location":  node.get("location", {}).get("name", "") if node.get("location") else "",
                        })
                return data
    except Exception:
        pass

    # Método 2: Scraping HTML + Regex
    try:
        s2 = requests.Session()
        r2 = s2.get(f"https://www.instagram.com/{username}/", headers=get_headers(), timeout=12)
        if r2.status_code == 404:
            return {"error": "Usuario no encontrado"}
        if r2.status_code == 429:
            return {"error": "Rate limit de Instagram — esperá unos minutos"}
        if r2.status_code == 200:
            html = r2.text
            extractors = {
                "followers":    r'"edge_followed_by":\{"count":(\d+)\}',
                "following":    r'"edge_follow":\{"count":(\d+)\}',
                "posts":        r'"edge_owner_to_timeline_media":\{"count":(\d+)\}',
                "full_name":    r'"full_name":"([^"]+)"',
                "biography":    r'"biography":"([^"]*)"',
                "is_private":   r'"is_private":(true|false)',
                "is_verified":  r'"is_verified":(true|false)',
                "is_business":  r'"is_business_account":(true|false)',
                "id":           r'"id":"(\d+)"',
                "external_url": r'"external_url":"([^"]*)"',
                "profile_pic":  r'"profile_pic_url_hd":"([^"]+)"',
                "business_cat": r'"business_category_name":"([^"]*)"',
                "highlights":   r'"highlight_reel_count":(\d+)',
                "igtv":         r'"edge_felix_video_timeline":\{"count":(\d+)\}',
            }
            found = {}
            for key, pattern in extractors.items():
                m = re.search(pattern, html)
                if m:
                    val = m.group(1)
                    if val in ("true", "false"): found[key] = val == "true"
                    elif val.isdigit():          found[key] = int(val)
                    else:
                        try:    found[key] = val.encode().decode('unicode_escape')
                        except: found[key] = val

            if found.get("followers") is not None or found.get("full_name"):
                data["source"]   = "HTML Scraping"
                data["username"] = username
                data.update(found)
                return data
    except Exception:
        pass

    return {"error": "No se pudieron obtener datos. Puede ser cuenta privada o bloqueo temporal."}

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 1 — PERFIL COMPLETO
# ══════════════════════════════════════════════════════════════════════════════
def modulo_perfil(username, data):
    sep("PERFIL DE INSTAGRAM")
    if data.get("error"):
        fail(data["error"]); return

    ok(f"Datos obtenidos — Método: {data.get('source','—')}")
    print()

    dato("Username",      f"@{data.get('username','—')}")
    dato("Nombre",        data.get("full_name", "—"))
    dato("ID de usuario", str(data.get("id", "—")))

    # Estado
    privado    = data.get("is_private", False)
    verificado = data.get("is_verified", False)
    negocio    = data.get("is_business", False)

    estado = []
    if verificado: estado.append(f"{G}✓ VERIFICADO{RS}")
    if privado:    estado.append(f"{Y}🔒 PRIVADO{RS}")
    else:          estado.append(f"{G}🌐 PÚBLICO{RS}")
    if negocio:    estado.append(f"{C}💼 BUSINESS{RS}")
    print(f"  {C}  ▸ {D}Estado:{RS}        {'  '.join(estado)}")

    cat = data.get("business_cat", "")
    if cat and cat != "—": dato("Categoría",   cat)

    bio = data.get("biography", "")
    if bio and bio != "—": dato("Biografía",   bio[:160] + ("..." if len(bio) > 160 else ""))

    ext = data.get("external_url", "")
    if ext and ext != "—": dato("Link externo", ext)

    print()
    sep_line = f"  {C}{B}── ESTADÍSTICAS ─────────────────────────{RS}"
    print(sep_line)

    followers = int(data.get("followers", 0) or 0)
    following = int(data.get("following", 0) or 0)
    posts     = int(data.get("posts", 0) or 0)

    dato("Seguidores",     f"{fmt_num(followers)}  ({followers:,})")
    dato("Seguidos",       f"{fmt_num(following)}  ({following:,})")
    dato("Publicaciones",  str(posts))

    if followers and following and following > 0:
        ratio = followers / following
        dato("Ratio seg/seg",  f"{ratio:.2f}x")

    highlights = data.get("highlights", 0)
    igtv       = data.get("igtv", 0)
    if highlights: dato("Historias dest.", str(highlights))
    if igtv:       dato("Videos IGTV",    str(igtv))

    print()
    # Nivel de influencer
    if followers:
        if followers >= 1_000_000:  nivel = f"{Y}{B}⭐ MEGA INFLUENCER  (+1M){RS}"
        elif followers >= 100_000:  nivel = f"{G}{B}⭐ MACRO INFLUENCER (+100K){RS}"
        elif followers >= 10_000:   nivel = f"{C}{B}⭐ MICRO INFLUENCER (+10K){RS}"
        elif followers >= 1_000:    nivel = f"{W}⭐ NANO INFLUENCER  (+1K){RS}"
        else:                       nivel = f"{D}Usuario regular{RS}"
        print(f"  {C}  ▸ {D}Clasificación:{RS}  {nivel}")

    # Foto de perfil (URL directa para descarga)
    pic = data.get("profile_pic", "")
    if pic and pic != "—":
        print()
        dato("Foto de perfil (HD)", pic)

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 2 — POSTS Y ENGAGEMENT
# ══════════════════════════════════════════════════════════════════════════════
def modulo_posts(username, data):
    sep("PUBLICACIONES Y ENGAGEMENT")

    if data.get("is_private"):
        warn("Cuenta privada — posts no visibles"); return

    posts = data.get("recent_posts", [])
    if not posts:
        warn("No se pudieron extraer posts (posible rate limit o cuenta privada)")
        return

    ok(f"Últimos {len(posts)} posts analizados")
    print()

    total_likes    = 0
    total_comments = 0
    all_hashtags   = []
    all_locations  = []

    tipo_icons = {"GraphImage": "📷 Foto", "GraphVideo": "🎥 Video", "GraphSidecar": "📎 Carrusel"}

    for i, post in enumerate(posts, 1):
        likes    = int(post.get("likes", 0))
        comments = int(post.get("comments", 0))
        ts       = post.get("timestamp", 0)
        tipo     = post.get("type", "GraphImage")
        caption  = post.get("caption", "")
        hashtags = post.get("hashtags", [])
        location = post.get("location", "")
        shortcode= post.get("shortcode", "")

        total_likes    += likes
        total_comments += comments
        all_hashtags   += hashtags
        if location: all_locations.append(location)

        tipo_str = tipo_icons.get(tipo, "📷 Foto")
        print(f"  {C}{B}── Post #{i}  {tipo_str}{RS}")
        dato("  Fecha",        ts_to_date(ts))
        dato("  Shortcode",    shortcode)
        dato("  Likes",        f"{fmt_num(likes)} ({likes:,})")
        dato("  Comentarios",  f"{fmt_num(comments)} ({comments:,})")
        if caption:
            dato("  Caption",  caption[:100] + ("..." if len(caption) > 100 else ""))
        if hashtags:
            dato("  Hashtags", "  ".join([f"#{h}" for h in hashtags[:10]]))
        if location:
            dato("  Ubicación", location)
        print()

    # Resumen de engagement
    if posts:
        sep("RESUMEN DE ENGAGEMENT")
        n         = len(posts)
        avg_likes = total_likes // n
        avg_com   = total_comments // n
        followers = int(data.get("followers", 0) or 0)

        dato("Total likes analizados",       f"{total_likes:,}")
        dato("Total comentarios analizados", f"{total_comments:,}")
        dato("Promedio likes/post",          fmt_num(avg_likes))
        dato("Promedio comentarios/post",    fmt_num(avg_com))

        if followers:
            eng = ((avg_likes + avg_com) / followers) * 100
            dato("Tasa de engagement",       f"{eng:.2f}%")
            if eng > 6:   nivel = f"{G}🔥 EXCELENTE (>6%){RS}"
            elif eng > 3: nivel = f"{C}✓ BUENO (3-6%){RS}"
            elif eng > 1: nivel = f"{Y}~ PROMEDIO (1-3%){RS}"
            else:         nivel = f"{D}▼ BAJO (<1%){RS}"
            print(f"  {C}  ▸ {D}Nivel:{RS}  {nivel}")

        # Post más popular
        mejor = max(posts, key=lambda x: int(x.get("likes", 0)))
        print()
        dato("Post más popular", f"{fmt_num(mejor.get('likes',0))} likes — {ts_to_date(mejor.get('timestamp',0))}")

        # Horario de mayor actividad
        horas = [datetime.datetime.fromtimestamp(int(p["timestamp"])).hour
                 for p in posts if p.get("timestamp")]
        if horas:
            hora_comun = Counter(horas).most_common(1)[0][0]
            dato("Hora más frecuente de publicación", f"{hora_comun:02d}:00 hs")

    # Top hashtags
    if all_hashtags:
        print()
        sep("HASHTAGS MÁS USADOS")
        top = Counter(all_hashtags).most_common(12)
        for tag, count in top:
            bar = "█" * min(count * 4, 24)
            print(f"  {C}  #{tag:<22}{RS}{G}{bar}{RS} {W}{count}x{RS}")

    # Ubicaciones
    if all_locations:
        print()
        sep("UBICACIONES DETECTADAS")
        for loc in list(set(all_locations)):
            dato("Lugar", loc)

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 3 — ANÁLISIS DE INTELIGENCIA
# ══════════════════════════════════════════════════════════════════════════════
def modulo_inteligencia(username, data):
    sep("ANÁLISIS DE INTELIGENCIA")
    if data.get("error"):
        warn("Sin datos suficientes"); return

    bio       = data.get("biography", "")
    followers = int(data.get("followers", 0) or 0)
    following = int(data.get("following", 0) or 0)
    posts     = int(data.get("posts", 0) or 0)
    privado   = data.get("is_private", False)

    # ── Análisis de biografía ──────────────────────────────────────────────
    if bio and bio != "—":
        print(f"  {C}{B}── DATOS ENCONTRADOS EN BIOGRAFÍA ────────{RS}\n")

        emails = re.findall(r'[\w.+-]+@[\w-]+\.[a-z]{2,}', bio)
        for e in emails: ok(f"Email: {G}{e}{RS}")

        phones = re.findall(r'(?:\+?\d[\d\s\-\(\)]{7,}\d)', bio)
        for p in phones: ok(f"Teléfono: {G}{p.strip()}{RS}")

        urls = re.findall(r'https?://\S+|www\.\S+', bio)
        for u in urls: ok(f"URL: {G}{u}{RS}")

        redes = {
            "Twitter/X":  r'twitter\.com/|x\.com/|(?<!\w)@\w+',
            "TikTok":     r'tiktok\.com/',
            "YouTube":    r'youtube\.com/|youtu\.be/',
            "LinkedIn":   r'linkedin\.com/',
            "Telegram":   r't\.me/|telegram',
            "WhatsApp":   r'wa\.me/|whatsapp',
            "Facebook":   r'facebook\.com/|fb\.com/',
            "Twitch":     r'twitch\.tv/',
            "Spotify":    r'open\.spotify\.com/',
        }
        for red, pat in redes.items():
            if re.search(pat, bio, re.IGNORECASE):
                info(f"Referencia a {red} detectada en biografía")

        if not emails and not phones and not urls:
            info("No se encontraron datos de contacto en la biografía")

    # ── Análisis de comportamiento ─────────────────────────────────────────
    print(f"\n  {C}{B}── ANÁLISIS DE COMPORTAMIENTO ────────────{RS}\n")

    if privado:
        warn("Cuenta PRIVADA — contenido restringido")
    else:
        ok("Cuenta PÚBLICA — contenido accesible")

    if followers and following:
        ratio = followers / following if following > 0 else followers
        if ratio > 10:
            ok(f"Ratio {ratio:.1f}x — Gran alcance orgánico")
        elif ratio > 1:
            info(f"Ratio {ratio:.1f}x — Perfil equilibrado")
        else:
            warn(f"Ratio {ratio:.2f}x — Sigue a más de los que le siguen")

    # Detección de anomalías
    if followers > 50000 and posts < 20:
        warn("Muchos seguidores con muy pocos posts — posible compra de seguidores")
    if following > 7500:
        warn("Sigue a más de 7500 cuentas — posible estrategia follow/unfollow")
    if followers < 50 and following > 500:
        warn("Perfil nuevo o posible bot/spam")
    if posts > 500 and followers < 500:
        warn("Muchos posts y pocos seguidores — baja visibilidad")

    if followers > 10000 and posts > 50:
        posts_per_1k = posts / (followers / 1000)
        dato("Posts por cada 1K seguidores", f"{posts_per_1k:.1f}")

    # Idioma de la bio
    if bio:
        if re.search(r'\b(the|and|is|in|of|you|for)\b', bio, re.IGNORECASE):
            info("Idioma detectado en bio: Inglés")
        elif re.search(r'\b(de|la|el|en|es|un|una|por|con)\b', bio, re.IGNORECASE):
            info("Idioma detectado en bio: Español")
        elif re.search(r'\b(de|la|le|les|du|des|et|en)\b', bio, re.IGNORECASE):
            info("Idioma detectado en bio: Francés/Portugués")

# ══════════════════════════════════════════════════════════════════════════════
# RESUMEN FINAL
# ══════════════════════════════════════════════════════════════════════════════
def modulo_resumen(username, data):
    sep("RESUMEN FINAL")
    print(f"\n  {C}{B}Target:{RS}        {W}{B}@{username}{RS}")
    if not data.get("error"):
        print(f"  {C}{B}Nombre:{RS}        {W}{data.get('full_name','—')}{RS}")
        print(f"  {C}{B}ID:{RS}            {W}{data.get('id','—')}{RS}")
        print(f"  {C}{B}Seguidores:{RS}    {W}{fmt_num(data.get('followers',0))}{RS}")
        print(f"  {C}{B}Seguidos:{RS}      {W}{fmt_num(data.get('following',0))}{RS}")
        print(f"  {C}{B}Posts:{RS}         {W}{data.get('posts',0)}{RS}")
        print(f"  {C}{B}Privado:{RS}       {W}{'SÍ 🔒' if data.get('is_private') else 'NO 🌐'}{RS}")
        print(f"  {C}{B}Verificado:{RS}    {W}{'SÍ ✓' if data.get('is_verified') else 'NO'}{RS}")
        print(f"  {C}{B}Business:{RS}      {W}{'SÍ 💼' if data.get('is_business') else 'NO'}{RS}")
        posts_data = data.get("recent_posts", [])
        if posts_data:
            total_likes = sum(int(p.get("likes",0)) for p in posts_data)
            print(f"  {C}{B}Total likes:{RS}   {W}{fmt_num(total_likes)}{RS}")
    print(f"\n  {D}Análisis completado — Ciberbrigada OSINT Suite v2.0{RS}\n")

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    banner()
    print(f"  {W}Ingresá el username de Instagram (sin @):{RS}\n")

    while True:
        try:
            username = input(f"  {C}▸ Username:{RS} ").strip().lstrip("@")
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n  {Y}Saliendo... Hasta pronto.{RS}\n"); sys.exit(0)

        if username.lower() in ("salir","exit","quit","q"):
            print(f"\n  {Y}Saliendo... Hasta pronto.{RS}\n"); sys.exit(0)

        if not username or not re.match(r'^[a-zA-Z0-9._]+$', username):
            warn("Username inválido"); continue

        print(f"\n  {C}Extrayendo datos de @{username}...{RS}")
        print(f"  {D}Conectando con Instagram, aguardá...{RS}\n")

        data = extraer_perfil(username)

        sep("SELECCIONÁ LOS MÓDULOS")
        modulos = [
            ("1", "Perfil       — Nombre, bio, seguidores, estado, foto"),
            ("2", "Posts        — Publicaciones, likes, hashtags, engagement"),
            ("3", "Inteligencia — Bio, comportamiento, anomalías"),
            ("0", "TODOS LOS MÓDULOS"),
        ]
        for num, desc in modulos:
            color = C if num != "0" else Y
            print(f"  {color}[{num}]{RS} {W}{desc}{RS}")

        print()
        try:
            sel = input(f"  {C}▸ Opción:{RS} ").strip()
        except (KeyboardInterrupt, EOFError):
            sys.exit(0)

        selected = ["1","2","3"] if sel == "0" else [s.strip() for s in sel.split(",")]
        print()

        if "1" in selected: modulo_perfil(username, data)
        if "2" in selected: modulo_posts(username, data)
        if "3" in selected: modulo_inteligencia(username, data)

        modulo_resumen(username, data)

        sep()
        print(f"\n  {D}¿Analizar otro usuario? (Enter / 'salir'){RS}")
        try:
            again = input(f"  {C}▸{RS} ").strip().lower()
            if again in ("salir","exit","quit","q"):
                print(f"\n  {Y}Saliendo... Hasta pronto.{RS}\n"); sys.exit(0)
        except (KeyboardInterrupt, EOFError):
            sys.exit(0)

        banner()

if __name__ == "__main__":
    main()
