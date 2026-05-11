# 📸 CB-InstaHunter

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0-cyan?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/OSINT-Instagram-orange?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/free-sin%20login-brightgreen?style=for-the-badge"/>
</p>

<p align="center">
  <b>Instagram OSINT — Análisis completo de perfiles públicos sin login</b><br/>
  Parte de la <a href="https://ciberbrigada.com">Ciberbrigada OSINT Suite</a>
</p>

---

## ¿Qué hace?

CB-InstaHunter extrae y analiza datos de perfiles públicos de Instagram sin necesidad de cuenta ni login:

- ✅ Perfil completo (nombre, bio, ID, seguidores, seguidos, posts)
- ✅ Estado de cuenta (privado, verificado, business, categoría)
- ✅ Últimas publicaciones (fecha, likes, comentarios, hashtags)
- ✅ Tasa de engagement calculada automáticamente
- ✅ Nivel de influencer detectado automáticamente
- ✅ Análisis de biografía (emails, teléfonos, URLs, redes)
- ✅ Detección de comportamientos sospechosos (bots, compra de seguidores)
- ✅ Google Dorks automáticos
- ✅ Historial en Wayback Machine
- ✅ Links a mirrors públicos (Picuki, Imginn, InstaDP)

**100% gratuito · Sin login · Sin API key**

---

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/ciberbrigada/cb-instahunter
cd cb-instahunter

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar
python3 cb_insta_hunter.py
```

---

## 🔄 Mantener actualizado

```bash
cd cb-instahunter
git pull
```

---

## Uso

```bash
python3 cb_insta_hunter.py
```

```
▸ Username: nasa

[0] TODOS LOS MÓDULOS
[1] Perfil          — Info completa del usuario
[2] Posts recientes — Últimas publicaciones y engagement
[3] Análisis        — Comportamiento, bio y detección
[4] Búsquedas       — Google Dorks y Wayback Machine
```

---

## Módulos

| # | Módulo | Descripción |
|---|--------|-------------|
| 1 | Perfil | Nombre, ID, bio, seguidores, seguidos, posts, estado, links |
| 2 | Posts | Últimas publicaciones, likes, comentarios, hashtags, engagement |
| 3 | Análisis | Bio, comportamiento, detección bots, clasificación influencer |
| 4 | Búsquedas | Google Dorks, Wayback Machine, mirrors públicos |

---

## Técnicas de extracción

- API privada de Instagram (`?__a=1`)
- Scraping de HTML con múltiples patrones
- JSON embebido (`_sharedData`)
- Schema.org JSON-LD
- Mirror público (Picuki)

---

## Requisitos

- Python 3.8+
- requests
- colorama
- Conexión a internet

---

## ⚠️ Aviso Legal

Esta herramienta es para uso **exclusivamente legal, ético y educativo**.
Solo funciona con perfiles **públicos**. No bypasea ninguna medida de seguridad.
Ciberbrigada no se hace responsable del mal uso de esta herramienta.

---

## 🛡️ Ciberbrigada OSINT Suite

- 📧 **CB-EmailHunter** → [github.com/ciberbrigada/cb-emailhunter](https://github.com/ciberbrigada/cb-emailhunter)
- 👤 **CB-UserHunter** → [github.com/ciberbrigada/cb-userhunter](https://github.com/ciberbrigada/cb-userhunter)
- 📱 **CB-PhoneHunter** → [github.com/ciberbrigada/cb-phonehunter](https://github.com/ciberbrigada/cb-phonehunter)
- 📸 **CB-InstaHunter** → *(este repositorio)*
- 🌐 **CB-DomainHunter** → *(próximamente)*

---

<p align="center">
  <a href="https://ciberbrigada.com">ciberbrigada.com</a> ·
  <a href="https://github.com/ciberbrigada">GitHub</a> ·
  <a href="https://www.linkedin.com/company/ciberbrigada/">LinkedIn</a>
  <br/><br/>
  <sub>by: Fgunther</sub>
</p>
