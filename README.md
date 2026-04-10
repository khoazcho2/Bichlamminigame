# Chia Sẻ Link Tải Hay

## 🚀 Demo
Live on GitHub Pages (after deploy): [TBD]

## 📱 Features
- Search/filter categories realtime
- Beautiful responsive cards
- Admin panel: add/delete links
- Supabase realtime DB

## 🔐 Admin
- PW in script.js (hashed, change ADMIN_PW_HASH)
- Table: `link` (title, url, category)

## 🛠 Setup
1. Fork/Clone
2. Enable GitHub Pages (Settings > Pages > main branch)
3. Visit https://yourusername.github.io/repo

## 📊 Supabase
```
https://huhyetvefyhlhyldkvis.supabase.co
anon key: sb_publishable_40AA8unUr1HLIcgBn4gkFg_dvmCshjR
```
Table `link`: id (uuid), title, url, category, created_at (timestamptz)

**Security note: RLS optional for public read/anon write/delete (limit abuse w/ rules)**
