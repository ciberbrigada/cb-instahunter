#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
#   CB-INSTAHUNTER v1.0 — Ciberbrigada OSINT Suite
#   Instagram OSINT — Perfil público sin login
#   Uso exclusivo para fines legales y educativos
# ═══════════════════════════════════════════════════════════════════════════════

import sys
import os
import re
import json
import time
import urllib.parse
import hashlib
import random

try:
    import requests
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    os.system("pip install requests colorama --break-system-packages -q")
    import requests
    from colorama import init, Fore, Style
    init(autoreset=True)

# ── Colores ───────────────────────────────────────────────────────────────────
C  = Fore.CYAN
Y  = Fore.YELLOW
G  = Fore.GREEN
R  = Fore.RED
W  = Fore.WHITE
D  = Fore.WHITE + Style.DIM
M  = Fore.MAGENTA
B  = Style.BRIGHT
RS = Style.RESET_ALL

# ── Headers rotativos para evitar bloqueos ────────────────────────────────────
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
]

def get_headers(mobile=False):
    ua = USER_AGENTS[3] if mobile else random.choice(USER_AGENTS[:3])
    return {
        "User-Agent": ua,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "es-AR,es;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Cache-Control": "max-age=0",
    }

def get_api_headers():
    return {
        "User-Agent": USER_AGENTS[3],
        "Accept": "*/*",
        "Accept-Language": "es-AR,es;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "X-IG-App-ID": "936619743392459",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.instagram.com/",
        "Origin": "https://www.instagram.com",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
    }

# ══════════════════════════════════════════════════════════════════════════════
# BANNER
# ══════════════════════════════════════════════════════════════════════════════
def banner():
    os.system("cls" if os.name == "nt" else "clear")
    CYAN = '\033[96m'; ORAN = '\033[38;5;208m'
    DIM  = '\033[2m\033[37m'; BOLD = '\033[1m'
    YEL  = '\033[33m'; RST  = '\033[0m'
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
    print(f"  {BOLD}║  📸  CB-INSTAHUNTER  v1.0               ║{RST}")
    print(f"  {BOLD}║  Instagram OSINT — Perfil público       ║{RST}")
    print(f"  {BOLD}╚══════════════════════════════════════════╝{RST}")
    print(f"  {DIM}[ ciberbrigada.com ]  [ OSINT Suite ]{RST}")
    print(f"  {YEL}⚠  Solo para uso legal, ético y educativo  ⚠{RST}")
    print()

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def sep(titulo=""):
    if titulo:
        pad = (56 - len(titulo)) // 2
        print(f"\n{C}{'─'*pad} {B}{titulo}{RS}{C} {'─'*pad}{RS}")
    else:
        print(f"{D}{'─'*60}{RS}")

def ok(msg):    print(f"  {G}{B}[✓]{RS} {W}{msg}{RS}")
def warn(msg):  print(f"  {Y}[!]{RS} {Y}{msg}{RS}")
def fail(msg):  print(f"  {R}[✗]{RS} {D}{msg}{RS}")
def info(msg):  print(f"  {C}[i]{RS} {W}{msg}{RS}")
def dato(k, v): print(f"  {C}  ▸ {D}{k}:{RS} {W}{B}{v}{RS}")

def fmt_number(n):
    try:
        n = int(n)
        if n >= 1_000_000: return f"{n/1_000_000:.1f}M"
        if n >= 1_000:     return f"{n/1_000:.1f}K"
        return str(n)
    except:
        return str(n)

# ══════════════════════════════════════════════════════════════════════════════
# EXTRACTOR PRINCIPAL — múltiples métodos
# ══════════════════════════════════════════════════════════════════════════════
def extraer_perfil(username):
    data = {}

    # Método 1: API privada de Instagram (?__a=1)
    try:
        session = requests.Session()
        # Primero visitar la página principal para obtener cookies
        session.get("https://www.instagram.com/", headers=get_headers(), timeout=10)
        time.sleep(1)

        r = session.get(
            f"https://www.instagram.com/{username}/?__a=1&__d=dis",
            headers=get_api_headers(),
            timeout=12
        )
        if r.status_code == 200:
            try:
                d = r.json()
                user = d.get("graphql", {}).get("user") or d.get("data", {}).get("user") or d.get("user", {})
                if user and user.get("username"):
                    data["source"] = "API Instagram (?__a=1)"
                    data["id"]              = user.get("id", "—")
                    data["username"]        = user.get("username", "—")
                    data["full_name"]       = user.get("full_name", "—")
                    data["biography"]       = user.get("biography", "—")
                    data["followers"]       = user.get("edge_followed_by", {}).get("count", 0)
                    data["following"]       = user.get("edge_follow", {}).get("count", 0)
                    data["posts"]           = user.get("edge_owner_to_timeline_media", {}).get("count", 0)
                    data["is_private"]      = user.get("is_private", False)
                    data["is_verified"]     = user.get("is_verified", False)
                    data["is_business"]     = user.get("is_business_account", False)
                    data["business_cat"]    = user.get("business_category_name", "—")
                    data["external_url"]    = user.get("external_url", "—")
                    data["profile_pic"]     = user.get("profile_pic_url_hd") or user.get("profile_pic_url", "—")
                    data["highlight_count"] = user.get("highlight_reel_count", 0)
                    data["igtv_count"]      = user.get("edge_felix_video_timeline", {}).get("count", 0)

                    # Posts recientes
                    posts_edges = user.get("edge_owner_to_timeline_media", {}).get("edges", [])
                    if posts_edges:
                        data["recent_posts"] = []
                        for edge in posts_edges[:6]:
                            node = edge.get("node", {})
                            data["recent_posts"].append({
                                "shortcode":  node.get("shortcode", ""),
                                "likes":      node.get("edge_liked_by", {}).get("count", 0),
                                "comments":   node.get("edge_media_to_comment", {}).get("count", 0),
                                "timestamp":  node.get("taken_at_timestamp", 0),
                                "type":       node.get("__typename", "—"),
                                "caption":    (node.get("edge_media_to_caption", {}).get("edges", [{}])[0]
                                               .get("node", {}).get("text", "")[:100] if
                                               node.get("edge_media_to_caption", {}).get("edges") else ""),
                                "hashtags":   re.findall(r'#(\w+)', node.get("edge_media_to_caption", {})
                                                        .get("edges", [{}])[0].get("node", {}).get("text", ""))
                                              if node.get("edge_media_to_caption", {}).get("edges") else [],
                            })
                    return data
            except (json.JSONDecodeError, KeyError):
                pass
    except Exception:
        pass

    # Método 2: Scraping del HTML de la página
    try:
        session2 = requests.Session()
        r2 = session2.get(
            f"https://www.instagram.com/{username}/",
            headers=get_headers(),
            timeout=12
        )
        if r2.status_code == 200:
            html = r2.text

            # Extraer JSON embebido en el HTML
            patterns = [
                r'window\._sharedData\s*=\s*({.+?});</script>',
                r'"user":\s*({[^{}]+(?:{[^{}]*}[^{}]*)*})',
                r'<script type="application/ld\+json">(.*?)</script>',
            ]

            for pattern in patterns:
                match = re.search(pattern, html, re.DOTALL)
                if match:
                    try:
                        raw = match.group(1)
                        d = json.loads(raw)

                        # Intentar extraer de _sharedData
                        user = (d.get("entry_data", {})
                                 .get("ProfilePage", [{}])[0]
                                 .get("graphql", {})
                                 .get("user", {}))

                        if not user and d.get("@type") == "Person":
                            # Schema.org JSON-LD
                            data["source"]    = "HTML Schema.org"
                            data["username"]  = username
                            data["full_name"] = d.get("name", "—")
                            data["biography"] = d.get("description", "—")
                            data["external_url"] = d.get("url", "—")
                            return data

                        if user and user.get("username"):
                            data["source"]       = "HTML _sharedData"
                            data["id"]           = user.get("id", "—")
                            data["username"]     = user.get("username", "—")
                            data["full_name"]    = user.get("full_name", "—")
                            data["biography"]    = user.get("biography", "—")
                            data["followers"]    = user.get("edge_followed_by", {}).get("count", 0)
                            data["following"]    = user.get("edge_follow", {}).get("count", 0)
                            data["posts"]        = user.get("edge_owner_to_timeline_media", {}).get("count", 0)
                            data["is_private"]   = user.get("is_private", False)
                            data["is_verified"]  = user.get("is_verified", False)
                            data["profile_pic"]  = user.get("profile_pic_url_hd", "—")
                            data["external_url"] = user.get("external_url", "—")
                            return data
                    except Exception:
                        continue

            # Método 3: Regex directo sobre el HTML
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
            }

            found = {}
            for key, pattern in extractors.items():
                m = re.search(pattern, html)
                if m:
                    val = m.group(1)
                    if val in ("true", "false"):
                        found[key] = val == "true"
                    elif val.isdigit():
                        found[key] = int(val)
                    else:
                        found[key] = val.encode().decode('unicode_escape')

            if found.get("followers") or found.get("full_name"):
                data["source"]   = "HTML Regex"
                data["username"] = username
                data.update(found)

                # Extraer hashtags del HTML
                hashtags = list(set(re.findall(r'#(\w+)', html)))[:20]
                if hashtags:
                    data["hashtags_encontrados"] = hashtags

                return data

        elif r2.status_code == 404:
            return {"error": "Usuario no encontrado (404)"}
        elif r2.status_code == 429:
            return {"error": "Rate limit de Instagram — esperá unos minutos"}

    except Exception as e:
        return {"error": str(e)}

    # Método 4: Picuki (mirror público de Instagram)
    try:
        r3 = requests.get(
            f"https://www.picuki.com/profile/{username}",
            headers=get_headers(),
            timeout=12
        )
        if r3.status_code == 200:
            html3 = r3.text
            found3 = {}

            patterns3 = {
                "full_name":  r'<div class="profile-name-top">\s*<h1>([^<]+)</h1>',
                "biography":  r'<div class="profile-description">\s*<p>([^<]+)</p>',
                "followers":  r'Seguidores[^>]*>\s*<span[^>]*>([\d,\.KM]+)<',
                "following":  r'Seguidos[^>]*>\s*<span[^>]*>([\d,\.KM]+)<',
                "posts":      r'Publicaciones[^>]*>\s*<span[^>]*>([\d,\.KM]+)<',
            }

            for key, pat in patterns3.items():
                m = re.search(pat, html3, re.IGNORECASE)
                if m:
                    found3[key] = m.group(1).strip()

            if found3:
                data["source"]   = "Picuki (mirror)"
                data["username"] = username
                data.update(found3)
                return data
    except Exception:
        pass

    return {"error": "No se pudieron obtener datos. El perfil puede ser privado o estar bloqueado."}

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 1 — PERFIL
# ══════════════════════════════════════════════════════════════════════════════
def modulo_perfil(username, data):
    sep("PERFIL DE INSTAGRAM")

    if data.get("error"):
        fail(data["error"])
        return

    ok(f"Perfil encontrado — Fuente: {D}{data.get('source','—')}{RS}")
    print()

    dato("Username",       f"@{data.get('username','—')}")
    dato("Nombre",         data.get("full_name", "—"))
    dato("ID de usuario",  str(data.get("id", "—")))

    # Estado de cuenta
    privado   = data.get("is_private", False)
    verificado= data.get("is_verified", False)
    negocio   = data.get("is_business", False)

    estado = []
    if verificado: estado.append(f"{G}✓ VERIFICADO{RS}")
    if privado:    estado.append(f"{Y}🔒 PRIVADO{RS}")
    else:          estado.append(f"{G}🌐 PÚBLICO{RS}")
    if negocio:    estado.append(f"{C}💼 CUENTA BUSINESS{RS}")

    print(f"  {C}  ▸ {D}Estado:{RS}         {'  '.join(estado)}")

    cat = data.get("business_cat", "")
    if cat and cat != "—": dato("Categoría business", cat)

    bio = data.get("biography", "")
    if bio and bio != "—":
        dato("Biografía",      bio[:150] + ("..." if len(bio) > 150 else ""))

    ext = data.get("external_url", "")
    if ext and ext != "—": dato("Link externo",    ext)

    print()

    # Estadísticas
    followers = data.get("followers", 0)
    following = data.get("following", 0)
    posts     = data.get("posts", 0)

    if followers or following or posts:
        print(f"  {C}{B}── ESTADÍSTICAS ──────────────────────────{RS}")
        dato("Seguidores",    f"{fmt_number(followers)} ({followers:,})")
        dato("Seguidos",      f"{fmt_number(following)} ({following:,})")
        dato("Publicaciones", str(posts))

        if followers and following:
            ratio = followers / following if following > 0 else followers
            dato("Ratio follow",  f"{ratio:.2f}x")

        # Clasificación de influencer
        if followers:
            f = int(followers)
            if f >= 1_000_000:   nivel = f"{Y}⭐ MEGA INFLUENCER (1M+){RS}"
            elif f >= 100_000:   nivel = f"{G}⭐ MACRO INFLUENCER (100K+){RS}"
            elif f >= 10_000:    nivel = f"{C}⭐ MICRO INFLUENCER (10K+){RS}"
            elif f >= 1_000:     nivel = f"{W}⭐ NANO INFLUENCER (1K+){RS}"
            else:                nivel = f"{D}Usuario regular{RS}"
            print(f"  {C}  ▸ {D}Nivel:{RS}          {nivel}")

    highlights = data.get("highlight_count", 0)
    if highlights: dato("Destacados",    str(highlights))

    igtv = data.get("igtv_count", 0)
    if igtv: dato("Videos IGTV",    str(igtv))

    # Links del perfil
    print()
    print(f"  {C}{B}── LINKS ─────────────────────────────────{RS}")
    dato("Perfil web",     f"https://www.instagram.com/{username}/")
    dato("Foto perfil",    data.get("profile_pic", "—"))

    pic_url = data.get("profile_pic", "")
    if pic_url and pic_url != "—":
        # Hash MD5 de la URL para referencia
        dato("Hash foto",  hashlib.md5(pic_url.encode()).hexdigest()[:16] + "...")

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 2 — POSTS RECIENTES
# ══════════════════════════════════════════════════════════════════════════════
def modulo_posts(username, data):
    sep("POSTS RECIENTES")

    posts = data.get("recent_posts", [])
    if not posts:
        if data.get("is_private"):
            warn("Cuenta privada — no se pueden ver los posts")
        else:
            warn("No se pudieron extraer posts (posible rate limit)")
        return

    ok(f"Últimos {len(posts)} posts analizados:")
    print()

    total_likes    = 0
    total_comments = 0
    all_hashtags   = []

    for i, post in enumerate(posts, 1):
        shortcode = post.get("shortcode", "")
        likes     = post.get("likes", 0)
        comments  = post.get("comments", 0)
        ts        = post.get("timestamp", 0)
        tipo      = post.get("type", "—")
        caption   = post.get("caption", "")
        hashtags  = post.get("hashtags", [])

        total_likes    += likes
        total_comments += comments
        all_hashtags   += hashtags

        # Fecha
        fecha = "—"
        if ts:
            import datetime
            fecha = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")

        tipo_icon = {"GraphImage": "📷", "GraphVideo": "🎥", "GraphSidecar": "📎"}.get(tipo, "📷")

        print(f"  {C}{B}[Post #{i}]{RS} {tipo_icon} {D}{shortcode}{RS}")
        dato("  URL",       f"https://www.instagram.com/p/{shortcode}/")
        dato("  Fecha",     fecha)
        dato("  Likes",     fmt_number(likes))
        dato("  Comentarios", fmt_number(comments))
        if caption:
            dato("  Caption",  caption[:80] + ("..." if len(caption) > 80 else ""))
        if hashtags:
            dato("  Hashtags", " ".join([f"#{h}" for h in hashtags[:8]]))
        print()

    # Resumen de engagement
    if total_likes or total_comments:
        followers = data.get("followers", 0)
        sep("ENGAGEMENT")
        dato("Total likes",     fmt_number(total_likes))
        dato("Total comentarios", fmt_number(total_comments))
        avg_likes = total_likes // len(posts) if posts else 0
        avg_com   = total_comments // len(posts) if posts else 0
        dato("Promedio likes/post",    fmt_number(avg_likes))
        dato("Promedio comentarios",   fmt_number(avg_com))

        if followers:
            eng_rate = ((avg_likes + avg_com) / followers) * 100
            dato("Tasa de engagement",  f"{eng_rate:.2f}%")
            if eng_rate > 6:    nivel = f"{G}🔥 EXCELENTE (>6%){RS}"
            elif eng_rate > 3:  nivel = f"{C}✓ BUENO (3-6%){RS}"
            elif eng_rate > 1:  nivel = f"{Y}~ PROMEDIO (1-3%){RS}"
            else:               nivel = f"{D}▼ BAJO (<1%){RS}"
            print(f"  {C}  ▸ {D}Nivel engagement:{RS} {nivel}")

    # Top hashtags
    if all_hashtags:
        sep("HASHTAGS MÁS USADOS")
        from collections import Counter
        top_tags = Counter(all_hashtags).most_common(15)
        for tag, count in top_tags:
            bar = "█" * min(count * 3, 20)
            print(f"  {C}#{tag:<20}{RS} {G}{bar}{RS} {W}{count}{RS}")

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 3 — ANÁLISIS AVANZADO
# ══════════════════════════════════════════════════════════════════════════════
def modulo_analisis(username, data):
    sep("ANÁLISIS AVANZADO")

    if data.get("error"):
        warn("Sin datos suficientes para análisis")
        return

    # Análisis de la biografía
    bio = data.get("biography", "")
    if bio and bio != "—":
        print(f"  {C}{B}── ANÁLISIS DE BIOGRAFÍA ─────────────────{RS}")

        # Emails en bio
        emails = re.findall(r'[\w.+-]+@[\w-]+\.[a-z]{2,}', bio)
        if emails:
            ok(f"Email encontrado en bio: {', '.join(emails)}")

        # Teléfonos en bio
        phones = re.findall(r'[\+\d][\d\s\-\(\)]{7,}', bio)
        if phones:
            ok(f"Teléfono encontrado en bio: {', '.join(phones)}")

        # URLs en bio
        urls = re.findall(r'https?://\S+|www\.\S+', bio)
        if urls:
            ok(f"URLs en bio: {', '.join(urls)}")

        # Links de otras redes en bio
        redes = {
            "Twitter/X":  r'twitter\.com/|x\.com/|@\w+',
            "TikTok":     r'tiktok\.com/|tt\.me/',
            "YouTube":    r'youtube\.com/|youtu\.be/',
            "LinkedIn":   r'linkedin\.com/',
            "Telegram":   r't\.me/|telegram',
            "WhatsApp":   r'wa\.me/|whatsapp',
            "Facebook":   r'facebook\.com/|fb\.com/',
        }
        for red, pat in redes.items():
            if re.search(pat, bio, re.IGNORECASE):
                info(f"Referencia a {red} en la bio")

        # Idioma aproximado
        if re.search(r'\b(the|and|is|in|of)\b', bio, re.IGNORECASE):
            info("Idioma detectado: Inglés")
        elif re.search(r'\b(de|la|el|en|es|un|una)\b', bio, re.IGNORECASE):
            info("Idioma detectado: Español")

    # Análisis de seguidores
    followers = int(data.get("followers", 0))
    following = int(data.get("following", 0))
    posts     = int(data.get("posts", 0))

    if followers and following:
        print(f"\n  {C}{B}── ANÁLISIS DE COMPORTAMIENTO ────────────{RS}")

        # Ratio seguidor/seguido
        if following > 0:
            ratio = followers / following
            if ratio > 10:
                info(f"Ratio {ratio:.1f}x — Perfil con gran alcance orgánico")
            elif ratio > 1:
                info(f"Ratio {ratio:.1f}x — Perfil equilibrado")
            else:
                info(f"Ratio {ratio:.1f}x — Sigue a más personas de las que le siguen")

        # Actividad estimada
        if posts > 0:
            posts_per_follower = followers / posts if posts else 0
            if followers > 10000 and posts < 50:
                warn("Pocos posts para la cantidad de seguidores — posible compra de seguidores")
            elif posts > 1000:
                info("Cuenta muy activa — más de 1000 publicaciones")

        # Detección cuenta fantasma/bot
        if followers > 10000 and following > 5000:
            warn("Seguidos muy alto — posible estrategia follow/unfollow")
        if followers < 100 and following > 1000:
            warn("Posible cuenta bot o spam")

    # Info adicional
    print(f"\n  {C}{B}── LINKS ÚTILES ──────────────────────────{RS}")
    dato("Perfil",        f"https://www.instagram.com/{username}/")
    dato("Posts",         f"https://www.instagram.com/{username}/posts/")
    dato("Reels",         f"https://www.instagram.com/{username}/reels/")
    dato("Tagged",        f"https://www.instagram.com/{username}/tagged/")
    dato("Picuki mirror", f"https://www.picuki.com/profile/{username}")
    dato("Imginn mirror", f"https://imginn.com/{username}/")
    dato("InstaDP foto",  f"https://www.instadp.com/fullsize/{username}")

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 4 — BÚSQUEDAS EXTERNAS
# ══════════════════════════════════════════════════════════════════════════════
def modulo_externo(username, data):
    sep("BÚSQUEDAS EXTERNAS")

    full_name = data.get("full_name", "")
    bio       = data.get("biography", "")

    print(f"  {C}{B}── GOOGLE DORKS ──────────────────────────{RS}")
    dorks = [
        (f'site:instagram.com "{username}"',              "Perfil en Google"),
        (f'"@{username}" instagram',                       "Menciones con @"),
        (f'"{username}" instagram filetype:pdf',           "En PDFs"),
        (f'"{username}" instagram email OR correo',        "Email asociado"),
    ]
    if full_name and full_name != "—":
        dorks += [
            (f'"{full_name}" instagram',                   "Nombre completo"),
            (f'"{full_name}" site:linkedin.com',           "LinkedIn del dueño"),
            (f'"{full_name}" email OR correo OR mail',     "Email del dueño"),
        ]

    for dork, desc in dorks:
        encoded = urllib.parse.quote(dork)
        url = f"https://www.google.com/search?q={encoded}"
        print(f"  {C}▸ {W}{desc:<30}{RS} {D}{url[:60]}{RS}")

    print(f"\n  {C}{B}── WAYBACK MACHINE ───────────────────────{RS}")
    wb_url = f"https://web.archive.org/web/*/instagram.com/{username}/"
    dato("Historial", wb_url)
    # Consultar Wayback
    try:
        r = requests.get(
            f"https://archive.org/wayback/available?url=instagram.com/{username}/",
            headers={"User-Agent": "cb-instahunter/1.0"},
            timeout=8
        )
        if r.status_code == 200:
            d = r.json()
            snap = d.get("archived_snapshots", {}).get("closest", {})
            if snap.get("available"):
                dato("Snapshot más cercano", snap.get("timestamp", "—"))
                dato("URL snapshot",         snap.get("url", "—"))
            else:
                warn("Sin snapshots en Wayback Machine")
    except Exception:
        warn("Wayback Machine no disponible")

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 5 — RESUMEN
# ══════════════════════════════════════════════════════════════════════════════
def modulo_resumen(username, data):
    sep("RESUMEN DE INTELIGENCIA")
    print(f"\n  {C}{B}Target:{RS}         {W}{B}@{username}{RS}")

    if not data.get("error"):
        print(f"  {C}{B}Nombre:{RS}         {W}{data.get('full_name','—')}{RS}")
        print(f"  {C}{B}ID:{RS}             {W}{data.get('id','—')}{RS}")
        print(f"  {C}{B}Seguidores:{RS}     {W}{fmt_number(data.get('followers',0))}{RS}")
        print(f"  {C}{B}Seguidos:{RS}       {W}{fmt_number(data.get('following',0))}{RS}")
        print(f"  {C}{B}Posts:{RS}          {W}{data.get('posts',0)}{RS}")
        print(f"  {C}{B}Privado:{RS}        {W}{'SÍ 🔒' if data.get('is_private') else 'NO 🌐'}{RS}")
        print(f"  {C}{B}Verificado:{RS}     {W}{'SÍ ✓' if data.get('is_verified') else 'NO'}{RS}")
        print(f"  {C}{B}Business:{RS}       {W}{'SÍ 💼' if data.get('is_business') else 'NO'}{RS}")
    print(f"\n  {D}Análisis completado — Ciberbrigada OSINT Suite v1.0{RS}\n")

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
            print(f"\n\n  {Y}Saliendo... Hasta pronto.{RS}\n")
            sys.exit(0)

        if username.lower() in ("salir", "exit", "quit", "q"):
            print(f"\n  {Y}Saliendo... Hasta pronto.{RS}\n")
            sys.exit(0)

        if not username or len(username) < 1:
            warn("Ingresá un username válido")
            continue

        if not re.match(r'^[a-zA-Z0-9._]+$', username):
            warn("Username inválido — solo letras, números, puntos y guiones bajos")
            continue

        print(f"\n  {C}Extrayendo datos de @{username}...{RS}")
        print(f"  {D}Esto puede tardar unos segundos{RS}\n")

        data = extraer_perfil(username)

        # Menú de módulos
        sep("SELECCIONÁ LOS MÓDULOS")
        modulos = [
            ("1", "Perfil          — Info completa del usuario"),
            ("2", "Posts recientes — Últimas publicaciones y engagement"),
            ("3", "Análisis        — Comportamiento, bio y detección"),
            ("4", "Búsquedas       — Google Dorks y Wayback Machine"),
            ("0", "TODOS LOS MÓDULOS"),
        ]
        for num, desc in modulos:
            color = C if num != "0" else Y
            print(f"  {color}[{num}]{RS} {W}{desc}{RS}")

        print()
        try:
            sel = input(f"  {C}▸ Opción (ej: 0 o 1,3):{RS} ").strip()
        except (KeyboardInterrupt, EOFError):
            sys.exit(0)

        selected = ["1","2","3","4"] if sel == "0" else [s.strip() for s in sel.split(",")]
        print()

        if "1" in selected: modulo_perfil(username, data)
        if "2" in selected: modulo_posts(username, data)
        if "3" in selected: modulo_analisis(username, data)
        if "4" in selected: modulo_externo(username, data)

        modulo_resumen(username, data)

        sep()
        print(f"\n  {D}¿Analizar otro usuario? (Enter / 'salir'){RS}")
        try:
            again = input(f"  {C}▸{RS} ").strip().lower()
            if again in ("salir", "exit", "quit", "q"):
                print(f"\n  {Y}Saliendo... Hasta pronto.{RS}\n")
                sys.exit(0)
        except (KeyboardInterrupt, EOFError):
            sys.exit(0)

        banner()

if __name__ == "__main__":
    main()
